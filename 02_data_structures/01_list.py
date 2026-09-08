"""
    리스트 (list)
"""
# 리스트 데이터 표현: 대괄호[]를 사용한다
colors = ["Crimson", "Teal", "Independence"]
print(f"colors > {colors}")
# 첫 번째 요소 출력
print(f"첫 번째: {colors[0]}")
# 마지막 요소 출력
print(f"마지막: {colors[-1]}")
print(f"{colors[0:2]}")

# 다양한 타입의 데이터를 담을 수 있다
mixed = [100, "Hello", True, [1,2,3]]
print(f"mixed: {mixed}")

# 리스트 상태에 따라 bool 타입 확인
temp = []
print(f"mixed >> {bool(mixed)}")
print(f"temp >> {bool(temp)}")
print("=" * 60)
items = ["에이스", "아이비", "코피코"]
print(f"item >> {items}")

# 데이터 추가: append(), insert(), extend()
items.append("포카칩")
print(f"append를 사용하면 맨 뒤에 추가: {items}")
items.insert(2, "쿠크다스")
print(f"insert를 사용하면 위치를 지정: {items}")
items.extend(["허니버터칩", "꼬깔콘"])
print(f"extend는 여러 개의 데이터를 추가: {items}")

# 수정 / 삭제
print("=" * 60)
items[0] = "ACE"
print(f"특정 인덱스를 지정하여 값을 변경: {items}")
items.remove("아이비")
print(f"remove는 값으로 삭제하는 방법: {items}")
# items.remove("아이비")                            # 해당 데이터가 없을 경우, ValueError를 발생시킨다
snak = items.pop()
print(f"pop을 사용하게 되면 맨 뒤의 데이터를 삭제 후 반환: {snak} / {items}")
del items[0]
print(f"del을 사용하게 되면 인덱스로 삭제: {items}")
