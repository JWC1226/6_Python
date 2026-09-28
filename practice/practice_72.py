"""
    ==============================================================================
    [신작 FPS 기획] 경쟁작 연간 시장 데이터 기반 타겟팅 전략 수립 실습
    ------------------------------------------------------------------------------
    시니어 게임 데이터 분석가(Game Market BI Analyst)가 신입 분석가에게 출제하는
    가상 데이터셋 + 4단계 시각화 과제입니다.

    각 과제는 아래 4단계 서식으로 구성되어 있습니다.
        1) [비즈니스 문제 의도]
        2) [분석 및 시각화 힌트]
        3) [TODO 빈칸 템플릿 코드]
        4) [비즈니스 인사이트 질의]
    ==============================================================================
"""
import platform
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

# 한글 폰트 및 마이너스 기호 깨짐 방지
# 오류 수정: sns.set_style()이 font.family를 'sans-serif'로 되돌리므로,
# 반드시 set_style을 먼저 호출한 뒤 한글 폰트를 지정해야 함 (순서 변경)
sns.set_style('whitegrid')
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# 차트 저장 경로 (output 폴더) - VSCode 탐색기/미리보기로 바로 이미지 확인 가능
# --------------------------------------------------------------------------------
OUTPUT_DIR = Path(__file__).with_name('output')
OUTPUT_DIR.mkdir(exist_ok=True)


def save_chart(fig, filename):
    """완성된 차트를 output/ 폴더에 PNG로 저장"""
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=120, bbox_inches='tight')
    print(f'차트 저장 완료: {path}')


# 0. 가상 데이터셋 생성 (재현성 보장: np.random.seed(42))
#    ※ 실제 서비스 지표가 아닌, 실습을 위한 가상(synthetic) 데이터입니다.
np.random.seed(42)
YEARS = list(range(2022, 2027))  # 2022 ~ 2026, 5개년
# 게임별 기본 속성(플랫폼/BM) 및 연도별 추세 파라미터
#   base_*   : 2022년 기준값
#   *_trend  : 연간 변화량(선형 추세, 2022년 대비 매년 더해지는 값)
#   실제 값은 아래 생성 루프에서 추세 + 노이즈(np.random.normal)로 계산됨
GAME_META = {
    'Overwatch 2':           dict(platform='Crossplay',      bm_type='Hybrid/BattlePass',
                                   base_ccu=220_000,  ccu_trend=-15_000,
                                   base_rev=420,  rev_trend=-10,
                                   base_rating=62, rating_trend=-3,
                                   base_neg=32,   neg_trend=3.0),
    'Valorant':               dict(platform='PC 전용',        bm_type='F2P',
                                   base_ccu=350_000,  ccu_trend=25_000,
                                   base_rev=500,  rev_trend=60,
                                   base_rating=82, rating_trend=1,
                                   base_neg=15,   neg_trend=-0.5),
    'Rainbow Six Siege':      dict(platform='Console 전용',   bm_type='Hybrid/BattlePass',
                                   base_ccu=90_000,   ccu_trend=5_000,
                                   base_rev=260,  rev_trend=15,
                                   base_rating=78, rating_trend=0.5,
                                   base_neg=18,   neg_trend=0.0),
    'Delta Force':            dict(platform='Crossplay',      bm_type='F2P',
                                   base_ccu=60_000,   ccu_trend=180_000,
                                   base_rev=40,   rev_trend=220,
                                   base_rating=80, rating_trend=2,
                                   base_neg=12,   neg_trend=-1.0),
    'Counter-Strike 2':       dict(platform='PC 전용',        bm_type='F2P',
                                   base_ccu=1_100_000, ccu_trend=60_000,
                                   base_rev=850,  rev_trend=90,
                                   base_rating=86, rating_trend=0.5,
                                   base_neg=10,   neg_trend=0.5),
    'Apex Legends':           dict(platform='Crossplay',      bm_type='Hybrid/BattlePass',
                                   base_ccu=250_000,  ccu_trend=-8_000,
                                   base_rev=480,  rev_trend=-5,
                                   base_rating=74, rating_trend=-1,
                                   base_neg=22,   neg_trend=1.0),
    'Call of Duty: Warzone':  dict(platform='Console 전용',   bm_type='Hybrid/BattlePass',
                                   base_ccu=300_000,  ccu_trend=-10_000,
                                   base_rev=900,  rev_trend=-20,
                                   base_rating=65, rating_trend=-1,
                                   base_neg=30,   neg_trend=1.5),
    'PUBG: BATTLEGROUNDS':    dict(platform='Crossplay',      bm_type='F2P',
                                   base_ccu=400_000,  ccu_trend=-20_000,
                                   base_rev=380,  rev_trend=-15,
                                   base_rating=68, rating_trend=-0.5,
                                   base_neg=25,   neg_trend=0.5),
    'The Finals':             dict(platform='Crossplay',      bm_type='F2P',
                                   base_ccu=130_000,  ccu_trend=10_000,
                                   base_rev=60,   rev_trend=20,
                                   base_rating=84, rating_trend=1,
                                   base_neg=14,   neg_trend=-0.5),
    'Escape from Tarkov':     dict(platform='PC 전용',        bm_type='Buy-to-Play',
                                   base_ccu=70_000,   ccu_trend=3_000,
                                   base_rev=150,  rev_trend=25,
                                   base_rating=72, rating_trend=-2,
                                   base_neg=28,   neg_trend=2.0),
}
records = []
for game, meta in GAME_META.items():
    for i, year in enumerate(YEARS):
        ccu = meta['base_ccu'] + meta['ccu_trend'] * i + np.random.normal(0, meta['base_ccu'] * 0.05)
        revenue = meta['base_rev'] + meta['rev_trend'] * i + np.random.normal(0, meta['base_rev'] * 0.08)
        rating = meta['base_rating'] + meta['rating_trend'] * i + np.random.normal(0, 2.5)
        neg_rate = meta['base_neg'] + meta['neg_trend'] * i + np.random.normal(0, 2.0)

        records.append({
            'game_title': game,
            'year': year,
            'platform': meta['platform'],
            'bm_type': meta['bm_type'],
            'annual_revenue_mil': revenue,
            'avg_ccu': ccu,
            'user_rating_pct': rating,
            'negative_review_rate': neg_rate,
        })
df = pd.DataFrame(records)

# 스펙 범위 클리핑
df['annual_revenue_mil'] = df['annual_revenue_mil'].clip(20, 1500).round(1)
df['avg_ccu'] = df['avg_ccu'].clip(10_000, 1_500_000).round(0).astype(int)
df['user_rating_pct'] = df['user_rating_pct'].clip(30, 98).round(1)
df['negative_review_rate'] = df['negative_review_rate'].clip(5, 60).round(1)
# --------------------------------------------------------------------------------

# [현업 이상치 주입]
# 이상치 1: 동접자 수는 급증했지만 매출/평점은 급락한 사례
#           (Overwatch 2, PvE 콘텐츠 축소 논란 시점을 가정한 2023년)
mask_ow_2023 = (df['game_title'] == 'Overwatch 2') & (df['year'] == 2023)
df.loc[mask_ow_2023, 'avg_ccu'] = 480_000
df.loc[mask_ow_2023, 'annual_revenue_mil'] = 180.0
df.loc[mask_ow_2023, 'user_rating_pct'] = 35.0
df.loc[mask_ow_2023, 'negative_review_rate'] = 58.0

# 이상치 2: 동접자 수 대비 유저당 매출(ARPU)이 기형적으로 높은 사례
#           (Escape from Tarkov, 고가 한정판 대량 판매 시즌을 가정한 2024년)
mask_tarkov_2024 = (df['game_title'] == 'Escape from Tarkov') & (df['year'] == 2024)
df.loc[mask_tarkov_2024, 'avg_ccu'] = 78_000
df.loc[mask_tarkov_2024, 'annual_revenue_mil'] = 480.0
# --------------------------------------------------------------------------------

# 결측치 주입: user_rating_pct 컬럼에 약 3~5% 결측치 발생
n_missing = max(1, int(len(df) * 0.04))
missing_idx = np.random.choice(df.index, size=n_missing, replace=False)
df.loc[missing_idx, 'user_rating_pct'] = np.nan
df = df.reset_index(drop=True)
print(f'데이터셋 생성 완료: {df.shape[0]}행 x {df.shape[1]}열')
print(df.head(10))
print()

# ================================================================================
# 결측치 확인/전처리 + BM타입 · 플랫폼별 연간 평균 매출 비교 (Bar Chart)
"""
    [비즈니스 문제 의도]
    결측치를 처리하지 않고 바로 분석하면 평균/분포 통계가 왜곡될 수 있습니다.
    또한 신작의 BM(F2P / Buy-to-Play / Hybrid-BattlePass)과
    플랫폼(PC전용 / Console전용 / Crossplay) 전략을 확정하기 전에、
    "실제로 어떤 조합이 더 높은 매출을 내고 있는가?"를 데이터로 검증해야 합니다.

    [분석 및 시각화 힌트]
    - 결측치 확인: df.isnull().sum()
    - 결측치 대체: groupby('game_title')['user_rating_pct'].transform('mean')로 게임별 평균 대체
      (단순 dropna는 표본이 줄어드는 단점이 있음)
    - 그룹 집계: df.groupby(['bm_type', 'platform'])['annual_revenue_mil'].mean()
    - 시각화: sns.barplot(data=, x=, y=, hue=)
    - 축 포맷: matplotlib.ticker.FuncFormatter 로 '$1,234M' 형태 표시
"""

# ================================================================================
# Step 1. 결측치 현황 점검
missing_summary = df.isnull().sum()
print('결측치 현황:')
print(missing_summary)
print("-" * 40) # --------------------------------------------------

# Step 2. 결측치 전처리 (게임별 평균 평점으로 대체)
df['user_rating_pct'] = df['user_rating_pct'].fillna(
    df.groupby('game_title')['user_rating_pct'].transform('mean')
)

# Step 3. BM타입 x 플랫폼별 연평균 매출 집계
revenue_summary = df.groupby(['bm_type', 'platform'])['annual_revenue_mil'].mean().reset_index()

# Step 4. 그룹 막대 차트 시각화
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=revenue_summary,
    x='bm_type',      # BM 타입
    y='annual_revenue_mil',      # 연평균 매출
    hue='platform',    # 플랫폼별 색상 구분
    ax=ax,
)

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}M'))
ax.set_title('BM 타입 및 플랫폼별 연평균 매출 비교', fontsize=14, fontweight='bold')
ax.set_xlabel('비즈니스 모델(BM Type)')
ax.set_ylabel('연평균 매출액')
ax.legend(title='플랫폼', loc='upper right')  # 범례 위치를 겹치지 않는 곳으로 지정
plt.tight_layout()
save_chart(fig, '01_bm_platform_revenue_bar.png')
plt.show()

"""
    [비즈니스 인사이트 도출 질의]
    Q1. 어떤 BM 타입 x 플랫폼 조합이 연평균 매출이 가장 높으며、
        신작이 이 조합을 채택했을 때 기대할 수 있는 매출 규모는 어느 정도인가?
"""


# ================================================================================
# [과제 2] CCU 대비 연간 매출 상관관계 분석 및 ARPU 이상치 식별 (Scatter Plot)
"""
    [비즈니스 문제 의도]
    동시 접속자(CCU)가 많다고 해서 반드시 매출이 높은 것은 아닙니다.
    "트래픽은 많지만 수익화가 안 되는" 게임과 "소수 정예 유저가 고액 소비하는"
    게임을 구분해야 신작의 BM 설계(무엇을, 누구에게, 얼마에 팔 것인가)가 방향을 잃지 않습니다.
    또한 논란으로 반짝 동접만 오르고 매출/평점이 무너지는 리스크 패턴도 미리 식별해야 합니다.

    [분석 및 시각화 힌트]
    - ARPU(유저당 매출) = annual_revenue_mil(단위: 백만 달러) * 1,000,000 / avg_ccu
    → 단위 변환에 주의하세요 (그냥 나누면 실제 달러 단위가 아닙니다).
    - 상관계수: df['avg_ccu'].corr(df['annual_revenue_mil'])
    - 시각화: sns.scatterplot(data=, x=, y=, hue='game_title', size='arpu', sizes=(40, 400))
    - 이상치 라벨: df.nlargest(n, 'arpu') 로 상위 n개 찾아 ax.annotate()
"""

# Step 1. 유저당 매출(ARPU, $) 계산
df['arpu'] = (df['annual_revenue_mil'] * 1_000_000) / df['avg_ccu']

# Step 2. CCU-매출 상관계수 확인
corr_value = df['avg_ccu'].corr(df['annual_revenue_mil'])
print(f'동접자 수-매출 상관계수: {corr_value:.3f}')

# Step 3. 산점도 시각화 (게임별 색상, ARPU는 버블 크기로 표현)
fig, ax = plt.subplots(figsize=(11, 7))
sns.scatterplot(
    data=df,
    x='avg_ccu',      # 연평균 동시접속자 수
    y='annual_revenue_mil',      # 연간 매출액
    hue='game_title',    # 게임별 색상 구분
    size='arpu',   # ARPU를 버블 크기로 표현
    sizes=(40, 400),
    alpha=0.75,
    ax=ax,
)

ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}M'))
ax.set_title('동시접속자 수 vs 연간 매출 (버블 크기 = ARPU)', fontsize=14, fontweight='bold')
ax.set_xlabel('연평균 동시접속자 수(CCU)')
ax.set_ylabel('연간 매출액')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8, title='게임')

# Step 4. ARPU 상위 이상치 라벨링
top_outliers = df.nlargest(2, 'arpu')
for _, row in top_outliers.iterrows():
    ax.annotate(
        f"{row['game_title']} ({row['year']})",
        xy=(row['avg_ccu'], row['annual_revenue_mil']),
        xytext=(10, 10), textcoords='offset points', fontsize=8,
    )

plt.tight_layout()
save_chart(fig, '02_ccu_revenue_scatter.png')
plt.show()

"""
    [비즈니스 인사이트 도출 질의]
    Q2. 동접자 수와 매출은 어느 정도 상관관계를 보이며、
        ARPU가 비정상적으로 높거나 낮은 이상치 게임/연도는 무엇인가?
        이것이 신작의 수익화(BM) 설계에 주는 시사점은 무엇인가?
"""

# ================================================================================
# [과제 3] 핵심 비교 대상 4종 유저 평점 및 부정 리뷰 비율 분포 비교 (Box Plot)
"""
    [비즈니스 문제 의도]
    우리 신작과 장르/포지셔닝이 가장 유사한 핵심 경쟁작
    4종(Overwatch 2, Valorant, Rainbow Six Siege, Delta Force)에 대해서는 단순 평균이 아니라 "연도별 변동성"까지 봐야 합니다.
    평점이 꾸준히 안정적인 게임과 특정 연도에 급락 리스크가 있는 게임을 구분해야
    신작의 라이브서비스 리스크 관리 전략을 세울 수 있습니다.

    [분석 및 시각화 힌트]
    - 필터링: df['game_title'].isin([...])
    - 시각화: sns.boxplot(data=, x='game_title', y=, hue='game_title')
    - 평점/부정리뷰율 2개 차트를 나란히: plt.subplots(1, 2, figsize=(14, 6))
    - x축 라벨이 길 경우: ax.tick_params(axis='x', rotation=15)
"""

CORE_GAMES = ['Overwatch 2', 'Valorant', 'Rainbow Six Siege', 'Delta Force']

# Step 1. 핵심 비교 대상 4종만 필터링
df_core = df[df['game_title'].isin(CORE_GAMES)]

# Step 2. 박스플롯 2개(평점 / 부정리뷰율)를 나란히 시각화
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.boxplot(
    data=df_core,
    x='game_title',
    y='user_rating_pct',       # 유저 긍정 평점
    hue='game_title',
    legend=False,
    ax=axes[0],
)
axes[0].set_title('핵심 경쟁작 4종 - 유저 긍정 평점 분포', fontweight='bold')
axes[0].set_xlabel('')
axes[0].set_ylabel('유저 긍정 평점(%)')
axes[0].tick_params(axis='x', rotation=15)

sns.boxplot(
    data=df_core,
    x='game_title',
    y='negative_review_rate',       # 부정 리뷰/이탈 위험률
    hue='game_title',
    legend=False,
    ax=axes[1],
)
axes[1].set_title('핵심 경쟁작 4종 - 부정 리뷰/이탈 위험률 분포', fontweight='bold')
axes[1].set_xlabel('')
axes[1].set_ylabel('부정 리뷰율(%)')
axes[1].tick_params(axis='x', rotation=15)

plt.tight_layout()
save_chart(fig, '03_core4_rating_negrate_box.png')
plt.show()

"""
    [비즈니스 인사이트 도출 질의]
    Q3. 핵심 경쟁작 4종 중 유저 평점이 가장 안정적인(변동폭이 작은) 게임과
        가장 불안정한(리스크가 큰) 게임은 각각 무엇이며、
        이는 신작의 장기 라이브서비스 운영 전략에 어떤 시사점을 주는가?
"""

# ================================================================================
# [과제 4] 플랫폼 x BM타입별 매출 쏠림 히트맵 또는 10종 연도별 동접 추세선
        # (택 1, 시간이 되면 둘 다 완성해 보세요)

"""
    [비즈니스 문제 의도]
        (A) 히트맵: 신작의 플랫폼 전략(PC전용 / Console전용 / Crossplay)과 BM 설계가
            "어디에 매출이 쏠려 있는지" 한눈에 보여줘야 자원을 어디에 집중할지 결정할 수 있습니다.
        (B) 추세선: 장기적으로 어떤 경쟁작이 유저 트래픽(CCU)을 잃고 있고
            어떤 게임이 성장하고 있는지 흐름을 봐야 신작의 출시 타이밍과
            포지셔닝(누구의 유저를 빼앗아 올 것인가)을 결정할 수 있습니다.

    [분석 및 시각화 힌트]
        (A) 피벗: df.pivot_table(index='platform',
                                columns='bm_type',
                                values='annual_revenue_mil',
                                aggfunc='mean')
            시각화: sns.heatmap(data=, annot=True, fmt=',.0f', cmap='YlOrRd', cbar_kws={'label': ...})
        (B) 시각화: sns.lineplot(data=df, x='year', y='avg_ccu', hue='game_title', marker='o')
            x축 눈금: ax.set_xticks(YEARS)
"""

# Step 1. 피벗 테이블 생성 (플랫폼 x BM타입별 평균 매출)
pivot_revenue = df.pivot_table(
    index='platform',
    columns='bm_type',
    values='annual_revenue_mil',
    aggfunc='mean',
)

# Step 2. 히트맵 시각화
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    pivot_revenue,
    annot=True,
    fmt=',.0f',
    cmap='YlOrRd',  # 오류 수정: 'YlorRd'는 존재하지 않는 컬러맵 이름(대소문자 오타) → 'YlOrRd'로 수정
    cbar_kws={'label': '연평균 매출액($M)'},
    ax=ax,
)
ax.set_title('플랫폼 x BM타입별 연평균 매출 쏠림', fontsize=14, fontweight='bold')
plt.tight_layout()
save_chart(fig, '04a_platform_bm_heatmap.png')
plt.show()

fig, ax = plt.subplots(figsize=(12, 7))
sns.lineplot(
    data=df,
    x='year',      # 연도
    y='avg_ccu',      # 연평균 동시접속자 수
    hue='game_title',    # 게임별 구분
    marker='o',
    ax=ax,
)

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.set_xticks(YEARS)
ax.set_title('경쟁작 10종 연도별 동시접속자 추세', fontsize=14, fontweight='bold')
ax.set_xlabel('연도')
ax.set_ylabel('연평균 동시접속자 수(CCU)')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8, title='게임')

plt.tight_layout()
save_chart(fig, '04b_ccu_trend_line.png')
plt.show()

"""
    [비즈니스 인사이트 도출 질의]
        Q4-A. 어떤 플랫폼 x BM타입 조합에 매출이 가장 쏠려 있으며、
              신작이 초기 자원을 우선 투입해야 할 조합은 무엇인가?
        Q4-B. 최근 5년간 동접자 수가 가장 가파르게 성장한 게임과 감소한 게임은 각각 무엇이며、
              이 흐름이 신작의 출시 타이밍/포지셔닝에 주는 시사점은 무엇인가?
"""


# ================================================================================
# [대시보드] 과제 1~4 통합 뷰 (경영진 보고용 2x2 보드)
# ================================================================================
from matplotlib.patches import Rectangle

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('신작 FPS 경쟁작 시장 데이터 분석 보드', fontsize=18, fontweight='bold', y=0.98)

# (1) BM타입 x 플랫폼별 연평균 매출 (Bar)
ax = axes[0, 0]
sns.barplot(data=revenue_summary, x='bm_type', y='annual_revenue_mil', hue='platform', ax=ax)
for container in ax.containers:
    ax.bar_label(container, fmt='$%.0fM', fontsize=8, padding=2)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}M'))
ax.set_title('[BM 전략 검토] BM타입 x 플랫폼별 연평균 매출', fontsize=11, fontweight='bold')
ax.set_xlabel('비즈니스 모델(BM Type)')
ax.set_ylabel('연평균 매출액')
ax.legend(title='플랫폼', fontsize=8, title_fontsize=9, loc='upper right')

# (2) CCU 대비 매출 산점도 + ARPU 이상치 (Scatter)
ax = axes[0, 1]
sns.scatterplot(data=df, x='avg_ccu', y='annual_revenue_mil', hue='game_title',
                 alpha=0.75, s=60, ax=ax, legend=False)
for _, row in df.nlargest(2, 'arpu').iterrows():
    ax.annotate(f"{row['game_title']} ({row['year']})",
                xy=(row['avg_ccu'], row['annual_revenue_mil']),
                xytext=(8, 8), textcoords='offset points', fontsize=7)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}M'))
ax.set_title('[리스크 식별] CCU 대비 매출 및 ARPU 이상치', fontsize=11, fontweight='bold')
ax.set_xlabel('연평균 동시접속자 수(CCU)')
ax.set_ylabel('연간 매출액')

# (3) 핵심 경쟁작 4종 평점/부정리뷰 분포 (Box)
ax = axes[1, 0]
df_core_melt = df_core.melt(
    id_vars='game_title',
    value_vars=['user_rating_pct', 'negative_review_rate'],
    var_name='metric', value_name='value',
)
df_core_melt['metric'] = df_core_melt['metric'].map({
    'user_rating_pct': '긍정 평점(%)',
    'negative_review_rate': '부정 리뷰율(%)',
})
sns.boxplot(data=df_core_melt, x='game_title', y='value', hue='metric', ax=ax)
ax.set_title('[리스크 식별] 핵심 경쟁작 4종 평점/부정리뷰 분포', fontsize=11, fontweight='bold')
ax.set_xlabel('')
ax.set_ylabel('비율(%)')
ax.tick_params(axis='x', rotation=15)
ax.legend(fontsize=8, loc='upper right', title=None)

# (4) 플랫폼 x BM타입별 매출 쏠림 (Heatmap)
ax = axes[1, 1]
sns.heatmap(pivot_revenue, annot=True, fmt=',.0f', cmap='YlOrRd',
            cbar_kws={'label': '연평균 매출액($M)'}, ax=ax)
ax.set_title('[자원 배분 검토] 플랫폼 x BM타입별 매출 쏠림', fontsize=11, fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.96])
fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                          fill=False, edgecolor='black', linewidth=3))

save_chart(fig, '00_dashboard_overview.png')
plt.show()