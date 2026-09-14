"""
crm_manager.py
--------------
CRMManager 클래스는 고객 데이터를 메모리(List)에 저장하고,
등록/조회/수정/구매/탈퇴 등의 비즈니스 로직을 처리합니다.

데이터는 self.customers 리스트에만 보관되며, 프로그램을 종료하면 사라집니다(요구사항 3번).
"""

import re

from models import DuplicateContactError, CustomerNotFoundError, NormalCustomer, VIPCustomer

# 연락처 형식 검증용 정규식 (예: 02-123-4567, 010-1234-5678 등 0으로 시작하는 국내 전화번호 패턴)
CONTACT_PATTERN = re.compile(r"^0\d{1,2}-\d{3,4}-\d{4}$")


class CRMManager:
    """고객 목록을 관리하는 CRM 관리자 클래스입니다."""

    def __init__(self):
        self.customers = []       # 고객 객체들을 저장하는 메모리 리스트
        self._next_id = 1         # 고객 ID 자동 증가를 위한 내부 카운터 (중복 ID 방지)

    # ---------------------------------------------------
    # 내부 헬퍼 메서드
    # ---------------------------------------------------

    def _is_duplicate_contact(self, contact, exclude_id=None):
        """
        주어진 연락처가 이미 등록되어 있는지 확인합니다.
        exclude_id를 지정하면 해당 ID의 고객은 검사 대상에서 제외합니다. (연락처 수정 시 자기 자신 제외용)
        """
        for customer in self.customers:
            if customer.contact == contact and customer.customer_id != exclude_id:
                return True
        return False

    def _find_by_id(self, customer_id):
        """ID로 고객을 찾아 반환합니다. 없으면 CustomerNotFoundError를 발생시킵니다."""
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        raise CustomerNotFoundError(f"ID {customer_id}에 해당하는 고객을 찾을 수 없습니다.")

    def _validate_contact_format(self, contact):
        """연락처가 '0xx-xxx(x)-xxxx' 형식의 전화번호인지 검사합니다. 아니면 ValueError를 발생시킵니다."""
        if not CONTACT_PATTERN.match(contact):
            raise ValueError(
                f"연락처 '{contact}'의 형식이 올바르지 않습니다. '010-1234-5678'과 같은 형식으로 입력해주세요."
            )

    # ---------------------------------------------------
    # 1) 고객 등록
    # ---------------------------------------------------

    def register_customer(self, customer):
        """
        고객 객체(NormalCustomer 또는 VIPCustomer)를 등록합니다.
        연락처 형식이 올바르지 않으면 ValueError를,
        연락처가 이미 등록되어 있으면 DuplicateContactError를 발생시킵니다.
        등록에 성공하면 등록된 고객 객체를 반환합니다.
        """
        self._validate_contact_format(customer.contact)

        if self._is_duplicate_contact(customer.contact):
            raise DuplicateContactError(f"연락처 '{customer.contact}'는 이미 등록되어 있습니다.")

        customer.customer_id = self._next_id  # 자동 증가 ID 부여
        self._next_id += 1
        self.customers.append(customer)
        return customer

    def get_customer_by_id(self, customer_id):
        """ID로 고객 한 명을 상세 조회합니다. 없으면 CustomerNotFoundError가 발생합니다."""
        return self._find_by_id(customer_id)

    # ---------------------------------------------------
    # 2) 전체 고객 조회
    # ---------------------------------------------------

    def get_all_customers(self):
        """등록된 모든 고객 리스트를 반환합니다."""
        return self.customers

    # ---------------------------------------------------
    # 3) VIP 고객만 조회
    # ---------------------------------------------------

    def get_vip_customers(self):
        """is_vip()가 True인 고객만 필터링하여 반환합니다."""
        return [customer for customer in self.customers if customer.is_vip()]

    # ---------------------------------------------------
    # 4) 특정 포인트 이상 보유 고객 검색
    # ---------------------------------------------------

    def find_by_min_points(self, min_points):
        """
        누적 포인트가 min_points 이상인 고객을 검색하여 반환합니다.
        min_points가 음수이면 ValueError를 발생시킵니다.
        """
        if min_points < 0:
            raise ValueError("검색 기준 포인트는 0 이상이어야 합니다.")
        return [customer for customer in self.customers if customer.points >= min_points]

    # ---------------------------------------------------
    # 5) 고객 연락처 수정
    # ---------------------------------------------------

    def update_contact(self, customer_id, new_contact):
        """
        ID로 고객을 찾아 연락처를 수정합니다.
        - 고객이 없으면 CustomerNotFoundError
        - 새 연락처 형식이 올바르지 않으면 ValueError
        - 새 연락처가 다른 고객과 중복되면 DuplicateContactError
        """
        customer = self._find_by_id(customer_id)  # 없으면 여기서 예외 발생

        self._validate_contact_format(new_contact)

        if self._is_duplicate_contact(new_contact, exclude_id=customer_id):
            raise DuplicateContactError(f"연락처 '{new_contact}'는 이미 다른 고객이 사용 중입니다.")

        customer.contact = new_contact
        return customer

    def update_name(self, customer_id, new_name):
        """
        ID로 고객을 찾아 이름을 수정합니다.
        - 고객이 없으면 CustomerNotFoundError
        - 이름이 비어 있으면 ValueError
        """
        customer = self._find_by_id(customer_id)

        if not new_name.strip():
            raise ValueError("이름은 빈 값일 수 없습니다.")

        customer.name = new_name
        return customer

    def change_grade(self, customer_id, new_grade, manager_name=None):
        """
        ID로 고객을 찾아 등급(일반 <-> VIP)을 전환합니다.
        내부적으로는 동일한 ID/이름/연락처/포인트를 유지한 채
        NormalCustomer <-> VIPCustomer 객체로 교체합니다.
        - 고객이 없으면 CustomerNotFoundError
        - new_grade가 'normal'/'vip'가 아니거나 이미 같은 등급이면 ValueError
        """
        customer = self._find_by_id(customer_id)

        if new_grade == "vip":
            if isinstance(customer, VIPCustomer):
                raise ValueError("이미 VIP 고객입니다.")
            new_customer = VIPCustomer(
                customer.customer_id, customer.name, customer.contact, customer.points, manager_name
            )
        elif new_grade == "normal":
            if isinstance(customer, NormalCustomer):
                raise ValueError("이미 일반 고객입니다.")
            new_customer = NormalCustomer(customer.customer_id, customer.name, customer.contact, customer.points)
        else:
            raise ValueError("등급은 'normal' 또는 'vip'만 가능합니다.")

        index = self.customers.index(customer)
        self.customers[index] = new_customer  # 같은 위치에 새 등급 객체로 교체
        return new_customer

    def update_manager(self, customer_id, new_manager_name):
        """
        VIP 고객의 담당 매니저 이름을 변경합니다.
        - 고객이 없으면 CustomerNotFoundError
        - VIP 고객이 아니면 ValueError
        """
        customer = self._find_by_id(customer_id)

        if not isinstance(customer, VIPCustomer):
            raise ValueError("VIP 고객만 담당 매니저를 지정할 수 있습니다. 먼저 등급을 VIP로 전환해주세요.")

        customer.manager_name = new_manager_name if new_manager_name else None
        return customer

    # ---------------------------------------------------
    # 6) 상품 구매 (포인트 적립)
    # ---------------------------------------------------

    def purchase(self, customer_id, amount):
        """
        ID로 고객을 찾아 구매 금액만큼 포인트를 적립합니다.
        - 고객이 없으면 CustomerNotFoundError
        - 구매 금액이 음수이면 ValueError
        적립된 포인트(int)를 반환합니다.
        """
        customer = self._find_by_id(customer_id)

        if amount < 0:
            raise ValueError("구매 금액은 0 이상이어야 합니다.")

        earned = customer.add_purchase(amount)  # 등급별 적립률은 각 클래스에서 처리
        return earned

    # ---------------------------------------------------
    # 7) 고객 탈퇴
    # ---------------------------------------------------

    def withdraw_customer(self, customer_id):
        """
        ID로 고객을 찾아 리스트에서 삭제합니다.
        고객이 없으면 CustomerNotFoundError가 발생합니다.
        """
        customer = self._find_by_id(customer_id)  # 존재 여부 확인 및 예외 처리
        self.customers.remove(customer)
        return customer
