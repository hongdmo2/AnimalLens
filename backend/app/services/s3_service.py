"""
AWS S3 Service Module

This module handles all S3-related operations for the application.
It provides functionality for file uploads and CORS configuration.

Features:
- File upload to S3 bucket and return its URL.
- CORS configuration for S3 bucket
- URL generation for uploaded files
- Error handling for S3 operations
"""

import boto3
from ..config import settings
from ..logger import logger
import uuid
import os
import io

class S3Service:
    def __init__(self):
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.bucket_name = settings.S3_BUCKET
            logger.info("S3 service initialized successfully")
            self.configure_bucket_cors()
        except Exception as e:
            logger.error(f"Failed to initialize S3 service: {e}")
            raise

    def configure_bucket_cors(self):
        """S3 버킷의 CORS 설정"""
        try:
            cors_configuration = {
                'CORSRules': [{
                    'AllowedHeaders': ['*'],
                    'AllowedMethods': ['GET', 'POST', 'PUT'],
                    'AllowedOrigins': ['*'],
                    'ExposeHeaders': []
                }]
            }
            self.s3_client.put_bucket_cors(
                Bucket=self.bucket_name,
                CORSConfiguration=cors_configuration
            )
            logger.info("Successfully configured CORS for S3 bucket")
        except Exception as e:
            logger.error(f"Failed to configure CORS: {e}")
            # CORS 설정 실패는 치명적이지 않으므로 예외를 다시 발생시키지 않음

    async def upload_file(self, file_content: bytes, original_filename: str) -> str:
        """
        파일을 S3에 업로드하고 URL을 반환
        """
        try:
            # 파일 이름에 UUID 추가
            file_extension = os.path.splitext(original_filename)[1]
            filename = f"{uuid.uuid4()}{file_extension}"
            
            # S3에 업로드
            self.s3_client.upload_fileobj(
                io.BytesIO(file_content),
                self.bucket_name,
                filename,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
            
            # S3 URL 생성
            url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
            logger.info(f"File uploaded successfully: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise

# 서비스 인스턴스 생성을 지연시킴
_instance = None

def get_s3_service():
    global _instance
    if _instance is None:
        _instance = S3Service()
    return _instance

s3_service = get_s3_service() 