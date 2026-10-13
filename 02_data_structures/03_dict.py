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
# [TIP] Python 3.7 부터 딕셔너리는 넣은 순서(삽입 순서)를 그대로 유지한다
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


# ======================================================================
# [실무 TIP] Counter / defaultdict / 딕셔너리 병합(|)
# collections 모듈의 Counter(개수 세기), defaultdict(기본값 자동 생성)는 집계 코드에서 매우 자주 사용된다
# ======================================================================
from collections import Counter, defaultdict

votes = ["Python", "Java", "Python", "SQL", "Python", "Java"]
counter = Counter(votes)
print(f"Counter: {counter} / 최다: {counter.most_common(1)}")

groups = defaultdict(list)              # 없는 key 에 접근하면 빈 리스트를 자동으로 만들어준다
for lang in votes:
    groups[lang[0]].append(lang)        # 첫 글자를 기준으로 묶기
print(f"defaultdict: {dict(groups)}")

base = {"host": "localhost", "port": 8080}
custom = {"port": 1521}
print(f"병합: {base | custom}")          # 같은 key 는 뒤쪽 값이 우선 (Python 3.9+) / 이전 버전은 {**base, **custom}
