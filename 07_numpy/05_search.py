"""
    넘파이 배열 : 검색, 정렬
    - where: 조건에 맞는 요소의 인덱스 반환 / 값 치환
    - argmax / argmin: 최대값/최소값이 있는 인덱스를 반환
    - sort: 정렬 
"""
import numpy as np

arr = np.array([10, 5, 22, 72, 8, 23])
print(f"arr: {arr}")
# 15보다 큰 값을 찾기
print("=== 15보다 큰 값을 찾기 ===")
idx_info = np.where(arr > 15)           # np.where(조건) > 조건에 해당하는 인덱스들을 반환
print(f"idx_info: {idx_info}")
print(arr[idx_info])

# 10보다 큰 값은 99로 변경
    # 아닌 값은 0으로 변경
arr2 = np.where(arr > 10, 99, 0)
print("=== 10보다 크면 99、아니면 0으로 변경 ===")
print(f"arr2: {arr2}")
# np.where(조건, 조건에-해당하면_변경할-값, 조건에 해당하지 않으면_변경할 값)
# > 조건에 따라 변경된 값으로 구성된 배열 반환
print("-" * 35) # --------------------------------------------------

arr = np.array([[10, 23, 5], [34, 16, 42]])
print(arr)
# 최대값의 인덱스 반환 : argmax
# 최소값의 인덱스 반환 : argmin
print(f"argmax : {np.argmax(arr)}")
print(f"argmin : {np.argmin(arr)}")
print(arr.flatten())
# 2 차원 배열을 1 차원으로 변환했을 때, 기준으로 인덱스를 반환해준다 !
# 축 (axis) 기준으로 조회
    # axis=0 : 열을 기준으로 조회
    # axis=1 : 행을 기준으로 조회
print(f"열 기준 최대값 인덱스: {np.argmax(arr, axis=0)}")
print(f"행 기준 최대값 인덱스: {np.argmax(arr, axis=1)}")
# [TIP] 2차원 배열에서 (행, 열) 위치가 필요하면 np.unravel_index(np.argmax(arr), arr.shape) 를 사용한다 (파일 하단 참고)
print("-" * 35) # --------------------------------------------------

arr = arr.flatten()
print(f"arr: {arr}")
# np.sort(배열): 원본 배열을 변경하지 않고、정렬된 새로운 배열을 반환해준다
sorted_arr = np.sort(arr)
print(f"정렬된 배열: {sorted_arr}")     # 오름차순
desc_arr = sorted_arr[::-1]            # 내림차순: 오름차순 정렬 후、역순으로 배치
print(desc_arr)

# 배열.sort(): 원본 배열 자체를 정렬시켜줌
print(f"arr: {arr}")
arr.sort()
print(f"정렬된 배열: {arr}")


# ======================================================================
# [실무 TIP] 상위 N개 찾기 - argsort / 값의 빈도 - unique
# argsort 는 '정렬했을 때의 인덱스 순서'를 반환하므로, 뒤에서부터 N개를 자르면 상위 N개의 위치를 얻을 수 있다
# ======================================================================
scores = np.array([72, 95, 88, 60, 95, 81])
top3_idx = np.argsort(scores)[::-1][:3]
print(f"상위 3개 위치: {top3_idx} / 값: {scores[top3_idx]}")
values, counts = np.unique(scores, return_counts=True)
print(f"고유값: {values} / 개수: {counts}")
m2 = np.array([[10, 23, 5], [34, 16, 42]])
print(f"최대값의 (행, 열) 위치: {np.unravel_index(np.argmax(m2), m2.shape)}")
