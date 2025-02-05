import logging
import sys

"""
로깅 설정 모듈
역할:
1. 애플리케이션 전반의 로깅 설정
2. 로그 포맷 및 출력 레벨 관리
3. 디버깅 및 모니터링을 위한 로그 제공
"""

# 로깅 포맷 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# 로거 생성
logger = logging.getLogger("animal_lens")
logger.setLevel(logging.DEBUG)