"""
    결측치 처리
"""
import pandas as pd
from utils.config import step_path

# _step2.pkl 파일을 읽어서 df 변수에 저장
df = pd.read_pickle(step_path('_step2.pkl'))
print(f"Step 2: 이상치 처리 완료.. {len(df)}행")
print("현재 결측")
for col in ['open', 'high', 'low', 'close', 'volume']:
    n = df[col].isna().sum()
    if n:
        print(f"{col}:{n}건 ({n/len(df)*100:.2f}%)")
"""
    결측 처리 3가지 방법 (전략)
    1. 삭제: dropna(subset=,how=,...)
        > 삭제할 행 없이도 분석이 가능한지 ..?
    2. 대치: fillna(값/평균값/중앙값)
        > 대표값으로 적절한 것이 있는지 ..?
    3. 보간: interpolate()
        > 시계열. 앞뒤 값 사이를 잇는다 !
"""
print("-" * 40) # --------------------------------------------------

# 1. 보간 방법
    # > 종목별로 처리해줘야한다 !
edge = df.index[df['code'] != df['code'].shift()][1]
print(edge)

demo = df.loc[edge-2:edge+2, ['code','date','close']].copy()
print(demo)

demo.loc[edge, 'close'] = pd.NA
demo['close'] = pd.to_numeric(demo['close'], errors='coerce')
print("-" * 40) # --------------------------------------------------

print(demo)
print("-" * 40) # --------------------------------------------------

result1 = demo['close'].interpolate()
print(result1)
print("-" * 40) # --------------------------------------------------

result2 = demo.groupby('code')['close'].transform(lambda s: s.interpolate())
print(result2)
"""
    groupby 없이 보간처리를 하면、마지막 종가(G0001)와 뒷 종목의 다음 종가 사이를 강제로 잇는다
    groupby 를 사용하여 보간처리를 하면 해당 종목(= 그룹화 기준열) 안에서만 이어준다 !
"""
print("-" * 40) # --------------------------------------------------

# 열 별로 각각 다른 방법을 적용하여 처리
    # open, high, low, close > 종목별 보간 처리 진행 (시계열 데이터, 연속성)
    # volume > 결측 유지(0으로 채우면 안된다)
OHLC = ['open', 'high', 'low', 'close']
before = df[OHLC].isna().sum().sum()
print(f"OHLC 결측: {before}")

for col in OHLC:
    df[col] = df.groupby('code')[col].transform(lambda s: s.interpolate())
pola = df[OHLC].isna().sum().sum()
print(f"종목 별 보간 처리 후: {pola}")
# > 종목의 맨 앞/뒤에 남은 결측 개수
    # .ffill() : 결측을 바로 앞의 값으로 채운다
    # .bfill() : 결측을 바로 뒤의 값으로 채운다
    # [TIP] 예전 코드의 fillna(method="ffill") 은 pandas 2.1 부터 권장되지 않는다 → .ffill() / .bfill() 메소드를 사용한다
for col in OHLC:
    df[col] = df.groupby('code')[col].transform(lambda s: s.ffill().bfill())
fb = df[OHLC].isna().sum().sum()
print(f"ffill + bfill 처리 후: {fb}")

# 거래량(volume)은 결측 유지


# ======================================================================
# [실무 TIP] dropna(thresh) / fillna(딕셔너리)
# thresh=n 은 '결측이 아닌 값이 n개 이상인 행만 남긴다', fillna 에 딕셔너리를 주면 열마다 다른 값으로 채울 수 있다
# ======================================================================
print(f"volume 결측: {df['volume'].isna().sum()}")
kept = df.dropna(thresh=len(df.columns) - 1)            # 결측이 1개 이하인 행만 유지
print(f"dropna(thresh): {len(df)} > {len(kept)}행")
filled = df.fillna({"volume": 0})                      # 문법 예시 (실제로는 위 설명처럼 volume 을 0으로 채우면 안 된다)
print(f"fillna(dict) 후 volume 결측: {filled['volume'].isna().sum()}")
