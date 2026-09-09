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
print(f"10000원 >>> {calc_tax(1000):,}")
help(calc_tax)

# 주의할 점: Python은 호이스팅이라는 개념이 없기 때문에, 함수를 정의하기 전에는 호출이 불가합니다
# print(test())                        # 정의를 내리지 않으면 호출 할 수 없다
def test():
    return "테스트 함수입니다"