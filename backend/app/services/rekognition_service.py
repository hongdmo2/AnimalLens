import boto3
from ..config import settings

rekognition_client = boto3.client(
    'rekognition',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

async def detect_labels(image_url: str) -> list:
    """이미지에서 레이블 감지"""
    # S3 URL에서 버킷 이름과 객체 키 추출
    # 예: https://bucket-name.s3.region.amazonaws.com/path/to/image.jpg
    bucket = settings.S3_BUCKET
    key = image_url.split(f"{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/")[1]
    
    try:
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            MaxLabels=10,
            MinConfidence=70
        )
        
        return [
            {
                "name": label["Name"],
                "confidence": label["Confidence"]
            }
            for label in response["Labels"]
        ]
    except Exception as e:
        print(f"Rekognition 분석 중 에러 발생: {str(e)}")
        raise 