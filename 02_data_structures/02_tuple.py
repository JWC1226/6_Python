"""
    튜플 (tuple)
"""

# 튜플을 생성하는 방법 > ()
point = (10, 20)
point2 = 50, 60
single = (10,)      # 데이터가 1개일 때 콤마가 필수이다 !
single2 = (10)      # 이 경우는 무엇인가？ > 콤마가 없으면 튜플이 아니다 !
print(f"point : {point} {type(point)}")
print(f"point2 : {point2} {type(point2)}")
print(f"single : {single} {type(single)}")
print(f"single2 : {single2} {type(single2)}")
print()

print(f"point[0] : {point[0]}")     # 인덱스 접근은 가능하다 !
# point[0] = 99     # 수정이 불가하다 (불변성)
point = (99, 20)
print(f"point 자체를 변경 : {point}")
# 새로운 튜플 할당은 가능하다
print()

# 언패킹
t = (2, 6)
x, y = t
print(f"x, y : {x}, {y}")

# 함수 사용
def get_numbers():
    return 77, 44
x, y = get_numbers()
print(f"x, y : {x}, {y}")
print()

# 튜플 내에서 불필요한 값을 무시 > _ 사용
x , _, z = (10, 20, 30)
print(f"{x} {z}")

# 첫 번째 값만 변수에 저장하고 나머지는 따로 처리 > * 사용
x, *rest = (1,2,3,4,5)
print(f"x: {x}, rest: {rest}")      # 나머지 데이터는 리스트 형태로 패킹(묶음 처리)하였다

"""
    튜플 | 리스트
    불변 | 가변
    （） | []
    딕셔너리 키 O | 딕셔너리 키 X
"""
# [TIP] 좌표처럼 바뀌면 안 되는 묶음 데이터는 튜플로 표현하며, 불변이라서 딕셔너리의 key 나 set 의 원소로 사용할 수 있다
locations = {
    (35.5451, 126.9750): "서울역", 
    (30.5401, 124.9050): "부산역"
}


# ======================================================================
# [실무 TIP] NamedTuple - 이름으로 접근하는 튜플
# 인덱스(t[0]) 대신 이름(t.lat)으로 접근할 수 있어 읽기 쉽고, 튜플처럼 불변·언패킹도 그대로 가능하다
# ======================================================================
from typing import NamedTuple

class Station(NamedTuple):
    name: str
    lat: float
    lng: float

seoul = Station("서울역", 37.5547, 126.9706)
print(f"{seoul.name}: ({seoul.lat}, {seoul.lng})")
name, lat, lng = seoul                  # 일반 튜플처럼 언패킹
print(seoul)
