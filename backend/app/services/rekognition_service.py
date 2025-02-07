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

# Initialize AWS Rekognition client with credentials
rekognition_client = boto3.client(
    'rekognition',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

async def detect_labels(image_url: str) -> list:
    """
    Detect labels in an image stored in S3.
    
    Args:
        image_url (str): Full S3 URL of the image
            Format: https://bucket-name.s3.region.amazonaws.com/path/to/image.jpg
    
    Returns:
        list: List of detected labels with confidence scores
        
    Raises:
        Exception: If Rekognition analysis fails
    """
    # Extract bucket name and object key from S3 URL
    bucket = settings.S3_BUCKET
    key = image_url.split(f"{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/")[1]
    
    try:
        # Call Rekognition API to detect labels
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
        
        # Format and return the results
        return [
            {
                "name": label["Name"],
                "confidence": label["Confidence"]
            }
            for label in response["Labels"]
        ]
    except Exception as e:
        print(f"Error during Rekognition analysis: {str(e)}")
        raise 