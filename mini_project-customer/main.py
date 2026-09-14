"""
main.py
-------
고객 관리 시스템(CRM)의 실행 진입점입니다.
while 루프 기반의 대화형 콘솔 메뉴를 제공하며, 실제 로직은 CRMManager에 위임합니다.
"""

from models import NormalCustomer, VIPCustomer, DuplicateContactError, CustomerNotFoundError
from crm_manager import CRMManager


def print_menu():
    """메인 메뉴를 출력합니다."""
    print("\n===== 고객 관리 시스템 (CRM) =====")
    print("1. 고객 등록")
    print("2. 전체 고객 조회")
    print("3. VIP 고객 조회")
    print("4. 특정 포인트 이상 고객 검색")
    print("5. 고객 상세 조회 (ID)")
    print("6. 고객 정보 수정 (이름/연락처/등급/매니저)")
    print("7. 상품 구매 (포인트 적립)")
    print("8. 고객 탈퇴")
    print("9. 종료")
    print("===================================")


def print_customer_list(customers):
    """고객 리스트를 보기 좋게 출력하는 공통 함수입니다."""
    if not customers:
        print("- 표시할 고객이 없습니다.")
        return
    for customer in customers:
        print(f"- {customer}")  # Customer.__str__()이 자동으로 호출됩니다.


def handle_register(manager):
    """1. 고객 등록 처리"""
    print("\n[고객 등록] 등록할 고객 유형을 선택하세요.")
    print("1) 일반 고객   2) VIP 고객")
    grade = input("선택: ").strip()

    name = input("이름: ").strip()
    contact = input("연락처 (예: 010-1234-5678): ").strip()

    try:
        if grade == "1":
            new_customer = NormalCustomer(customer_id=None, name=name, contact=contact)
        elif grade == "2":
            manager_name = input("전담 매니저 이름 (없으면 엔터): ").strip()
            manager_name = manager_name if manager_name else None
            new_customer = VIPCustomer(customer_id=None, name=name, contact=contact, manager_name=manager_name)
        else:
            print("잘못된 선택입니다. 등록을 취소합니다.")
            return

        registered = manager.register_customer(new_customer)
        print(f"등록 완료: {registered}")

    except (DuplicateContactError, ValueError) as e:
        print(f"[오류] {e}")


def handle_view_all(manager):
    """2. 전체 고객 조회 처리"""
    print("\n[전체 고객 목록]")
    print_customer_list(manager.get_all_customers())


def handle_view_vip(manager):
    """3. VIP 고객 조회 처리"""
    print("\n[VIP 고객 목록]")
    print_customer_list(manager.get_vip_customers())


def handle_search_by_points(manager):
    """4. 특정 포인트 이상 고객 검색 처리"""
    try:
        min_points = int(input("검색 기준 포인트(이상): ").strip())
    except ValueError:
        print("[오류] 숫자를 입력해야 합니다.")
        return

    try:
        results = manager.find_by_min_points(min_points)
    except ValueError as e:
        print(f"[오류] {e}")
        return

    print(f"\n[{min_points}점 이상 보유 고객 목록]")
    print_customer_list(results)


def handle_view_detail(manager):
    """5. 고객 상세 조회(ID) 처리"""
    try:
        customer_id = int(input("조회할 고객 ID: ").strip())
    except ValueError:
        print("[오류] ID는 숫자로 입력해야 합니다.")
        return

    try:
        customer = manager.get_customer_by_id(customer_id)
        print(f"\n[고객 상세 정보]\n- {customer}")
    except CustomerNotFoundError as e:
        print(f"[오류] {e}")


def handle_update_info(manager):
    """6. 고객 정보 수정 처리 (이름 / 연락처 / 등급 전환 / VIP 매니저)"""
    print("\n[고객 정보 수정] 수정할 항목을 선택하세요.")
    print("1) 이름 수정   2) 연락처 수정   3) 등급 전환(일반<->VIP)   4) VIP 담당 매니저 변경")
    sub_choice = input("선택: ").strip()

    try:
        customer_id = int(input("대상 고객 ID: ").strip())
    except ValueError:
        print("[오류] ID는 숫자로 입력해야 합니다.")
        return

    try:
        if sub_choice == "1":
            new_name = input("새 이름: ").strip()
            updated = manager.update_name(customer_id, new_name)
            print(f"수정 완료: {updated}")

        elif sub_choice == "2":
            new_contact = input("새 연락처 (예: 010-1234-5678): ").strip()
            updated = manager.update_contact(customer_id, new_contact)
            print(f"수정 완료: {updated}")

        elif sub_choice == "3":
            print("전환할 등급을 선택하세요. 1) 일반 고객   2) VIP 고객")
            grade_choice = input("선택: ").strip()
            if grade_choice == "2":
                manager_name = input("전담 매니저 이름 (없으면 엔터): ").strip()
                manager_name = manager_name if manager_name else None
                updated = manager.change_grade(customer_id, "vip", manager_name)
            elif grade_choice == "1":
                updated = manager.change_grade(customer_id, "normal")
            else:
                print("잘못된 선택입니다. 등급 전환을 취소합니다.")
                return
            print(f"등급 전환 완료: {updated}")

        elif sub_choice == "4":
            new_manager_name = input("새 담당 매니저 이름: ").strip()
            updated = manager.update_manager(customer_id, new_manager_name)
            print(f"수정 완료: {updated}")

        else:
            print("잘못된 선택입니다.")

    except (CustomerNotFoundError, DuplicateContactError, ValueError) as e:
        print(f"[오류] {e}")


def handle_purchase(manager):
    """7. 상품 구매 처리"""
    try:
        customer_id = int(input("구매 고객 ID: ").strip())
        amount = int(input("구매 금액: ").strip())
    except ValueError:
        print("[오류] ID와 구매 금액은 숫자로 입력해야 합니다.")
        return

    try:
        earned = manager.purchase(customer_id, amount)
        print(f"구매 완료! {earned}점이 적립되었습니다.")
    except (CustomerNotFoundError, ValueError) as e:
        print(f"[오류] {e}")


def handle_withdraw(manager):
    """8. 고객 탈퇴 처리"""
    try:
        customer_id = int(input("탈퇴할 고객 ID: ").strip())
    except ValueError:
        print("[오류] ID는 숫자로 입력해야 합니다.")
        return

    try:
        removed = manager.withdraw_customer(customer_id)
        print(f"탈퇴 처리 완료: {removed}")
    except CustomerNotFoundError as e:
        print(f"[오류] {e}")


def main():
    """프로그램 진입점: while 루프로 메뉴를 반복 실행합니다."""
    manager = CRMManager()

    while True:
        print_menu()
        choice = input("메뉴 번호 선택: ").strip()

        if choice == "1":
            handle_register(manager)
        elif choice == "2":
            handle_view_all(manager)
        elif choice == "3":
            handle_view_vip(manager)
        elif choice == "4":
            handle_search_by_points(manager)
        elif choice == "5":
            handle_view_detail(manager)
        elif choice == "6":
            handle_update_info(manager)
        elif choice == "7":
            handle_purchase(manager)
        elif choice == "8":
            handle_withdraw(manager)
        elif choice == "9":
            print("프로그램을 종료합니다.")
            break
        else:
            print("[오류] 1~9 사이의 번호를 입력해주세요.")


if __name__ == "__main__":
    main()
