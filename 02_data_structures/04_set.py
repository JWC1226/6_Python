"""
    집합 set
"""
# 중복 불가, 순서 X、수정 O
nums = {1, 2, 3, 3, 3, 4, 2}
print(f"nums: {nums}")
# 비어있는 상태는 어떻게 표현 > {}？
empty1 = {}
empty2 = set()
print(f"empty1: {type(empty1)}")
print(f"empty2: {type(empty2)}")
print()

nums = [1, 2, 3, 3, 3, 4, 2]
print(f"원본 데이터: {nums}")
print(f"중복 제거: {set(nums)}")
print(f"중복 제거(list): {list(set(nums))}")
# [TIP] set 은 순서를 보장하지 않는다 → 순서를 유지하면서 중복을 제거하려면 list(dict.fromkeys(nums)) 를 사용한다
print()

# 집합 연산
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(f"합집합 | : {a | b}")
print(f"교집합 & : {a & b}")
print(f"차집합 - : {a - b}")
print()

# 데이터 변경
data = {1, 2}
print(f"데이터 변경(data): {data}")

# 추가: add
data.add(3)
print(f"add(3) data: {data}")
data.add(3)
print(f"add(3) data: {data}")

# update
data.update([4, 5])
print(f"update[4,5] data: {data}")
data.update([4, 5, 6, 7])
print(f"update[4,5,6,7] data: {data}")

# 삭제 discard
data.discard(1)
print(f"discard(1) data: {data}")
data.discard(99)
print(f"discard(99) data: {data}")


# ======================================================================
# [실무 TIP] 포함 여부(in) 검사는 list 보다 set 이 훨씬 빠르다
# list 는 처음부터 하나씩 비교(O(n))하지만, set 은 해시로 바로 찾는다(O(1)) → 대량 데이터의 포함 여부 검사는 set 으로 한다
# ======================================================================
import time
big_list = list(range(1_000_000))
big_set = set(big_list)
start = time.perf_counter(); _ = 999_999 in big_list; t_list = time.perf_counter() - start
start = time.perf_counter(); _ = 999_999 in big_set;  t_set = time.perf_counter() - start
print(f"list: {t_list * 1000:.3f}ms / set: {t_set * 1000:.5f}ms")
print(f"대칭 차집합(^): {a ^ b} / {{1, 2}}는 a의 부분집합인가? {set([1, 2]) <= a}")
