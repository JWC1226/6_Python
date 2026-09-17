"""
    공통 변수 (설정 항목)
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent         # 상위 폴더 위치 조정
DATA_DIR = BASE_DIR / "data"
RAW_PATH = DATA_DIR / "raw-prices.csv"
# / = 경로 연결을 돕는 역할을 한다
ENCODING = "utf-8-sig"

def path(name):
    """
        data 폴더 안의 파일 경로를 반환해주는 함수를 정의
    """
    return DATA_DIR / name