"""
    딕셔너리 (dict)
"""
# JSON 형식과 유사한 구조
# key-value 형태로 데이터를 관리

user = {
    "name": "사용자",
    "age": 20,
    "skills": ["Java", "SQL", "html/css", "js", "Python"]
}
print(f"user: {user}")
# 딕셔너리 내의 데이터 접근 > key 값으로 접근
print(f"이름: {user['name']}")
print(f"스킬: {user['skills']}")
# print(f"연락처: {user['phone']}")
    # 직접 접근 시 존재하지 않는 key 값은 오류를 발생시킨다 !
print()
# get() 이라는 메소드를 사용하여 접근
print(f"이름: {user.get('name')}")
print(f"스킬: {user.get('skills')}")
print(f"연락처: {user.get('phone')}")
    # 존재하지 않는 key 값인 경우, None을 반환해준다
print(f"연락처: {user.get('phone', '없음')}")       # 기본 값 지정이 가능하다
print()
# 변경 (추가 / 수정 / 삭제)
user['email'] = 'user123@user.co.kr'               # 새로운 key 값을 지정하면 추가
print(f"user: {user}")
user['age'] = 40                                   # 기존의 key 값을 지정하면 변경된다
print(f"user: {user}")

del user['age']
print(f"user: {user}")
"""
del user['phone']                                  # 오류 발생 !
print(f"user: {user}")
"""
print()
print("=" * 120)

# 탐색
for key in user:
    print(f"key: {key} / value: {user[key]}")
print()
for k, v in user.items():
    print(f"key: {k} / value: {v}")
print()

print(f"Key 목록: {list(user.keys())}")
print(f"Value 목록: {list(user.values())}")
print(f"items(): {list(user.items())}")