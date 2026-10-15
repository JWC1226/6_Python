"""
    공통 항목 설정
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))       # ~/12_ml
DATA_DIR = os.path.join(BASE_DIR, "data")                   # ~/12_ml/data
MODEL_DIR = os.path.join(BASE_DIR, "models")                # ~/12_ml/models
BASE_URL = "https://kh-lab.rockua.ai.kr"
ENCODING = "utf-8-sig"

def path(name):
    """data 폴더 안의 파일 경로 반환"""
    return os.path.join(DATA_DIR, name)

def prices_path():
    """일별 시세 데이터(prices.csv) 파일 경로 or URL 반환"""
    local = path("prices.csv")
    if os.path.exists(local):
        return local
    return f"{BASE_URL}/datasets/prices.csv"

def model_path(name="model_bundle.pkl"):
    """models 폴더 안에 파일 경로 반환"""
    # [TIP] 학습한 모델은 joblib.dump(model, model_path()) 로 저장하고, joblib.load(model_path()) 로 불러와서 재사용한다
    os.makedirs(MODEL_DIR, exist_ok=True)
    return os.path.join(MODEL_DIR, name)