"""
    그룹화 기초 (groupby)
    - agg / transform
"""
import pandas as pd
from utils.loader import load_csv

# 출력창 크기 설정
pd.set_option("display.width", 130)

# 데이터 불러오기
df = load_csv()

# agg: 그룹 당 한 줄 (행)
# 'code' 열을 기준으로 평균을 조회
# SQL : SELECT code, AVG(close) FROM prices GROUP BY code
# Pandes
mean_by_code = df.groupby('code')['close'].mean()
print(f"종목 코드별 평균: {len(mean_by_code)}행")
print(mean_by_code.head().round())

# 여러 개를 한 번에 집계
summary = df.groupby('code').agg(
    평균종가 = ("close", "mean"), 최고가=("close", "max"), 거래일수=("date", "count")
)
print(f"통계 결과: {len(summary)}행")
print(summary.head())
"""
    .agg(
        새로운_열_이름=(계산할_기존_열_이름, 적용할_함수_이름),
    )
"""
# transform: 결과 행이 원본과 같은 길이로 반환
df['code_mean'] = df.groupby('code')['close'].transform('mean')
# [TIP] transform 결과는 원본과 길이가 같아서 df['close'] / df['code_mean'] 처럼 '그룹 평균 대비 비율'을 바로 계산할 수 있다
print(df.head())
print(df.tail())

"""
    ・agg: 여러 집계를 한 번에 확인하고자 할 때 사용한다
        df.groupby(기준열).agg(새로운_열_이름=(대상_열, 집계함수), ...)
    >>> 그룹 수 만큼 행을 반환해 준다
    >>> 그룹화하여 어떤 결과를 요약해서 볼 수 있도록 한다
    ・transform: 그룹별로 계산하되、기존 df와 연산을 하기 위해서 결과를 각 행의 원래 자리에 표시해준다
        df.groupby(기준열)[대상열].transform(집계함수)
    >>> 데이터 개수만큼 행 반환한다
    >>> 결과를 가지고 다음 연산을 수행할 수 있다
"""


# ======================================================================
# [실무 TIP] transform 으로 그룹 대비 비율 / 그룹 안에서의 순위
# rank() 도 groupby 와 함께 쓰면 그룹(종목) 안에서의 순위를 원본 길이 그대로 구해준다
# ======================================================================
df["vs_mean"] = (df["close"] / df["code_mean"]).round(3)                    # 종목 평균 대비 몇 배인가
df["rank_in_code"] = df.groupby("code")["close"].rank(ascending=False)    # 종목 안에서 종가 순위 (1 = 최고가)
print(df[["code", "date", "close", "code_mean", "vs_mean", "rank_in_code"]].head())
print(df.groupby("code")["close"].agg(["min", "max", "mean"]).head(3).round(0))   # 리스트로 여러 함수를 한 번에
