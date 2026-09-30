# TODO 1. pandas를 사용하여 train.csv 파일 데이터를 불러와 DataFrame으로 저장하십시오.
import pandas as pd

df = pd.read_csv('train.csv')

# TODO 2. 저장된 데이터에서 상위 5개의 행을 출력하시오
print(df.head())

# TODO 3. 각 열의 이름, 결측치 여부, 데이터 타입(dtype)을 한 번에 확인하시오
    # df.info()를 실행한 후 출력 결과를 바탕으로 다음을 기술하시오
        # 결측치가 존재하는 열과 결측 개수
        # dtype이 예상과 다르거나 주의가 필요한 열
df.info()
    # 결측치 존재 열: Age 177개, Cabin 687개, Embarked 2개
    # dtype 주의 열: Name/Sex/Ticket/Cabin/Embarked는 str형, Pclass는 int형이지만 실제로는 범주형(등급)으로 다뤄야 함

# TODO 4. Age(나이), Fare(요금) 열의 평균값, 최소값, 최대값을 구하시오
print("Age - 평균:", df['Age'].mean(), "최소:", df['Age'].min(), "최대:", df['Age'].max())
print("Fare - 평균:", df['Fare'].mean(), "최소:", df['Fare'].min(), "최대:", df['Fare'].max())

# TODO 5. 탑승객 중 생존자와 사망자가 각각 몇 명인지 계산하시오
    # 생존자: Survived=1 / 사망자: Survived=0
survived_count = (df['Survived'] == 1).sum()
dead_count = (df['Survived'] == 0).sum()
print("생존자 수:", survived_count, "사망자 수:", dead_count)

# TODO 6. 객실 등급(Pclass)별로 탑승객이 몇 명인지 계산하시오
print(df.groupby('Pclass').size())

# TODO 7. 나이가 50세 이상인 탑승객만 추출하여 새로운 데이터 프레임을 만드시오
elderly_df = df[df['Age'] >= 50]

# TODO 8. 탑승객을 나이대 기준으로 그룹화하여 새로운 열 AgeGroup을 추가한 후, 상위 5개 행을 확인하시오
    # 나이대 구분 기준
    # | 나이 범위 | AgeGroup값 |
    # | 0세 이상 ~ 10세 미만 | '아동' |
    # | 10세 이상 ~ 20세 미만 | '10대' |
    # | 20세 이상 ~ 30세 미만 | '20대' |
    # | 30세 이상 ~ 40세 미만 | '30대' |
    # | 40세 이상 ~ 50세 미만 | '40대' |
    # | 50세 이상 ~ 60세 미만 | '50대' |
    # | 60세 이상 | '60대 이상' |
    # | 결측치(NaN) | '미확인' |
        # pd.cut() 또는 조건식(if-else/np.where)을 자유롭게 사용해도 됩니다
def get_age_group(age):
    # 결측치는 나이대를 판단할 수 없으므로 '미확인'으로 우선 처리
    if pd.isna(age):
        return '미확인'
    elif age < 10:
        return '아동'
    elif age < 20:
        return '10대'
    elif age < 30:
        return '20대'
    elif age < 40:
        return '30대'
    elif age < 50:
        return '40대'
    elif age < 60:
        return '50대'
    else:
        return '60대 이상'

df['AgeGroup'] = df['Age'].apply(get_age_group)
print(df.head())

# TODO 9. 성별(Sex)과 객실 등급(Pclass)을 기준으로 그룹화하여 각각의 평균 생존율을 계산하시오
print(df.groupby('Sex')['Survived'].mean())
print(df.groupby('Pclass')['Survived'].mean())

# TODO 10. 나이대별 평균 생존율을 계산하시오
    # 8번에서 생성한 AgeGroup 열을 기준으로 그룹화하여 계산하시오
print(df.groupby('AgeGroup')['Survived'].mean())

# TODO 11. 각 열에 존재하는 결측치(NaN)의 총 개수와 전체 데이터 대비 비율을 계산하여 내림차순으로 출력하시오
missing_count = df.isnull().sum()
missing_ratio = missing_count / len(df) * 100
missing_df = pd.DataFrame({'결측치 개수': missing_count, '결측치 비율(%)': missing_ratio})
print(missing_df.sort_values(by='결측치 개수', ascending=False))

# TODO 12. Sex 열의 'male'은 0으로, 'female'은 1로 변경하여 Gender_Encoded라는 새로운 열을 추가하시오
    # map(), replace(), apply()중 편한 방식을 사용해도 됩니다
df['Gender_Encoded'] = df['Sex'].map({'male': 0, 'female': 1})

# TODO 13. 탑승지(Embarked)별로 승객이 지불한 요금(Fare)의 평균을 계산하시오
print(df.groupby('Embarked')['Fare'].mean())

# TODO 14. Pclass를 인덱스로 Sex를 컬럼으로 값으로 Fare의 평균을 사용하여 피벗 테이블을 생성하시오
pivot = df.pivot_table(index='Pclass', columns='Sex', values='Fare')

# TODO 15. SibSp(형제/배우자 수)와 Parch(부모/자녀 수)를 합산하여 FamilySize 열을 추가하고, 이 열의 요약 통계를 확인하세요
df['FamilySize'] = df['SibSp'] + df['Parch']
print(df['FamilySize'].describe())

# TODO 16. Name 열에서 호칭(Mr.,Mrs.Miss.,Master. 등)을 정규 표현식 or 문자열 함수를 추출하고 Title이라는 새로운 열을 생성한 뒤, 가장 흔한 5개의 호칭을 출력하시오
    # 정규 표현식 예시: r', ([A-Za-z]+)\.' = 성(Last name)뒤에 오는 호칭을 추출한다
df['Title'] = df['Name'].str.extract(r', ([A-Za-z]+)\.')
print(df['Title'].value_counts().head())

# TODO 17. 16번에서 생성한 Title열을 기준으로 그룹화하여, 각 호칭별 승객 수, 평균 나이, 평균 생존율을 한 번에 계산하시오
    # groupby().agg()의 Named Aggregation을 활용하면 집계 결과 열 이름을 직접 지정할 수 있다
title_stats = df.groupby('Title').agg(
    승객수=('PassengerId', 'count'),
    평균나이=('Age', 'mean'),
    평균생존율=('Survived', 'mean')
)
print(title_stats)

# TODO 18. 생존한 사람과 사망한 사람의 나이(Age) 분포를 비교할 수 있도록 시각화하시오
    # 히스토그램 or KDE(밀도) 플롯 중 하나를 사용하시오
    # 그래프에는 다음과 같은 요소를 반드시 포함하시오
        # 제목(set_title)
        # x축・y축 라벨(set_xlabel, set_ylabel)
        # 생존/사망 구분 범례(legend)
    # 결과를 화면에 출력하지 않고, **이미지 파일로 저장**하시오 (savefig 사용)
import matplotlib.pyplot as plt

# 한글 라벨이 깨지지 않도록 폰트를 지정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots()
ax.hist(df[df['Survived'] == 1]['Age'].dropna(), bins=20, alpha=0.5, label='생존')
ax.hist(df[df['Survived'] == 0]['Age'].dropna(), bins=20, alpha=0.5, label='사망')
ax.set_title('생존 여부에 따른 나이 분포')
ax.set_xlabel('나이')
ax.set_ylabel('인원 수')
ax.legend()
fig.savefig('age_distribution.png')

# TODO 19. 16번에서 추출한 Title과 Pclass를 동시에 고려하여 해당 그룹의 나이 중앙값으로 Age 열의 결측치를 대치하시오 (원본 프레임에 적용)
    # Ex. 'Master' 타이틀을 가진 1등급 승객 그룹의 나이 중앙값으로 해당 그룹의 결측치를 채운다
    # groupby().transform("median")을 활용하면 그룹별 중앙값을 원본과 같은 길이로 얻을 수 있다
    # ※ 이 문제는 반드시 **16번 완료 후** 진행하시오. Title 열이 존재해야 그룹 기준으로 사용할 수 있습니다.
df['Age'] = df['Age'].fillna(df.groupby(['Title', 'Pclass'])['Age'].transform('median'))

# TODO 20. Survived, Pclass, Age, SibSp, Parch, Fare 등의 수치형 변수들 간의 상관 관계 행렬을 계산하고, 그 결과를 히트맵(Heatmap)으로 시각화하시오
    # corr() : 상관관계 행렬 계산 함수
    # sns.heatmap(..., annot=True, cmap="coolwram", center=0) 형식으로 작성하면 값이 셀 안에 표시됩니다
    # 결과를 화면에 출력하지 않고 **이미지 파일로 저장**하시오 (savefig 사용)
import seaborn as sns

corr_matrix = df[['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare']].corr()

fig2, ax2 = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax2)
fig2.savefig('correlation_heatmap.png')