"""
    대화형 콘솔 메뉴를 담당하며、사용자 입력에 따라 InventoryManager의 기능을 호출하고 예외를 처리합니다
"""
from datetime import date, datetime
from models import NormalProduct, FreshProduct, OutOfStockError, ProductNotFoundError
from inventory import InventoryManager

def print_menu() -> None:
    # 메인 메뉴를 출력합니다
    print("\n" + "=" * 50)
    print("          재고 관리 프로그램 (Inventory Manager)")
    print("=" * 50)
    print("1. 신규 상품 등록")
    print("2. 전체 재고 조회")
    print("3. 긴급 발주 목록 조회 (재고 10개 미만)")
    print("4. 전체 재고 총 금액 확인")
    print("5. 입고 처리")
    print("6. 출고 처리")
    print("7. 상품 단가 수정")
    print("8. 단종 품목 삭제")
    print("0. 종료")
    print("=" * 50)

def input_int(prompt: str, min_value: int | None = None) -> int:
    # 정수를 입력받아 반환한다
    # 숫자가 아니거나 min_value보다 작으면 다시 입력
    while True:
        raw = input(prompt).strip()

        try:
            value = int(raw)
        except ValueError:
            print("[오류] 숫자를 입력해 주세요")
            continue

        if min_value is not None and value < min_value:
            print(f"[오류] {min_value} 이상의 값을 입력해 주세요")
            continue
        return value

def input_date(prompt: str) -> date:
    # 'YYYY-MM-DD' 형식의 문자열을 입력받아 date로 변환한다
    # 형식이 올바르지 않으면 다시 입력받는다
    while True:
        raw = input(prompt).strip()

        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print("[오류] 날짜 형식이 올바르지 않습니다 Ex) 2026-09-20")

def add_product_flow(manager: InventoryManager) -> None:
    # '신규 상품 등록' 메뉴 처리 흐름
    print("\n[신규 상품 등록]")
    print("1) 일반 물품  2) 신선 식품")
    kind = input("등록할 상품 종류를 선택하세요: ").strip()
    code = input("상품 코드: ").strip()
    name = input("품명: ").strip()
    price = input_int("단가: ", min_value=0)
    stock = input_int("재고 수량: ", min_value=0)

    if kind == "1":
        hazardous_raw = input("위험물 여부 (y/n): ").strip().lower()
        is_hazardous = hazardous_raw == "y"
        product = NormalProduct(code, name, price, stock, is_hazardous)
    elif kind == "2":
        expiration_date = input_date("유통기한 (YYYY-MM-DD): ")
        product = FreshProduct(code, name, price, stock, expiration_date)
    else:
        print("[오류] 잘못된 상품 종류 선택입니다")
        return

    try:
        manager.add_product(product)
        print(f"[완료] 상품이 등록되었습니다 -> {product}")
    except ValueError as e:
        print(f"[오류] {e}")

def list_all_flow(manager: InventoryManager) -> None:
    # '전체 재고 조회' 메뉴 처리 흐름
    print("\n[전체 재고 목록]")
    products = manager.get_all_products()
    if not products:
        print("등록된 상품이 없습니다")
        return
    # 모든 상품 클래스가 __str__을 오버라이딩하므로 종류에 상관없이 동일한 형식으로 출력된다
    for product in products:
        print(product)

def urgent_reorder_flow(manager: InventoryManager) -> None:
    # '긴급 발주 목록 조회' 메뉴 처리 흐름
    print(f"\n[긴급 발주 목록] (재고 {InventoryManager.URGENT_REORDER_THRESHOLD}개 미만)")
    urgent_list = manager.get_urgent_reorder_list()
    if not urgent_list:
        print("긴급 발주가 필요한 상품이 없습니다")
        return
    for product in urgent_list:
        print(product)

def total_value_flow(manager: InventoryManager) -> None:
    # '전체 재고 총 금액 확인' 메뉴 처리 흐름
    total = manager.get_total_inventory_value()
    print(f"\n[전체 재고 총 금액] {total:,}원")

def stock_in_flow(manager: InventoryManager) -> None:
    # '입고 처리' 메뉴 처리 흐름
    code = input("\n입고할 상품 코드: ").strip()
    amount = input_int("입고 수량: ", min_value=1)
    try:
        product = manager.stock_in(code, amount)
        print(f"[완료] 입고 처리되었습니다 -> {product}")
    except ProductNotFoundError as e:
        print(f"[오류] {e}")
    except ValueError as e:
        print(f"[오류] {e}")

def stock_out_flow(manager: InventoryManager) -> None:
    # '출고 처리' 메뉴 처리 흐름
    code = input("\n출고할 상품 코드: ").strip()
    amount = input_int("출고 수량: ", min_value=1)
    try:
        product = manager.stock_out(code, amount)
        print(f"[완료] 출고 처리되었습니다 -> {product}")
    except ProductNotFoundError as e:
        print(f"[오류] {e}")
    except OutOfStockError as e:
        print(f"[오류] {e}")
    except ValueError as e:
        print(f"[오류] {e}")

def update_price_flow(manager: InventoryManager) -> None:
    # '상품 단가 수정' 메뉴 처리 흐름
    code = input("\n단가를 수정할 상품 코드: ").strip()
    new_price = input_int("새 단가: ", min_value=0)
    try:
        product = manager.update_price(code, new_price)
        print(f"[완료] 단가가 수정되었습니다 -> {product}")
    except ProductNotFoundError as e:
        print(f"[오류] {e}")
    except ValueError as e:
        print(f"[오류] {e}")

def delete_product_flow(manager: InventoryManager) -> None:
    # '단종 품목 삭제' 메뉴 처리 흐름
    code = input("\n삭제할 상품 코드: ").strip()
    try:
        product = manager.delete_product(code)
        print(f"[완료] 상품이 삭제되었습니다 -> {product}")
    except ProductNotFoundError as e:
        print(f"[오류] {e}")

def main() -> None:
    # 프로그램 진입점・InventoryManager를 생성하고 메뉴 루프를 돌며 사용자 입력에 따라 기능을 호출합니다
    manager = InventoryManager()
    menu_actions = {
        "1": add_product_flow,
        "2": list_all_flow,
        "3": urgent_reorder_flow,
        "4": total_value_flow,
        "5": stock_in_flow,
        "6": stock_out_flow,
        "7": update_price_flow,
        "8": delete_product_flow,
    }

    while True:
        print_menu()
        choice = input("원하는 기능의 번호를 입력하세요: ").strip()
        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        action = menu_actions.get(choice)
        if action is None:
            print("[오류] 올바른 메뉴 번호를 입력해 주세요")
            continue
        action(manager)

if __name__ == "__main__":
    main()