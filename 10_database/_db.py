"""
    DB 접속 관련 공통 모듈
    - 접속 정보는 .env에서만 읽을 것 !
      (코드 상에서 비밀번호를 저장하지 않는다)
"""
import os
import oracledb
from dotenv import load_dotenv
from sqlalchemy import create_engine
load_dotenv() # .env 파일을 읽어서 os.environ 에 저장 (채워준다)
# os.getnev('key 값', 기본값): 환경변수에서 kwy 값에 해당하는 값을 반환
                            # (기본값 제시하는 경우、값이 없을 경우에 사용)
HOST = os.getenv("DB_HOST", '127.0.0.1')
PORT = int(os.getenv("DB_PORT", 1521))
NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")

def connect(autocommit=False):
    """
        오라클에 연결 후 커넥션 객체를 반환하는 함수
        Args:
            autocommit : 자동 커밋 설정(기본값: False)
    """
    # 오라클에 연결 / DDL, UPSET처럼 세밀한 작업(제어)이 필요할 때 사용
    conn = oracledb.connect(
        user=USER, password=PASS, dsn=f"{HOST}:{PORT}/{NAME}" # =localhost:1521/xe
    )
    conn.autocommit = autocommit
    return conn
def get_engine():
    """
        SQLAlchemy 엔진을 반환해주는 함수
    """
    url = f"oracle+oracledb://{USER}:{PASS}@{HOST}:{PORT}/?service_name={NAME}"
         # "oracle+oracledb://사용자명:비밀번호@호스트:포트/?service_name=서비스명"
    # pool_pre_ping : 풀에서 커넥션을 꺼낼 때, 아직 살아있는지를 한 번 확인한다
    return create_engine(url, pool_pre_ping=True)
