from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text
from .config import settings
from .models import Animal, AnalysisResult
from typing import List, Dict
from contextlib import asynccontextmanager
from .logger import logger

"""
데이터베이스 관리 모듈
역할:
1. 데이터베이스 연결 및 세션 관리
2. 동물 데이터 조회 및 저장
3. 분석 결과 저장 및 조회
4. 미확인 동물 데이터 관리
"""

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

class Database:
    def __init__(self):
        self.session_maker = AsyncSessionLocal
    
    @asynccontextmanager
    async def transaction(self):
        """트랜잭션 컨텍스트 매니저"""
        async with self.session_maker() as session:
            async with session.begin():
                yield session
    
    async def is_animal(self, label: str) -> bool:
        """레이블이 동물인지 확인"""
        async with self.session_maker() as session:
            # 대소문자 구분 없이 부분 일치 검색
            query = select(Animal).filter(
                Animal.name.ilike(f"%{label}%") |  # 이름으로 검색
                Animal.species.ilike(f"%{label}%")  # 학명으로도 검색
            )
            result = await session.execute(query)
            is_match = bool(result.scalar_one_or_none())
            logger.debug(f"Checking if '{label}' is known animal. Query result: {is_match}")
            return is_match
    
    async def save_analysis_result(
        self,
        image_url: str,
        label: str,
        confidence: float
    ) -> AnalysisResult:
        """분석 결과 저장"""
        async with self.session_maker() as session:
            # 매칭되는 동물 찾기
            query = select(Animal).filter(Animal.name.ilike(f"%{label}%"))
            result = await session.execute(query)
            animal = result.scalar_one_or_none()
            
            # 결과 저장
            result = AnalysisResult(
                image_url=image_url,
                label=label,
                confidence=confidence,
                matched_animal_id=animal.id if animal else None
            )
            session.add(result)
            await session.commit()
            await session.refresh(result)
            return result

    async def find_matching_animals(self, label: str, confidence: float) -> List[Dict]:
        """레이블과 일치하는 모든 동물 찾기"""
        async with self.session_maker() as session:
            query = select(Animal).filter(Animal.name.ilike(f"%{label}%"))
            result = await session.execute(query)
            animals = result.scalars().all()
            
            return [
                {
                    "id": animal.id,
                    "name": animal.name,
                    "confidence": confidence,
                    "habitat": animal.habitat,
                    "diet": animal.diet,
                    "description": animal.description
                }
                for animal in animals
            ]

    async def get_analysis_result(self, result_id: str) -> Dict:
        """분석 결과 조회"""
        async with self.session_maker() as session:
            try:
                # 문자열 ID를 정수로 변환
                numeric_id = int(result_id)
                
                # 결과와 매칭된 동물 정보 함께 조회
                query = select(AnalysisResult, Animal).join(
                    Animal,
                    AnalysisResult.matched_animal_id == Animal.id,
                    isouter=True
                ).filter(AnalysisResult.id == numeric_id)
                
                result = await session.execute(query)
                row = result.first()
                
                if not row:
                    return None
                
                analysis_result, animal = row
                
                return {
                    "id": str(analysis_result.id),
                    "image_url": analysis_result.image_url,
                    "label": analysis_result.label,
                    "confidence": analysis_result.confidence,
                    "animal": {
                        "name": animal.name,
                        "species": animal.species,
                        "habitat": animal.habitat,
                        "diet": animal.diet,
                        "description": animal.description
                    } if animal else None
                }
            except ValueError:
                # ID가 유효한 정수가 아닌 경우
                return None

    async def save_unidentified_animal(
        self,
        image_url: str,
        label: str,
        confidence: float
    ) -> Dict:
        """미확인 동물 저장"""
        async with self.session_maker() as session:
            # 미확인 동물 저장
            unidentified = {
                'label': label,
                'confidence': confidence,
                'image_url': image_url
            }
            
            query = text("""
                INSERT INTO unidentified_animals (label, confidence, image_url)
                VALUES (:label, :confidence, :image_url)
                RETURNING id
            """)
            result = await session.execute(query, unidentified)
            await session.commit()
            
            # ID 추출
            row = result.first()
            unidentified_id = str(row[0]) if row else None
            
            return {
                "upload_id": unidentified_id,  # ID 추가
                "image_url": image_url,
                "label": label,
                "confidence": confidence,
                "message": "We don't have enough data about this animal yet. Our team will review and add it to our database soon."
            }

    async def get_unidentified_animal(self, result_id: str) -> Dict:
        """미확인 동물 조회"""
        async with self.session_maker() as session:
            try:
                numeric_id = int(result_id)
                query = text("""
                    SELECT id, label, confidence, image_url
                    FROM unidentified_animals
                    WHERE id = :id
                """)
                result = await session.execute(query, {"id": numeric_id})
                row = result.first()
                
                if not row:
                    return None
                    
                return {
                    "id": str(row.id),
                    "image_url": row.image_url,
                    "label": row.label,
                    "confidence": row.confidence,
                    "message": "We don't have enough data about this animal yet. Our team will review and add it to our database soon."
                }
            except ValueError:
                return None

database = Database() 