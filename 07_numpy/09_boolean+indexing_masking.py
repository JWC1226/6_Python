"""
   Boolean Indexing & Masking
"""
import numpy as np
from load_utils import load_matrix, load_column

arr = np.array([10, 25, 45, 60, 95])
mask = arr > 50
print(f"arr: {arr}")
print(f"arr > 50: {mask}")
print(f"arr[mask]: {arr[mask]}")
# 대괄호 안에 mask를 넣으면 True에 해당하는 위치 값들만 추출하여 배열로 만들어준다
print(f"True 개수: {mask.sum()}")
print("-" * 50) # --------------------------------------------------

matrix = load_matrix()
big = matrix > 500_000
print(f"matrix > 500_000 :: shape {big.shape}, dtype {big.dtype}")
print(f"True의 개수: {big.sum()}개 / 전체: {matrix.size}개")
print(f"{matrix[big].shape}")       # 2 차원 배열에 Boolean Indexing > 1 차원 배열 추출
print("-" * 50) # --------------------------------------------------

# np.diff(배열, axis=1): 인접한 두 요소의 차를 계산 (오른쪽 값 - 왼쪽 값)
    # axis=1 이면 같은 행에서 열 방향으로 차(-)를 구할 것이다
    # Result : (120, 749)
result = np.diff(matrix, axis=1) / matrix[:,:-1]    # 일간 수익률
print(result)
cond1 = result > 0.03                               # 3% 넘게 오른 경우

# 거래량(volume)
volumes = load_column("volume")[:,1:]               # (120, 750) > (120, 749) 첫 날을 제외
cond2 = volumes > 2_000_000                         # 거래량이 200만 주(건) 초과된 경우
# and >> &    |    or >> |    |   not >> ~
both = cond1 & cond2
# [TIP] & 와 | 는 비교 연산자보다 우선순위가 높아서 (arr > 1) & (arr < 5) 처럼 조건마다 괄호가 꼭 필요하다
print(f"수익률이 3% 이상이고、거래량이 200만주 이상인 건수: {both.sum()}")
print(f"수익률이 3%가 되지 않는 건수: {(~cond1).sum()}")
print("-" * 50) # --------------------------------------------------

sample = np.array([0.05, -0.02, 0.0, 0.12, -0.15])
sample2 = np.where(sample > 0, "up", np.where(sample < 0, "down", "keep"))
print(sample2)


# ======================================================================
# [실무 TIP] np.select - 여러 조건을 한 번에 라벨링
# np.where 를 중첩하는 대신 조건 리스트와 값 리스트를 전달하면, 위에서부터 먼저 맞는 조건의 값이 선택된다
# ======================================================================
labels = np.select(
    [sample >= 0.1, sample > 0, sample < 0],
    ["급등", "상승", "하락"],
    default="보합",
)
print(f"{sample} > {labels}")
print(f"하루라도 3% 넘게 오른 종목 수: {cond1.any(axis=1).sum()} / 전체 {cond1.shape[0]}")
