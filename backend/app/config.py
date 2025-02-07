"""
Configuration Settings Module

This module manages all configuration settings for the Animal Lens application.
It uses pydantic_settings and python-dotenv for robust environment management.

Features:
- AWS credentials and region configuration
- Database connection settings
- CORS configuration
- Environment variable validation
- Automatic DATABASE_URL construction
"""

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Set environment and load appropriate .env file
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
ENV_FILE = f".env.{ENVIRONMENT}"

# Load environment variables from file
load_dotenv(ENV_FILE)

class Settings(BaseSettings):
    # AWS Configuration
    AWS_ACCESS_KEY_ID: str          # AWS access key for service authentication
    AWS_SECRET_ACCESS_KEY: str      # AWS secret key for service authentication
    AWS_REGION: str = "ap-northeast-2"  # Default AWS region
    S3_BUCKET: str                  # S3 bucket name for image storage
    
    # Database Configuration
    DB_USER: str                    # Database username
    DB_PASSWORD: str                # Database password
    DB_HOST: str                    # Database host address
    DB_PORT: int = 5432            # Database port (default: PostgreSQL)
    DB_NAME: str                    # Database name
    DATABASE_URL: str               # Full database connection URL
    
    # CORS Configuration
    FRONTEND_URL: str               # Frontend URL for CORS (e.g., Elastic IP or domain)
    BACKEND_URL: str               # Backend URL for API endpoints
    
    class Config:
        env_file = ENV_FILE
        extra = "ignore"           # 추가 필드 무시
        
    def __init__(self, **kwargs):
        # DB_PORT가 문자열이나 None이 아닌 정수로 설정되어 있는지 확인
        if 'DB_PORT' in kwargs:
            kwargs['DB_PORT'] = int(kwargs['DB_PORT'])
        
        if 'DATABASE_URL' not in kwargs:
            port = kwargs.get('DB_PORT', 5432)  # 기본값 5432
            kwargs['DATABASE_URL'] = f"postgresql+asyncpg://{kwargs.get('DB_USER')}:{kwargs.get('DB_PASSWORD')}@{kwargs.get('DB_HOST')}:{port}/{kwargs.get('DB_NAME')}"
        
        super().__init__(**kwargs)

    @property
    def is_development(self):
        """Check if running in development environment"""
        return ENVIRONMENT == 'development'

# Create global settings instance
settings = Settings() 