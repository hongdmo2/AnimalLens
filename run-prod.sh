#!/bin/bash
set -e  # 에러 발생 시 스크립트 중단

# 환경 설정
export ENVIRONMENT=production

# 환경 파일 확인
if [ ! -f .env.production ]; then
    echo "Error: .env.production file not found!"
    exit 1
fi

# 프로덕션 환경 실행
echo "Starting production environment..."
docker-compose -f docker-compose.prod.yml up --build -d 