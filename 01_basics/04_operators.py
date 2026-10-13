"""
    연산자
"""
print("=" * 60)
print("산술 연산자")
print("=" * 60)

print(f"7 + 3 = {7 + 3}")
print(f"7 - 3 = {7 - 3}")
print(f"7 x 3 = {7 * 3}")
print(f"7 / 3 = {7 / 3}")   # 실수 나눗셈
print(f"7 // 3 = {7 // 3}") # 정수 나눗셈
print(f"7 % 3 = {7 % 3}")   # 나머지 연산
print(f"7 ^ 3 = {7 ** 3}")  # 거듭제곱 연산 / 7을 3번 곱함
# [TIP] Python 에서 ^ 는 거듭제곱이 아니라 비트 XOR 연산자이다 (7 ^ 3 == 4) / 거듭제곱은 ** 또는 pow() 를 사용한다
print()

print(f"실수 나눗셈 타입 : {type(7 / 3)}")
print(f"실수 나눗셈 타입 : {type(6 / 3)}")  # 타입은 항상 float
print(f"-7 / 3 = {-7 / 3}")
print(f"-7 // 3 = {-7 // 3}")   # Java에서는 버림 처리, Python에서는 내림 처리

print("=" * 60)
print("비교, 논리 연산자")
print("=" * 60)

a, b = 2, 5
print(f"a, b   >> {a}  {b}")
print(f"a == b >> {a == b}")
print(f"a != b >> {a != b}")
print(f"a < b  >> {a <  b}")
print(f"a >= b >> {a >= b}")
print()

# 논리 연산자: Java에서 &&, ||, ! 연산자가 아닌 Python에서는 and, or, not 키워드 사용
print(f"and >> {True and True}")
print(f" or >> {True or  False}")
print(f"not >> {not False}")

# a 값이 -5 ~ 5 사이의 값인가？
print(f"결과: {-5 <= a and a <= 5}")
print(f"{-5 <= a <= 5}")    # Python 에서는 연쇄 비교가 가능하다 !

#26. 09. 08: 멤버쉽 연산자 ~
print("=" * 60)
print("멤버쉽 연산자(in)、식별 연산자(is)")
print("=" * 60)

members = ["사용자", "이고은", "최제욱"]
print(f"> {members}")
print(f"'사용자' 포함 여부 > {'사용자' in members}")
print(f"'이용자' 포함 여부 > {'이용자' in members}")
print(f"'관리자' 포함하지 않는지? > {'관리자' not in members}")
print(f"{'ll' in 'hello'}")

x = [1,2,3]
y = [1,2,3]
z = x
print(f"x : {x} / y : {y} / z : {z}")
print(f"배열 　값 비교: {x == y}")
print(f"객체 주소 비교: {x is y}")
print(f"x is z : {x is z}")

# None 비교 시 is 사용을 권장
data = None
print(f"data is none? {data is None}")
print(f"data is not none? {data is not None}")
print()

print("=" * 60)
print("복합 대입 연산자")
print("=" * 60)
x = 10
print(f"x : {x}")
    # x = x + 5
x += 5
print(f"x += 5 : {x}")
    # x = x - 5
x -= 5
print(f"x -= 5 : {x}")
    # Python에서는 증감 연산자가 존재하지 않는다 ! (++、--)
# 증가 연산자 (++): 1씩 증가
x += 1
# 감소 연산자 (--): 1씩 감소
x -= 1


# ======================================================================
# [실무 TIP] divmod() / or 로 기본값 지정 / 바다코끼리 연산자(:=)
# ':=' 는 값을 대입하면서 동시에 그 값을 조건식에 사용할 수 있게 해준다 (Python 3.8+)
# ======================================================================
q, r = divmod(125, 60)                  # 몫과 나머지를 한 번에 → 125분 = 2시간 5분
print(f"125분 = {q}시간 {r}분")
nickname = "" or "익명"                  # 앞의 값이 falsy("", 0, None 등)이면 뒤의 값을 사용
print(f"nickname: {nickname}")
if (n := len(members)) > 2:             # 대입(n = len(members))과 비교를 한 번에
    print(f"회원 수 {n}명")
