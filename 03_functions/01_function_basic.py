"""
    함수
    - 정의 시 사용하는 키워드: def
"""
print("=" * 30)

# 함수 정의
def hello(name):
    return f"{name}님 안녕하세요"
# 함수 사용 (호출)
print(hello("사용자"))
result = hello("이용자")
print(result)

# hello 함수: 매개변수 O、반환값 O
def hello_print(name):
    print(f"{name}님 반갑습니다")
    # return X ! (생략)
hello_print("관리자")
print(hello_print("형상 관리자"))       # 반환 값이 없는 함수는 None을 반환한다 !
result = hello_print("문서 관리자")
print(f"result: {result}")             # 동일하게 None을 반환한다 !
print("=" * 30)

# 여러 값을 반환
def calc(a, b):
    return a + b, a - b, a * b
result = calc(5, 7)
print(f"결과: {result}")

# 언패킹 > 여러 변수로 나누어 저장할 수 있다
add, sub, mul =calc(5, 7)
print(f"결과: {add} {sub} {mul}")

print("=" * 30)
print("docstring (함수 설명 / 주석)")

def calc_tax(price, rate = 0.1):
    """
    부가세를 포함한 최종 금액을 반환하는 함수입니다
    """
    return price * (1 + rate)
print(f"10000원 >>> {calc_tax(10000):,}")
help(calc_tax)
# [TIP] docstring 은 help() 와 VS Code 마우스 오버에 표시되므로, 실무에서는 Args / Returns 형식으로 매개변수와 반환값을 적어두는 경우가 많다

# 주의할 점: Python은 호이스팅이라는 개념이 없기 때문에, 함수를 정의하기 전에는 호출이 불가합니다
# print(test())                        # 정의를 내리지 않으면 호출 할 수 없다
def test():
    return "테스트 함수입니다"


# ======================================================================
# [실무 TIP] 타입 힌트를 붙인 함수 정의
# '매개변수: 타입', '-> 반환타입' 형태로 작성하면 에디터 자동완성과 오류 검사가 정확해진다 (실행 결과에는 영향 없음)
# ======================================================================
def calc_total(prices: list[int], discount: float = 0.0) -> int:
    """할인율을 적용한 총 금액을 반환한다"""
    return int(sum(prices) * (1 - discount))

print(f"총 금액: {calc_total([12000, 8000, 4500], discount=0.1):,}원")
