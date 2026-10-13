"""
    스코프
    ・전역 변수：함수 외부에 선언된 변수
    ・지역 변수：함수 내부에 선언된 변수 (해당 함수 내에서만 접근이 가능하다)
"""
print("=" * 60)
print("지역 변수：함수 안에서 만든 변수는 함수 밖에서 안 보인다 !")

count = 0        # 전역 변수 (함수 내부가 아니므로)
def increase1(): # 함수 정의만 되어있는 상태
    count = 10   # 지역 변수 생성
    print(f"count: {count}")  # 10
increase1()
print(f"count: {count}")      # 0
def increase2():
    global count # global: 전역 변수 사용 명시
    count += 1   # count = count + 1
increase2()
print(f"count: {count}")
# [TIP] global 은 어디서 값이 바뀌는지 추적하기 어렵게 만들어서, 실무에서는 매개변수로 받고 return 으로 돌려주는 방식을 권장한다
print("=" * 40)

# 스코프 검색 순서: Local > Enclosing > Global > 생략(내장 함수)
data = "-- 전역 변수 --"
def outer():
    data = '-- 바깥 함수(outer) --'
    def inner():
        data = '-- 안쪽 함수(inner) --'
        print(f"** inner :: data：{data}")
    inner()
    print(f"** outer :: data：{data}")
outer()
print(f"** 전역에서 확인 :: data：{data}")
print("=" * 40)


# ======================================================================
# [실무 TIP] nonlocal 과 클로저 (Enclosing 스코프의 변수 수정)
# 안쪽 함수가 바깥 함수의 변수를 '수정'하려면 nonlocal 을 선언해야 한다 / 상태를 기억하는 함수를 만들 때 사용한다
# ======================================================================
def make_counter():
    count = 0
    def increase():
        nonlocal count                  # 바깥 함수(make_counter)의 count 를 사용
        count += 1
        return count
    return increase

counter = make_counter()
print(counter(), counter(), counter())  # 1 2 3
