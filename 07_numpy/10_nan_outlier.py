"""
    결측과 이상치
"""
import numpy as np
from load_utils import load_dirty

arr, nan_idx, outlier_idx = load_dirty()
print(f"np.nan")
print(f"np.nan == np.nan ? {np.nan == np.nan}")
print(f"np.nan != np.nan ? {np.nan != np.nan}")
print(f"np.nan > 1 ? {np.nan > 1}")
print(f"np.nan < 1 ? {np.nan < 1}")
print(f"np.nan + 1 ? {np.nan + 1}")

# nan 뜻 자체가 Not a Number 이므로, "모르는 값"과 "모르는 값"을 비교하거나 연산을 수행했을 때、결과를 알 수 없다 !
result = (arr == np.nan)
print(f"arr == np.nan: {result.sum()}")

# 동등 비교로 결측치를 찾을 수 없다 !!
# [TIP] 결측 확인은 항상 np.isnan() 을 사용한다 (pandas 에서는 isna())
result = np.isnan(arr)
# print(result)
print(f"총 개수: {len(arr)} / 결측: {result.sum()}")
print(f"결측치의 위치: {np.where(result)[0]}")
print(f"평균: {np.mean(arr)} > {np.nanmean(arr):.2f}")
print()

for name, f1, f2 in [
    ("mean", np.mean, np.nanmean),
    ("sum", np.sum, np.nansum),
    ("std", np.std, np.nanstd),
    ("max", np.max, np.nanmax),
    ("min", np.min, np.nanmin)
]:
    r1 = f1(arr)
    r2 = f2(arr)
    print(f"{name} f1: {r1} f2: {r2}")
    """
        [결측치 해결 방법]
        1. 전용 함수 사용                       (np.nanXXXX)
        2. 결측치 제거                          arr[~np.isnan(arr)]                     # nan이 아닌 값만 추출
        3. 결측치를 다른 값으로 대체하는 방법     arr[np.isnan(arr)] = np.nanmean(arr)    # 평균으로 채우기
    """


# ======================================================================
# [실무 TIP] IQR 로 이상치 찾기 + np.clip 으로 범위 제한
# 이상치를 삭제하기 어려울 때는 정상 범위의 경계값으로 잘라내는(clip) 방식을 사용하기도 한다 (윈저라이징)
# ======================================================================
q1, q3 = np.nanpercentile(arr, [25, 75])
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
out_mask = (arr < lo) | (arr > hi)                  # nan 과의 비교는 항상 False
print(f"정상 범위: {lo:,.0f} ~ {hi:,.0f}")
print(f"IQR 이상치: {out_mask.sum()}개 / 실제로 넣은 이상치 {len(outlier_idx)}개 중 {out_mask[outlier_idx].sum()}개 탐지")
# 주가처럼 추세가 있는 데이터는 전체 IQR 로 보면 정상 값도 이상치로 잡힌다 → 08_pandas/06_outlier.py 처럼 기준을 보완해야 한다
clipped = np.clip(arr, lo, hi)
print(f"clip 전 최대값: {np.nanmax(arr):,.0f} > clip 후 최대값: {np.nanmax(clipped):,.0f}")
