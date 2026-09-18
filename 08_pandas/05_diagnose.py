"""
    점검하기
    > 데이터 정제 전에 데이터가 정상인지 여부를 확인하는 단계 (방법)
"""
import pandas as pd
from utils.config import RAW_PATH, ENCODING

# 옵션 없이 그대로 데이터를 읽어오기
df = pd.read_csv(RAW_PATH, encoding=ENCODING)
print(f"형태(행/열): {df.shape} / {df.shape[0]}행 {df.shape[1]}열")
print(f"상위 3개 데이터 조회: \n{df.head(3)}")
print(f"열별 데이터 타입 확인: \n{df.dtypes}")
"""
    close, volume 은 숫자(int)여야하는데、문자열(str)로 확인됨 !
    read_csv 는 열마다 타입을 추론하는데、한 열에 숫자가 아닌 값이 '하나라도' 존재하면 그 열은 전체가 문자열로 판단된다 !
"""
print("현재 상태에서 통계 조회")
print(df[['close', 'volume', 'high', 'low']].describe())
# int64 타입인 'high', 'low' 정상적으로 값이 출력
# str 타입인 'close', 'volume' 값이 출력되지 않는다 !

# df.close(): 행 수, 열 이름, non-null 개수, dtype 을 출력
df.info()
# non-null 개수를 통해 전체 행수와 다르면 결측이 있다고 판단

# 결측률
    # df.isnull() / df.isna()
na = df.isnull().sum()
print(f"{'열':<14}{'결측 수':<14}{'비율':<14}")
for col in df.columns:
    if na[col] > 0:
        print(f"{col:<14} {na[col]:<14}{na[col]/len(df)*100:>9.2f}")
# read csv 는 일부 문자열에 대해서 알아서 결측으로 변경해준다
    # 데이터에 N/A라고 되어있는 값을 읽을 때, NaN이 된다
    # 다른 문자들은 전부 결측처리가 되지..

# keep_default_na=False > 파일에 저장된 데이터를 그대로 읽어온다
# dtype=str > 모든 열을 문자열로 읽어온다
    # > "N/A" 값을 자동으로 Nan으로 처리했던 작업을 하지 않고, 문자열 그대로 읽어온다
df2 = pd.read_csv(RAW_PATH, encoding=ENCODING, keep_default_na=False, dtype=str)
print(f"{'열':<14}{'N/A':>10}{'-':>10}{'빈칸':>10}")
for col in ['close', 'volume']:
    na_cnt = (df2[col] == 'N/A').sum()
    dash_cnt = (df2[col] == '-').sum()
    blank_cnt = (df2[col] == '').sum()
    print(f"{col:<14}{na_cnt:>10}{dash_cnt:>10}{blank_cnt:>10}")

# 동일한 데이터가 오염되어 있어도 N/A은 결측으로 확인이 되는데
    # 오염된 데이터가 확실하게 확인하기가 어렵다 !
# 데이터를 읽어올 때 결측으로 판단할 값들을 지정할 수 있다 !
    # > na_values=['N/A', '-', ''] 옵션을 통해 결측 처리를 할 수 있다 !
print("-" * 40) # --------------------------------------------------

# values_counts(): 어떤 값이 몇 번 나오는 지 확인할 수 있다
    # dropna=False: 결측치(NaN)도 하나의 값으로 처리
print(df['close'].value_counts(dropna=False))

# 종가(close)
    # 오염된 데이터를 찾고자 할 때、이 방식으로 확인이 가능하다 ! (dropna=False)
print("-" * 40) # --------------------------------------------------

# to_numeric(errors="coerce"): 숫자로 변경이 불가능한 값에 대해 오류 대신 NaN으로..
for col in ['close', 'volume']:
    na_result = pd.to_numeric(df2[col], errors="coerce").isna().sum()
    print(f"{col:<10}:{na_result:>6}건")
# Comma(,)가 포함된 데이터도 숫자로 변경 불가능한 데이터에 포함된다 !
print("-" * 40) # --------------------------------------------------

# 데이터 중복 확인
    # duplicated(subset=[기준열, 기준열, ...])
        # > 원본 길이와 같은 결과를 반환 (True / False)
        # > 첫 번째 값은 Fasle, 두 번째부터 True
dup = df.duplicated(subset=['code', 'date']).sum()
print(f"(code, date) 중복 건수: {dup}")
print(f"중복 제거 후 개수: {len(df) - dup}")

# 날짜 형식
    # > 현재 실습 데이터에는 3가지 형식이 존재

# 1. 글자 수: .str.len()
lens = df['date'].astype(str).str.len().value_counts()
    # print(lens)
    # 2026-009-18, 2026.09.18 >> 10 글자
    # 20260918 >> 8 글자
print(f"20260918 형식: {lens.get(8, 0)}")

# 2. 패턴 검색 : .str.contains()
dot_cnt = df['data'].astype(str).str.contains(r"\.", regex=True).sum()
print(f"2026.09.18 형식: {dot_cnt}건")
print(f"2026-09-18 형식: {lens.get(10, 0) - dot_cnt}건")

temp = df.copy()
temp['date'] = pd.to_datetime(temp['date'], format='mixed')

# 3. temp.info()
dup2 = temp.duplicated(subset=['code', 'date']).sum()
print(f"날짜 데이터 변환 후 중복 건수: {dup2}")
print(f"날짜 형식 차이로 숨겨진 중복: {dup2 - dup}")
print("-" * 40) # --------------------------------------------------

temps = pd.DataFrame({
    'code': ['G0001', 'G0001', 'G0002'],
    'date': ['2026-09-18', '20260918', '2026-09-18'],
    'close': [24000, 24000, 24000]
})
print(temps)
print(f"문자열인 상태에서 중복: {temps.duplicated(subset=['code', 'date']).sum()}건")
temps['date'] = pd.to_datetime(temps['date'], format='mixed')
print(f"날짜 타입으로 변환 후 중복 체크: {temps.duplicated(subset=['code', 'date']).sum()}건")

# 어떤 데이터가 문제가 있는지를 진단
    # >> 타입 > 중복 > 결측 > 이상치 > 검증

# 데이터 정제 목표 정하기
print(f"{'항목':<24} {'현재':<14} {'목표':<14}")
print("-" * 40) # --------------------------------------------------

print(f"{'행수':<24} {len(df):<14} {'90,000':<14}")
print(f"{'종목수':24} {df['code'].nunique():<14} {'120':<14}")
print(f"{'종목별 행수(최소 ~ 최대)':<18}"
      f"{str(df.groupby('code').size().min()) + '~' + str(df.groupby('code').size().max()):<14} {'750':<14}")