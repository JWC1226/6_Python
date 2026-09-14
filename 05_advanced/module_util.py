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
print("=== module_util 모듈이 로드되었습니다 ===")