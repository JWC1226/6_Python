"""
    변수와 자료형에 대해서 다룰 예정..
"""

# 동적 타입 >> 타입 선언이 생략될 수 있다
name = "사용자"
age = 20
height = 182.3
is_tired = True     # || False
temp = None         # java에서 null과 동일하다

print(name, age, height, is_tired, temp)
print("=" * 60)
print("기본 자료형 5가지는 아래와 같다")
print("=" * 60)
# 변수에 저장된 데이터 타입 확인 > type(변수)
print(f"{name} : {type(name)}")
print(f"{age} : {type(age)}")
print(f"{height} : {type(height)}")
print(f"{is_tired} : {type(is_tired)}")
print(f"{temp} : {type(temp)}")
print("=" * 60)

value = 27
print(f"{value} : {type(value)}")
value = "스물일곱"
print(f"{value} : {type(value)}")
# 이전에 저장한 타입과 이후에 저장한 타입이 달라도 저장이 가능하다
# >> 혼란을 방지하기 위해 하나의 변수에는 하나의 타입만 사용하는 것을 '권장'한다
print("=" * 60)

# 다중 할당
x, y, z = 10, 20, 30
print(f"x, y, z -> {x}, {y}, {z}")
a = b = c = 100
print(f"a = b = c -> {a}, {b}, {c}")

# 값 교환
x, y = y, x
print(f"x, y -> {x} {y}")
print("=" * 60)

# 타입 힌트
menu: str = "Taco"
print(f"menu : {menu} ({type(menu)})")
price: int = "10000원"
print(f"price : {price} ({type(price)})")
# >> 타입 힌트는 강제성이 없으며, Error도 발생되지 않는다 !
# [TIP] 실행할 때 검사하지는 않지만 VS Code(Pylance)나 mypy 같은 도구가 미리 오류를 찾아주기 때문에 실무에서 널리 사용한다
print("=" * 60)

# 상수 > 대문자로 변수를 작성하는 것을 약속 (관례). final 키워드 X
# 최대 인원: "60명"이라는 값을 저장하려고 할 경우
MAX_PERSON = 60
print(f"최대 인원: {MAX_PERSON}")


# ======================================================================
# [실무 TIP] isinstance() 로 타입 확인하기
# type(x) == int 보다 isinstance(x, int) 를 권장한다 (상속 관계까지 인정하고, 여러 타입을 튜플로 한 번에 검사할 수 있다)
# ======================================================================
for v in [10, 3.14, "10", True]:
    print(f"{v!r:<6} 숫자인가? {isinstance(v, (int, float))}")
# 주의: bool 은 int 를 상속하기 때문에 isinstance(True, int) 도 True 이다
