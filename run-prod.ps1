# 환경 변수 설정
$env:ENVIRONMENT = "production"

# 환경 파일 확인
if (-not (Test-Path .env.production)) {
    Write-Error "Error: .env.production file not found!"
    exit 1
}

# 프로덕션 환경 실행
Write-Host "Starting production environment..."
docker-compose -f docker-compose.prod.yml up -d --build 