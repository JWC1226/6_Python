# inventory.py
# ------------------------------------------------------------
# InventoryManager 클래스: 리스트(List)를 이용하여 상품들을 메모리에 저장하고,
# 신규 등록 / 조회 / 입출고 / 단가 수정 / 삭제 등의 비즈니스 로직을 처리합니다.
# 파일이나 DB를 전혀 사용하지 않고, self.products 라는 리스트에만 데이터를 보관합니다.
# ------------------------------------------------------------

from models import Product, OutOfStockError, ProductNotFoundError


class InventoryManager:
    """
    재고(상품 목록)를 관리하는 클래스입니다.
    내부적으로 Product(또는 그 자식 클래스) 객체들을 self.products 리스트에 담아 관리합니다.
    """

    # 긴급 발주 기준 재고 수량: 이 값 미만이면 '재고 부족'으로 간주합니다.
    URGENT_REORDER_THRESHOLD = 10

    def __init__(self):
        # 프로그램 실행 중에만 유지되는 메모리 저장소 (리스트)
        self.products: list[Product] = []

    # --------------------------------------------------------
    # 신규 상품 등록
    # --------------------------------------------------------
    def add_product(self, product: Product) -> None:
        """
        새 상품 객체(NormalProduct 또는 FreshProduct)를 리스트에 추가합니다.
        이미 같은 상품 코드가 존재하면 등록을 막아 데이터 중복을 방지합니다.
        """
        if self._find_product_or_none(product.code) is not None:
            raise ValueError(f"이미 존재하는 상품 코드입니다: {product.code}")
        self.products.append(product)

    # --------------------------------------------------------
    # 상품 코드로 상품 찾기 (내부 helper 메서드)
    # --------------------------------------------------------
    def _find_product_or_none(self, code: str) -> Product | None:
        """리스트를 순회하며 code가 일치하는 상품을 찾습니다. 없으면 None을 반환합니다."""
        for product in self.products:
            if product.code == code:
                return product
        return None

    def find_product(self, code: str) -> Product:
        """
        상품 코드로 상품을 찾아 반환합니다.
        찾지 못하면 ProductNotFoundError를 발생시킵니다.
        (수정/삭제/입출고 등 '반드시 존재해야 하는' 조회에 사용합니다.)
        """
        product = self._find_product_or_none(code)
        if product is None:
            raise ProductNotFoundError(f"상품 코드 '{code}'를 찾을 수 없습니다.")
        return product

    # --------------------------------------------------------
    # 전체 재고 조회
    # --------------------------------------------------------
    def get_all_products(self) -> list[Product]:
        """등록된 모든 상품 리스트를 반환합니다."""
        return self.products

    # --------------------------------------------------------
    # 긴급 발주 목록 조회 (재고 수량 10개 미만)
    # --------------------------------------------------------
    def get_urgent_reorder_list(self) -> list[Product]:
        """재고 수량이 URGENT_REORDER_THRESHOLD(10개) 미만인 상품만 골라 반환합니다."""
        return [p for p in self.products if p.stock < self.URGENT_REORDER_THRESHOLD]

    # --------------------------------------------------------
    # 전체 재고 총 금액 확인
    # --------------------------------------------------------
    def get_total_inventory_value(self) -> int:
        """
        전체 재고의 총 금액을 계산합니다.
        각 상품의 get_price()(실제 판매가) * stock(재고수량)을 모두 더합니다.

        [다형성 포인트]
        여기서는 상품이 NormalProduct인지 FreshProduct인지 전혀 구분하지 않습니다.
        그냥 product.get_price()를 호출할 뿐이며, 실제로 어떤 클래스의 get_price()가
        실행되는지는 객체 스스로가 결정합니다(신선식품이면 할인가가 자동으로 계산됨).
        이것이 객체지향의 다형성(Polymorphism)이 주는 이점입니다.
        """
        total = 0
        for product in self.products:
            total += product.get_price() * product.stock
        return total

    # --------------------------------------------------------
    # 입고 처리 (재고 증가)
    # --------------------------------------------------------
    def stock_in(self, code: str, amount: int) -> Product:
        """
        상품 코드로 상품을 찾아 재고 수량을 amount만큼 증가시킵니다.
        상품이 없으면 find_product() 내부에서 ProductNotFoundError가 발생합니다.
        """
        product = self.find_product(code)
        product.stock += amount
        return product

    # --------------------------------------------------------
    # 출고 처리 (재고 감소)
    # --------------------------------------------------------
    def stock_out(self, code: str, amount: int) -> Product:
        """
        상품 코드로 상품을 찾아 재고 수량을 amount만큼 감소시킵니다.
        출고하려는 수량이 현재 재고보다 많으면 OutOfStockError를 발생시킵니다.
        """
        product = self.find_product(code)
        if amount > product.stock:
            raise OutOfStockError(
                f"재고 부족: '{product.name}'의 현재 재고는 {product.stock}개인데 "
                f"{amount}개를 출고하려고 했습니다."
            )
        product.stock -= amount
        return product

    # --------------------------------------------------------
    # 상품 단가 수정
    # --------------------------------------------------------
    def update_price(self, code: str, new_price: int) -> Product:
        """
        상품 코드로 상품을 찾아 단가(price)를 new_price로 수정합니다.
        상품이 없으면 ProductNotFoundError가 발생합니다.
        """
        product = self.find_product(code)
        product.price = new_price
        return product

    # --------------------------------------------------------
    # 단종 품목 삭제
    # --------------------------------------------------------
    def delete_product(self, code: str) -> Product:
        """
        상품 코드로 상품을 찾아 리스트에서 제거합니다.
        상품이 없으면 ProductNotFoundError가 발생합니다.
        """
        product = self.find_product(code)
        self.products.remove(product)
        return product
