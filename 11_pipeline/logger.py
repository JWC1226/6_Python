"""
    로깅 설정
    [단순 출력(print) 대신 로깅(logging)을 사용하는 이유]
    - 레벨 구분이 없다
        DEBUG・INFO・WARNING・ERROR・.. 로 중요도를 나눌 수 있다
    - 화면에만 메시지가 남는다
        자동으로 실행되는 프로그램에는 화면이 없어 메시지가 사라진다
    - 출력 시간을 직접 제시해야 한다
        포맷을 통해 자동으로 출력할 수 있다
    
    [로깅 구성 요소]
    - Logger: 로그를 남길 객체、logger.info(...)
    - Handler: 로그를 어디에 출력할 것인지를 설정
               StreamHandler > 화면(표준 출력)
               FileHandler > 파일
        Logger 하나에 여러 Handler를 연결하면 같은 메시지를 여러 곳에 출력할 수 있다
    - Formatter: 출력 형식을 설정하는 요소、시간/레벨/내용 형식을 지정할 수 있다
"""
import logging
import os
from datetime import datetime
from config import LOG_DIR

def setup(name="pipeline", level=logging.INFO):
    """
        화면과 파일에 동시에 기록하는 logger를 만들어서 반환
        Args:
            - name: logger 이름、getLogger(name)로 동일한 logger를 반환할 수 있다
            - level: log 레벨
                     DEBUG < INFO < WARNING < ERROR < CRITICAL 순으로 높아진다 !
        Return:
        설정이 완료된 Logger 객체
    """
    # 로그 폴더 생성 (있으면 패스 - exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # 저장될 로그 파일 설정 (YYYYmmdd.log > 20261001.log)
    path = os.path.koin(LOG_DIR, f"{datetime.now():%Y%m%d}.log")

    # Logger 객체 생성
    logger = logging.getLogger(name)

    # Log 레벨 설정
    logger.setLevel(level)

    # Handler 초기화
    logger.handlers.clear()
        # >> 함수(setup)가 여러 번 호출되면 동일한 메시지가 여러 번 출력될 수 있다
    
    # 출력 형식 설정
    fmt = logging.Formatter("%(asctime)s [%(levelname)-7s] %(message)s", "%H:%M:%S")
        # %(asctime)s     : log가 기록된 시간、두 번째 인자(%H:%M:%S) 형식으로 표시
        # %(levelname)-7s : log 레벨 이름 (INFO,ERROR,..)
                    # -7s : 7자리 왼쪽 정렬
        # %(message)s     : 실제 log 메시지 내용
        
    # Handler를 logger에 등록
    # [StreamHandler] > 화면에 출력(표준 출력)
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    # [FileHandler] > 파일 출력
    file = logging.FileHandler(path, encoding="utf-8")
    file.setFormatter(fmt)
    logger.addHandler(file)
    return logger