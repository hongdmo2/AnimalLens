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
from fastapi import UploadFile
from ..config import settings
import uuid

# Initialize AWS S3 client with credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

async def upload_file(file: UploadFile) -> str:
    """
    Upload a file to S3 bucket and return its URL.
    
    Args:
        file (UploadFile): FastAPI UploadFile object
        
    Returns:
        str: Public URL of the uploaded file
        
    Raises:
        Exception: If file upload fails
    """
    # Generate unique filename with UUID
    file_extension = file.filename.split('.')[-1]
    file_key = f"uploads/{uuid.uuid4()}.{file_extension}"
    
    # Upload file to S3 without ACL
    s3_client.upload_fileobj(
        file.file,
        settings.S3_BUCKET,
        file_key,
        ExtraArgs={
            'ContentType': file.content_type
        }
    )
    
    # Generate and return S3 URL
    url = f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{file_key}"
    return url

def configure_bucket_cors():
    """
    Configure CORS settings for S3 bucket.
    
    Sets up CORS rules to allow frontend access to bucket resources.
    This function is called on application startup.
    
    Note:
        Failure to configure CORS will not stop the server from running
    """
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
        print(f"Error configuring CORS: {str(e)}")
        # Continue running even if CORS configuration fails

# Configure CORS on startup
configure_bucket_cors() 