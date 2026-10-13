"""
    클래스와 객체
    
    《기본 형태》
    class 클래스명:
        # 생성자
        def __init__(self):
            self.필드명 = 값

        # 메소드
        def 메소드명(self):
            pass            # 실행할 내용
"""
print("=" * 50)
# 기본 형태
class Account:
    # 생성자
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance
    # 메소드
    def deposit(self, amount):
        self.balance += amount
        return self.balance
# 객체 생성
acc = Account("사용자", 10000)
print(f"owner: {acc.owner}")
print(f"balance: {acc.balance}")
print(f"deposit: {acc.deposit(7000)}")
# [TIP] print(acc) 를 했을 때 보기 좋게 출력하려면 __str__ 메소드를 정의한다 (02_method.py 하단 참고)
print("=" * 30)

# 인스턴스 변수 vs 클래스 변수
class Member:
    # 클래스 변수: 모든 인스턴스 공유
    team_name = "리센느"
    count = 0
    # 생성자 (정의)
    def __init__(self, name):
        self.name = name        # 인스턴스 변수
        Member.count += 1       # 클래스 변수는 클래스명으로 접근한다
m1 = Member("원이")
m2 = Member("미나미")
print(f"m1.name: {m1.name}")
print(f"m2.name: {m2.name}")
print(f"m1.team_name: {m1.team_name}")
print(f"m2.team_name: {m2.team_name}")
print(f"count: {Member.count}")
m1.team_name = "RESCENE"        # 인스턴스에 클래스 변수명으로 값을 대입하는 경우、새로운 인스턴스 변수를 생성한다
print(f"m1.team_name: {m1.team_name}")
print(f"Member.team_name: {Member.team_name}")
                                # 클래스 변수 자체는 변경되지 않는다
Member.team_name = "rescene"
print(f"Member.team_name: {Member.team_name}")
print("=" * 30)


# ======================================================================
# [실무 TIP] @dataclass - 데이터를 담는 클래스를 간단하게
# __init__, __repr__, __eq__ 를 자동으로 만들어주기 때문에 DTO, 설정값처럼 '데이터 묶음' 클래스에 많이 사용한다
# ======================================================================
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: int
    tags: list[str] = field(default_factory=list)    # 가변 기본값은 default_factory 로 지정

p1 = Product("아메리카노", 4500)
p2 = Product("아메리카노", 4500)
print(p1)                               # Product(name='아메리카노', price=4500, tags=[])
print(f"p1 == p2 : {p1 == p2}")          # 값이 같으면 True (__eq__ 자동 생성)
