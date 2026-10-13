"""
    컴프리헨션
    > 간결하고 직관적인 데이터 구조 생성 문법 (list, dict, set을 생성)
"""

# 리스트 (list)
nums = []
for n in range(1, 6):
    nums.append(n)
print(F"nums: {nums}")

# 리스트 컴프리헨션 > [표현식 for 변수 in 반복대상]
nums = [n for n in range(1, 6)]
print(f"nums(컴프리헨션): {nums}")
nums = [n * n for n in range(1, 6)]
print(f"nums(컴프리헨션): {nums}")

# 조건에 해당하는 데이터만 포함할 때 > [표현식 for 변수 in 반복대상 if 조건]
nums = [1, 2, 3, 4, 5, 6]
print(f"짝수만 >> {[n for n in nums if n % 2 == 0]}")
print(f"3의 배수만 >> {[n for n in nums if n % 3 == 0]}")
# [TIP] 컴프리헨션이 두 줄 이상으로 길어지거나 조건이 복잡해지면 일반 for 문이 더 읽기 좋다 (가독성 우선)
print("=" * 60)

# 딕셔너리 컴프리헨션 > {key_표현식:value_표현식 for 변수 in 반복대상 if 조건}
menus = ["삼계탕", "炒码面", "刺身", "pâtes"]

# Key > 메뉴명, Value > 메뉴명의 길이
menus_dict = {m:len(m) for m in menus}
print(f"menus_dict: {menus_dict}")
menus_dict = {m:len(m) for m in menus if len(m) == 3}
print(f"menus_dict: {menus_dict}")

print("=" * 60)
# 셋 (set) 컴프리헨션 > {표현식 for 변수 in 반복대상 if 조건}
message = 'No pain, No gain'
    # 문자열에서 고유한 문자만 추출 (중복된 문자는 제외)
unique_char = {ch for ch in message}
print(f"'{message}'의 고유 문자: {unique_char}")
unique_char = {ch for ch in message if ch != ',' and ch != ' '}
print(f"'{message}'의 고유 문자: {unique_char} / ({len(unique_char)})")


# ======================================================================
# [실무 TIP] 조건부 표현식 / 중첩 리스트 펼치기 / 제너레이터 표현식
# 대괄호 [] 대신 소괄호 () 를 쓰면 값을 미리 만들지 않고 하나씩 생성하는 '제너레이터'가 되어 메모리를 거의 쓰지 않는다
# ======================================================================
nums = [1, 2, 3, 4, 5, 6]
print([("짝" if n % 2 == 0 else "홀") for n in nums])     # if-else 는 for 앞에 작성한다
matrix = [[1, 2, 3], [4, 5, 6]]
print([x for row in matrix for x in row])                # 2차원 > 1차원 (바깥 for 를 먼저 작성)
print(sum(n * n for n in range(1, 1_000_001)))           # 리스트를 만들지 않고 합계만 계산
