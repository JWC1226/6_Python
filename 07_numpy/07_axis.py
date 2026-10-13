"""
    axis : 차원의 축을 의미한다
    - axis = 0 > 행의 방향
    - axis = 1 > 열의 방향
"""
print("=" * 60)
import numpy as np
from load_utils import load_matrix

# TODO: 2행 3열의 2 차원 배열 생성
m = np.array([[1,2,3], [4,5,6]])
print(f"m: \n{m}")
print(f"sum: {m.sum()}")
print(f"sum(axis=0): {m.sum(axis=0)} 열 기준(세로로 더함)")
print(f"sum(axis=1): {m.sum(axis=1)} 행 기준(가로로 더함)")
print("-" * 40) # --------------------------------------------------

print(f"m.shape: {m.shape}")
print(f"sum(axis=0): {m.sum(axis=0).shape} 행이 사라졌다 !")
print(f"sum(axis=1): {m.sum(axis=1).shape} 열이 사라졌다 !")
# axis 는 사라지는 축 !
# [TIP] axis=-1 은 '마지막 축'을 뜻해서, 차원 수와 상관없이 가장 안쪽 축을 기준으로 계산할 때 사용한다
    # shape: (120, 750)
        # axis = 0 > (750,)
        # axis = 1 > (120,)
print("-" * 40) # --------------------------------------------------

matrix = load_matrix()
print(f"matrix.shape: {matrix.shape}")
print(f"전체 평균: {matrix.mean()}")
print(f"날짜별 평균: {matrix.mean(axis=0)[:5]} {matrix.mean(axis=0).shape}")
print(f"종목별 평균: {matrix.mean(axis=1)[:5]} {matrix.mean(axis=1).shape}")
print("-" * 40) # --------------------------------------------------

# 줄인 축을 없애지 않고 유지하도록 하는 설정 (크기를 1로 남겨둔다)
    # keepdims=True
a = matrix.mean(axis=1)
b = matrix.mean(axis=1, keepdims=True)
print(f"a: {a.shape}")
print(f"b: {b.shape}")
# 값은 동일하다 / 축이 사라지지 않고 남아있다는 것만 다르다고 생각하면 된다
# (120, 750) 행렬과 연산을 수행하기 위해서 축을 유지시켜야 한다 !
# (120,) 이면 (120, 750)와 브로드 캐스팅 실패 !


# ======================================================================
# [실무 TIP] axis 와 argmax 를 함께 사용 - 종목별 최고가 날짜 찾기
# argmax(axis=1) 은 행(종목)마다 최대값이 있는 열(날짜) 위치를 반환한다
# ======================================================================
best_day = matrix.argmax(axis=1)                    # (120,) 종목마다 최고가였던 날의 위치
print(f"종목별 최고가 위치(앞 5개): {best_day[:5]}")
print(f"종목별 최고가(앞 5개): {matrix.max(axis=1)[:5]}")
print(f"날짜별 상승 종목 수(앞 5개): {(np.diff(matrix, axis=1) > 0).sum(axis=0)[:5]}")
