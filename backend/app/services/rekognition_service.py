"""
AWS Rekognition Service Module

This module handles image analysis using AWS Rekognition service.
It provides functionality to detect labels (objects, scenes, concepts) in images.

Features:
- Image label detection from S3 objects
- Confidence score filtering
- Error handling for AWS Rekognition operations
- Support for multiple label detection
"""

import boto3
from ..config import settings
from ..logger import logger
from urllib.parse import urlparse

class RekognitionService:
    def __init__(self):
        """AWS Rekognition 서비스 초기화"""
        self.client = boto3.client(
            'rekognition',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

    async def detect_labels(self, image_url: str) -> list:
        """
        이미지에서 레이블(객체) 감지
        
        Args:
            image_url (str): S3에 업로드된 이미지 URL
            
        Returns:
            list: 감지된 레이블 목록
        """
        try:
            # S3 URL에서 버킷과 키 추출
            parsed_url = urlparse(image_url)
            bucket = parsed_url.netloc.split('.')[0]
            key = parsed_url.path.lstrip('/')
            
            # Rekognition API 호출
            response = self.client.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                },
                MaxLabels=10,
                MinConfidence=70
            )
            
            # 결과 처리
            labels = [
                {
                    'name': label['Name'],
                    'confidence': label['Confidence']
                }
                for label in response['Labels']
            ]
            
            logger.info(f"Detected labels: {labels}")
            return labels
            
        except Exception as e:
            logger.error(f"Rekognition error: {e}")
            raise

# 서비스 인스턴스 생성
rekognition_service = RekognitionService() 