"""
    import 하기 위한 모듈 (의미부여)
    - 직접 실행할 수 있고、다른 파일에서 가져다가 사용할 수 있다 (import)
"""
BASE_URL = "https://kh-academy.co.kr/"
def clean_price(text):
    """ `1000원`같은 문자열에서 숫자만 추출하는 함수 > 1000 """
    return int(text.replace(",", "").replace("원", "").strip())
def to_code(number):
    """
        어떤 특정 숫자가 전달되면 앞에 0을 채워서 6자리 문자로 반환해주는 함수를 제작
        5123 >> '005123'
    """
    return f"{number:06d}"
# [TIP] 모듈 최상단의 print 는 import 할 때마다 실행된다 → 테스트용 코드는 아래처럼 if __name__ == "__main__": 안에 넣는다
print("=== module_util 모듈이 로드되었습니다 ===")


# ======================================================================
# [실무 TIP] 직접 실행할 때만 동작하는 테스트 코드
# python module_util.py 로 실행하면 동작하고, 다른 파일에서 import 할 때는 실행되지 않는다
# ======================================================================
if __name__ == "__main__":
    print(clean_price(" 1,000원 "))     # 1000
    print(to_code(5123))                # 005123
