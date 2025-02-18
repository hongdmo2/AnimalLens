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
from .logger import logger
import socket

# Set environment and load appropriate .env file
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), f".env.{ENVIRONMENT}")

# Load environment variables from file
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)
    logger.debug(f"Loaded environment from {ENV_FILE}")
else:
    logger.error(f"Environment file not found: {ENV_FILE}")

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
    DATABASE_URL: str = ""          # Full database connection URL
    
    # CORS Configuration
    FRONTEND_URL: str               # Frontend URL for CORS (e.g., Elastic IP or domain)
    BACKEND_URL: str               # Backend URL for API endpoints
    
    class Config:
        env_file = ENV_FILE
        env_file_encoding = 'utf-8'
        case_sensitive = False
        extra = "ignore"           # ignore additional fields
        
    def __init__(self, **kwargs):
        # debug environment variables
        logger.debug(f"DB_USER: {os.getenv('DB_USER')}")
        logger.debug(f"DB_HOST: {os.getenv('DB_HOST')}")
        logger.debug(f"DB_NAME: {os.getenv('DB_NAME')}")
        logger.debug(f"DB_PORT: {os.getenv('DB_PORT')}")
        
        super().__init__(**kwargs)  # initialize parent class first
        
        # generate DATABASE_URL
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            logger.debug(f"Generated DATABASE_URL: {self.DATABASE_URL.replace(self.DB_PASSWORD, '****')}")

    @property
    def is_development(self):
        """Check if running in development environment"""
        return ENVIRONMENT == 'development'

# Create global settings instance
settings = Settings() 