"""
    Method: 클래스 내의 함수
    
    《종류》
    ・인스턴스 메소드
    ・클래스 메소드     (@classmethod)
    ・정적 메소드      (@staticmethod)
"""
print("=" * 50)
class Account:
    bank_name = "KH 은행"
    MIN_DEPOSIT = 1000      # 상수 처리를 할 때、대문자로 작성한다
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance

    # 인스턴스 메소드: 객체의 데이터를 다루는 메소드 / 첫 번째 매개변수가 self
    def deposit(self, amount):
        self.balance += amount
        return self.balance

    # 클래스 메소드: 클래스 자체를 다루는 메소드 / 첫 번째 매개변수가 cls / @classmethod 지정
    @classmethod
    def from_dict(cls, data):
        """
            딕셔너리로부터 객체를 생성하는 메소드이다
        """
        return cls(data["owner"], data.get("balance", 0))

    # 정적 메소드: 객체나 클래스와 무관한 기능을 담당하는 메소드 / 유틸리티 역할을 갖는다 / @staticmethod 지정
    @staticmethod
    def is_valid_amount(amount):
        return amount >= Account.MIN_DEPOSIT
    # [TIP] 클래스 변수를 사용하는 기능은 @classmethod 로 만들고 cls.MIN_DEPOSIT 로 접근하면, 상속했을 때 자식 클래스의 값을 따라간다
    
acc = Account("사용자", 10000)
print(f"deposit >> {acc.deposit(3000)}")
                        # 인스턴스 메소드 호출

    # 클래스 메소드 호출
acc2 = Account.from_dict({"owner": "사용자", "balance": 10000})
print(f"owner: {acc2.owner}, balance: {acc2.balance}")

    # 정적 메소드 호출
print(f"amount: 6000 > {Account.is_valid_amount(6000)}")
print(f"amount: 500 > {Account.is_valid_amount(500)}")
amount = 500            # 변수에 금액을 담아서 검증과 입금에 동일하게 사용합니다. (Ai ErrorCode Edit)
if Account.is_valid_amount(amount):
    print(f"deposit >> {acc2.deposit(amount)}")
else:
    print(f"최소 금액을 만족하지 않습니다")

# from_dict 활용
response = [
    {"owner": "사용자", "balance": 20000},
    {"owner": "이용자"},
    {"owner": "관리자", "balance": 55000}
]
accounts = [Account.from_dict(item) for item in response]
for a in accounts:
    print(f"{a.owner} {a.balance}원")
# from_dict 를 활용하면 딕셔너리 구조를 자연스럽게 클래스에 넘겨서 객체를 생성할 수 있다
# 데이터 구조가 변경되거나 메소드를 수정하는 경우、새로 정의해서 대응이 가능하다
print("=" * 30)


# ======================================================================
# [실무 TIP] 특수 메소드(매직 메소드) - __str__ / __repr__ / __eq__
# __str__ 은 print() 용(사용자용), __repr__ 은 디버깅용(개발자용)이며 리스트를 print 하면 각 요소의 __repr__ 이 사용된다
# ======================================================================
class Coin:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def __str__(self):
        return f"{self.name} {self.price:,}원"
    def __repr__(self):
        return f"Coin({self.name!r}, {self.price})"
    def __eq__(self, other):
        return isinstance(other, Coin) and self.name == other.name

c = Coin("BTC", 150_000_000)
print(c)                                # __str__
print([c])                              # [Coin('BTC', 150000000)] → __repr__
print(c == Coin("BTC", 1))              # __eq__ → 이름이 같으면 같은 코인으로 판단
