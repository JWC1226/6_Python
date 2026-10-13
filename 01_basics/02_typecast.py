"""
    형변환
"""
print("=" * 60)
print("문자열 >> 숫자")
print("=" * 60)

print(f"'100' >> {int('100')}")
print(f"'3.14' >> {float('3.14')}")
# print(f"'3.14' >> {int('3.14')}")     # valueError 발생
print(f"'3.14' >> {int(float('3.14'))}")
# 실수 형태의 문자열은 바로 int 변환이 불가하다 !
# > float 변환 후, int 변환
# [TIP] int() 는 앞뒤 공백은 허용한다 → int(" 42 ") == 42 / 하지만 "1,000" 처럼 콤마가 있으면 replace(",", "") 로 먼저 제거해야 한다

print("=" * 60)
print("숫자 >> 문자열")
print("=" * 60)

print(f"{str(1000)}")
# print(1000 + "원")
# 숫자와 문자열은 더하기(+) 연산이 불가하다 !
print(str(1000)+"원")
    # = print(f"{1000}원")
print("=" * 60)
print("bool 타입 변환")
print("=" * 60)

falsy_values = [0, 0.0, "", [], (), {}, set(), None, False]
truthy_values = [1, -1, "0", "False", [0], " "]
print("== falsy (거짓으로 취급되는 값) ==")
for v in falsy_values:
    print(f"{str(v):<10} -> {bool(v)}")
print("== truthy (참으로 취급되는 값) ==")
for v in truthy_values:
    print(f"{str(v):<10} -> {bool(v)}")


# ======================================================================
# [실무 TIP] 변환 전에 검사하기 - str.isdigit()
# 사용자 입력처럼 숫자가 아닐 수도 있는 값은 변환 전에 검사하거나, try/except(05_advanced)로 감싸서 처리한다
# ======================================================================
for text in ["123", "12.5", "abc", " 7 "]:
    s = text.strip()
    result = int(s) if s.isdigit() else "변환 불가"
    print(f"{text!r:<8} isdigit: {str(s.isdigit()):<6} > {result}")
