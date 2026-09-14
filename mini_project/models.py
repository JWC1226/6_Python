"""
models.py
---------
고객(Customer) 도메인 모델과 커스텀 예외 클래스를 정의하는 모듈입니다.

- 예외 클래스: DuplicateContactError, CustomerNotFoundError
- 클래스 계층: Customer(부모) -> NormalCustomer, VIPCustomer(자식)
"""


# =========================================================
# 1. 커스텀 예외 클래스
# =========================================================

class DuplicateContactError(Exception):
    """이미 등록된 연락처로 신규 등록/수정을 시도할 때 발생시키는 예외입니다."""
    pass


class CustomerNotFoundError(Exception):
    """존재하지 않는 고객 ID로 조회/수정/삭제를 시도할 때 발생시키는 예외입니다."""
    pass


# =========================================================
# 2. 고객 모델 클래스 (부모 클래스)
# =========================================================

class Customer:
    """
    모든 고객 유형이 공통으로 가지는 속성과 동작을 정의하는 부모 클래스입니다.
    NormalCustomer, VIPCustomer는 이 클래스를 상속받아 세부 동작(포인트 적립률 등)만 다르게 구현합니다.
    """

    def __init__(self, customer_id, name, contact, points=0):
        self.customer_id = customer_id  # 고객을 구분하는 고유 ID (정수)
        self.name = name                # 고객 이름
        self.contact = contact          # 연락처 (중복 등록 방지 대상)
        self.points = points            # 누적 포인트 (기본값 0)

    def add_purchase(self, amount):
        """
        구매 금액(amount)을 입력받아 포인트를 적립하는 메서드입니다.
        실제 적립률은 등급별로 다르므로, 자식 클래스에서 반드시 오버라이딩해야 합니다.
        """
        raise NotImplementedError("자식 클래스에서 add_purchase()를 구현해야 합니다.")

    def is_vip(self):
        """VIP 여부를 반환합니다. 기본 Customer는 False이며, VIPCustomer에서 True로 오버라이딩합니다."""
        return False

    def __str__(self):
        """모든 고객 클래스가 공통으로 사용할 기본 출력 포맷입니다."""
        return f"[ID:{self.customer_id}] {self.name} | 연락처: {self.contact} | 누적 포인트: {self.points}점"


# =========================================================
# 3. 일반 고객 클래스 (자식 클래스)
# =========================================================

class NormalCustomer(Customer):
    """일반 고객: 구매 금액의 1%를 포인트로 적립합니다."""

    POINT_RATE = 0.01  # 일반 고객 포인트 적립률 (1%)

    def add_purchase(self, amount):
        earned = int(amount * self.POINT_RATE)  # 적립 포인트는 정수 단위로 계산
        self.points += earned
        return earned

    def __str__(self):
        # 부모의 공통 포맷을 재사용하고, 등급 표시만 추가합니다.
        return f"{super().__str__()} | 등급: 일반"


# =========================================================
# 4. VIP 고객 클래스 (자식 클래스)
# =========================================================

class VIPCustomer(Customer):
    """VIP 고객: 구매 금액의 5%를 포인트로 적립하며, 전담 매니저 이름을 가질 수 있습니다."""

    POINT_RATE = 0.05  # VIP 고객 포인트 적립률 (5%)

    def __init__(self, customer_id, name, contact, points=0, manager_name=None):
        super().__init__(customer_id, name, contact, points)
        self.manager_name = manager_name  # 전담 매니저 이름 (없을 수도 있으므로 기본값 None)

    def add_purchase(self, amount):
        earned = int(amount * self.POINT_RATE)
        self.points += earned
        return earned

    def is_vip(self):
        return True

    def __str__(self):
        manager_info = self.manager_name if self.manager_name else "미배정"
        return f"{super().__str__()} | 등급: VIP | 전담 매니저: {manager_info}"
