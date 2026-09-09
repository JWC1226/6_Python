from functools import reduce             # reduce 함수 사용을 위해 추가됨

"""
    람다식과 고차함수
"""
print("=" * 60)
print("lambda: 익명 함수")

def double1(x):
    return x * 2
print(f"일반 함수: {double1(77)}")

# lambda 표현식 > lambda 매개변수: 반환식
double2 = lambda x: x * 2
print(f"람다 함수: {double2(77)}")

print("=" * 40)
print("고차 함수")

# map(): 전달한 함수를 적용하여 새로운 이터레이터 반환
numbers = [n for n in range(1, 7)]       # [1,2,3,4,5,6]
print(f"numbers: {numbers}")
result = list(map(lambda x: x * 2, numbers))
print(f"map 활용한 결과 도출: {result}")

# filter(): 조건을 만족하는 요소만 가지고 새로운 이터레이터를 반환한다
list(filter(lambda x: x % 2 == 0, numbers))
print(f"filter 적용한 결과: {result}")

# sorted(): 데이터를 정렬시켜주는 함수
numbers = [15, 26, 7, 3, 41, 17]
print(f"numbers: {numbers}")
print(f"오름차순 정렬: {sorted(numbers)}")
print(f"내림차순 정렬: {sorted(numbers, reverse=True)}")
print()

products = [
    {"name": "Hammer Smith Coffee", "price": 4500},
    {"name": "Lahg On Coffee", "price": 10500},
    {"name": "Mamoth Coffee", "price": 4600}
]
print(f"products: {products}")
print("=" * 145)
    # 가격(price) 기준으로 내림차순 정렬
by_price = sorted(products, reverse=True, key=lambda p:p['price'])
for p in by_price:
    print(f"{p['name']} : {p['price']}")
print("=" * 40)

    # 이름(name) 기준으로 오름차순 정렬
for p in sorted(products, key=lambda x: x['name']):
    print(f"{p['name']} : {p['price']}")
print("=" * 40)

# reduce: 순회하면서 누적 계산을 수행하는 함수
numbers = [10, 20, 30]
print(f"{reduce(lambda total, curr: total + curr, numbers, 0)}")
    # total: 누적 값
    # curr: 현재 값
datas = ["apple", "cat", "strawberry", "moon"]
    # 가장 긴 문자열을 찾기
longest = reduce(lambda result, curr: result if len(result) >= len(curr) else curr, datas)
print(f"결과 >> {longest}")

# 다양한 내장 함수
numbers = [7, 2, 7, 6, 9, 0]
print(f"numbers: {numbers}")
print(f"길이: {len(numbers)}")
print(f"총합: {sum(numbers)}")
print(f"최대값: {max(numbers)}")
print(f"최소값: {min(numbers)}")
print("=" * 40)
print(f"any: {any(n > 5 for n in numbers)}")
print(f"all: {all(n > 5 for n in numbers)}")