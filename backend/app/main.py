from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .services import s3_service, rekognition_service
from .database import database
from .config import settings
from .models import AnalysisResult
from .logger import logger  # 이것만 사용
from PIL import Image
import io
"""
FastAPI 메인 애플리케이션 파일
역할:
1. API 엔드포인트 정의 (/api/upload, /api/results/{id} 등)
2. 이미지 업로드 및 분석 프로세스 조정
3. 에러 처리 및 응답 관리
4. CORS 및 기타 미들웨어 설정
""" 
app = FastAPI(title="Animal Lens API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload")
async def upload_image(file: UploadFile):
    """
    이미지 업로드 및 분석 엔드포인트
    1. 이미지를 S3에 업로드
    2. Rekognition으로 동물 분석
    3. 결과를 DB에 저장
    4. 동물 레이블 필터링 (confidence >= 80%)
    5. 동물 레이블 검증 (DB에 있는지 확인)
    6. 결과 반환
    """
    try:
        # 시작 로그
        logger.info("=== Starting image upload and analysis ===")
        logger.info(f"File details - name: {file.filename}, size: {file.size}, type: {file.content_type}")

        # 파일 크기 검증 (5MB 제한)
        contents = await file.read()
        file_size_mb = len(contents) / (1024 * 1024)
        logger.debug(f"File size: {file_size_mb:.2f}MB")

        if file_size_mb > 5:
            logger.warning(f"File too large: {file_size_mb:.2f}MB")
            raise HTTPException(400, "File too large")
            
        # MIME 타입 검증
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, "Invalid file type")
            
        # PIL을 사용한 이미지 파일 유효성 검증
        try:
            image = Image.open(io.BytesIO(contents))
            image.verify()  # 이미지 파일 검증
        except Exception:
            raise HTTPException(400, "Invalid image file")
            
        # 파일 포인터 리셋 (검증 후 다시 처음부터 읽기 위해)
        file.file = io.BytesIO(contents)
            
        # 트랜잭션으로 모든 작업 처리
        async with database.transaction():
            # S3 업로드 전
            logger.info("Uploading to S3...")
            image_url = await s3_service.upload_file(file)
            logger.info(f"Successfully uploaded to S3: {image_url}")
            
            # Rekognition 분석 전
            logger.info("Starting Rekognition analysis...")
            labels = await rekognition_service.detect_labels(image_url)
            logger.info(f"Rekognition labels received: {labels}")
            
            # 결과 처리 전
            logger.info("Processing analysis results...")
            result = await process_analysis_results(image_url, labels)
            logger.info(f"Analysis complete. Result: {result}")
            
        return result
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(500, str(e))

async def process_analysis_results(image_url: str, labels: list) -> dict:
    """분석 결과를 처리하고 저장하는 함수"""
    logger.info("=== Starting analysis results processing ===")
    logger.debug(f"Image URL: {image_url}")
    logger.debug(f"All labels: {labels}")
    
    # 일반적인 레이블 제외
    GENERIC_LABELS = {
        'Animal', 'Mammal', 'Wildlife', 'Pet', 'Fauna',
        'Canine',  # 추가: 더 일반적인 분류
        'Carnivore',
        'Feline'
    }
    
    # 레이블 우선순위 (더 구체적인 순서대로)
    PRIORITY_LABELS = [
        'Golden Retriever', 'Labrador', 'Poodle',  # 구체적인 견종
        'Dog',  # 일반적인 종
        'Puppy'  # 기타
    ]
    
    # 신뢰도가 높은 레이블만 필터링
    high_confidence_labels = [
        label for label in labels 
        if label["confidence"] >= 80 and 
        label["name"] not in GENERIC_LABELS
    ]
    logger.info(f"Filtered specific animal labels: {high_confidence_labels}")
    
    if not high_confidence_labels:
        logger.warning("No specific animals detected in image")
        raise HTTPException(400, "No specific animals detected in image")
    
    # 우선순위에 따라 레이블 선택
    selected_label = None
    for priority_name in PRIORITY_LABELS:
        matching_labels = [
            label for label in high_confidence_labels 
            if label["name"] == priority_name
        ]
        if matching_labels:
            selected_label = max(matching_labels, key=lambda x: x["confidence"])
            break
    
    # 우선순위에 없는 경우 가장 높은 신뢰도의 레이블 선택
    if not selected_label:
        selected_label = max(high_confidence_labels, key=lambda x: x["confidence"])
    
    logger.info(f"Selected specific animal: {selected_label}")
    
    # DB에서 동물 확인
    is_known_animal = await database.is_animal(selected_label["name"])
    logger.info(f"Database lookup - Animal '{selected_label['name']}' is known: {is_known_animal}")
    
    if is_known_animal:
        logger.debug("Processing known animal")
        result = await database.save_analysis_result(
            image_url=image_url,
            label=selected_label["name"],
            confidence=selected_label["confidence"]
        )
        return {
            "upload_id": str(result.id),
            "image_url": image_url
        }
    else:
        logger.debug("Processing unknown animal")
        return await database.save_unidentified_animal(
            image_url=image_url,
            label=selected_label["name"],
            confidence=selected_label["confidence"]
        )

@app.get("/api/test")
async def test_connection():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/api/results/{result_id}")
async def get_result(result_id: str):
    """분석 결과 조회"""
    try:
        # 일반 분석 결과 조회
        result = await database.get_analysis_result(result_id)
        if result:
            return result
            
        # 미확인 동물 결과 조회
        result = await database.get_unidentified_animal(result_id)
        if result:
            return result
            
        raise HTTPException(404, "Result not found")
    except Exception as e:
        logger.error(f"Failed to get result: {str(e)}")
        raise HTTPException(500, str(e))

