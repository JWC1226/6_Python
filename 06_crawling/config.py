"""
   공통 변수를 저장하는 파일 
"""
BASE = "https://kh-lab.rockua.ai.kr"
TIMEOUT = 5
# [TIP] timeout 을 지정하지 않으면 서버가 응답하지 않을 때 프로그램이 무한정 멈출 수 있으므로 항상 지정한다
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}