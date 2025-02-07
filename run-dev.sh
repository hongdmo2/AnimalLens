#!/bin/bash
set -e  # 에러 발생 시 스크립트 중단

# 환경 설정
export ENVIRONMENT=development

# 환경 파일 확인
if [ ! -f .env.development ]; then
    echo "Error: .env.development file not found!"
    exit 1
fi

# 개발 환경 실행
echo "Starting development environment..."
docker-compose -f docker-compose.dev.yml up --build 