"""
    문자열 다루기
"""
print("=" * 60)
print("인덱싱, 슬라이싱")
print("=" * 60)
# 인덱스는 0부터 시작
message = "No pain, No gain"
print(f"메세지: {message}")
print()

#인덱싱 : 변수[인덱스]
print(f"첫 글자 : {message[0]}")
print(f"마지막 글자: {message[-1]}")

# 슬라이싱 : 변수[시작:끝:간격]
print(f"{message[0:7:1]} / {message[0:7]} / {message[:7]}")
print(f"{message[7:]}")
print(f"{message[::2]}")  # 2칸 간격으로 슬라이싱 처리
print(f"{message[::-1]}") # -1, 역순으로 슬라이싱 처리

print("=" * 60)
print("다양한 문자열 메소드")
print("=" * 60)

# 대문자 변환 : upper()
print(f"대문자 변환: {message.upper()}")
# 소문자 변환 : Lower()
print(f"소문자 변환: {message.lower()}")
message = "    Python World    "
print(f"[{message}]")
# 좌우 공백 제거: strip()
print(f"좌우 공백 제거: [{message.strip()}]")
# 문자열을 구분자로 분할: split(구분자)
print(f"split : [{message.split(',')}]")
# [TIP] split() 처럼 인자를 생략하면 공백(스페이스·탭·줄바꿈) 기준으로 나누고, 연속된 공백도 하나로 취급한다 → message.split()
# 특정 문자의 개수를 반환 : count(문자)
print(f"l의 개수: {message.count('l')}")
# 특정 문자의 인덱스 반환: find(문자)
print(f"Python의 위치: {message.find('Python')}")
print(f"Java의 위치: {message.find('Java')}")       # 없으면 -1을 반환
# 리스트 >> 문자열 (문자열 결합)
today = '-'.join(['2026', '09', '07'])
print(today)
print(f"today: {today} {type(today)}")
print("=" * 60)
print("여러 줄 문자열")
print("=" * 60)

# 여러 줄 문자열 > 따옴표 3개
end_message = """
    문자열 다루기
    - 인덱싱, 슬라이싱
    - 자주 사용하는 메소드 (split, join, strip, ...)
"""
print(end_message)


# ======================================================================
# [실무 TIP] 자주 쓰는 문자열 메소드 - replace / startswith / zfill / join
# 문자열은 불변(immutable)이라서 메소드는 항상 '새 문자열'을 반환한다 (원본은 그대로 유지)
# ======================================================================
price_text = " 1,234,000원 "
print(int(price_text.strip().replace(",", "").replace("원", "")))      # 1234000
file_name = "report_2026.csv"
print(file_name.startswith("report"), file_name.endswith((".csv", ".xlsx")))   # True True
print("7".zfill(6))                                                     # 000007 (종목 코드처럼 앞을 0으로 채우기)
words = ["No", "pain", "No", "gain"]
print(" ".join(words))      # 반복문에서 += 로 이어 붙이는 것보다 join 이 빠르고 간결하다
