import boto3
from fastapi import UploadFile
from ..config import settings
import uuid

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

async def upload_file(file: UploadFile) -> str:
    """파일을 S3에 업로드하고 URL을 반환"""
    file_extension = file.filename.split('.')[-1]
    file_key = f"uploads/{uuid.uuid4()}.{file_extension}"
    
    # 파일 업로드 (ACL 제거)
    s3_client.upload_fileobj(
        file.file,
        settings.S3_BUCKET,
        file_key,
        ExtraArgs={
            'ContentType': file.content_type
        }
    )
    
    # S3 URL 생성
    url = f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{file_key}"
    return url

def configure_bucket_cors():
    """S3 버킷 CORS 설정"""
    try:
        cors_configuration = {
            'CORSRules': [{
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'POST'],
                'AllowedOrigins': [settings.FRONTEND_URL],
                'ExposeHeaders': ['ETag'],
                'MaxAgeSeconds': 3000
            }]
        }
        
        s3_client.put_bucket_cors(
            Bucket=settings.S3_BUCKET,
            CORSConfiguration=cors_configuration
        )
    except Exception as e:
        print(f"CORS 설정 중 에러 발생: {str(e)}")
        # CORS 설정 실패해도 서버는 계속 실행되도록 함

# FastAPI 시작 시 CORS 설정 시도
configure_bucket_cors() 