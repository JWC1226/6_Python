"""
    《캡슐화》
    클래스 내부의 데이터를 임의로 접근할 수 없게 하고 (정보 은닉)
    데이터와 처리 메소드를 모아서 관리한다 (데이터와 기능의 결합)

    ・인스턴스 변수명 앞에 언더바를 추가하여、"접근하지 말자" (관례)
    ・@property, @필드명.setter를 통해 getter/setter를 정의한다
"""
print("=" * 55)

# 네이밍 규칙 (_필드명 / __필드명) > Python에서는 private가 없다 !
class Account:
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self._bank_code = "005"
        self.__balance = balance                # 네임맹글링 적용됨
acc = Account("관리자", 10000)
print(f"owner: {acc.owner}")
print(f"_bank_code: {acc._bank_code}")          # Error X | 접근은 가능하지만、직접 접근하지 말 것!
# print(f"__balance: {acc.__balance}")          # Error O | 접근 불가
print(f"본명: {[k for k in vars(acc)]}")
print(f"_Account__balance: {acc._Account__balance}")
    # 네임맹글링 (name mangLing)
        # `__필드명` 형태의 변수는 `_클래스명_필드명` 형태로 변환되어 직접 접근을 차단한다
        # 변환된 이름으로는 접근이 가능하지만、사용을 권장하지 않는다 !
print("=" * 50)

# @property: 메소드를 속성(필드)처럼 사용하게 해주는 데코레이터
class SafeAccount:
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.__balance = balance
    # `__balance`의 getter
    @property
    def balance(self):
        """getter"""
        return self.__balance

    # `__balance`의 setter
    @balance.setter
    def balance(self, value):
        """setter"""
        if value < 0:
            self.__balance = 0
            return                  # return 뒤에 값을 넣지 않으면 그냥 종료
        self.__balance = value
    @property
    def info(self):
        return f"{self.owner}:{self.__balance:,}원"
    
sa = SafeAccount("문서", 500000)
print(f"sa.balance: {sa.balance}")  # getter
sa.balance = 1000000                # setter
print(f"sa.balance: {sa.balance}")
# sa.balance = -9999
# print(f"sa.balance: {sa.balance}")
print(f"sa.info: {sa.info}")
print("=" * 50)