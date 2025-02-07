# 환경 변수 설정
$env:ENVIRONMENT = "development"

# 환경 파일 확인
if (-not (Test-Path .env.development)) {
    Write-Error "Error: .env.development file not found!"
    exit 1
}

# 개발 환경 실행
Write-Host "Starting development environment..."

# 기존 컨테이너 정리 (선택적)
docker-compose -f docker-compose.dev.yml down

# 컨테이너 시작
docker-compose -f docker-compose.dev.yml up --build 