"""
    상품 목록을 메모리 리스트로 관리하며 등록/조회/입출고/단가수정/삭제 로직을 제공하는 InventoryManager를 정의합니다
"""
from models import Product, OutOfStockError, ProductNotFoundError

class InventoryManager:
    # 상품(Product 및 그 자식 클래스) 객체들을 리스트로 관리하는 클래스
    # 이 값 미만이면 긴급 발주가 필요한 재고로 간주
    URGENT_REORDER_THRESHOLD = 10

    def __init__(self):
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        # 새 상품을 등록
        # 이미 같은 코드가 존재하면 ValueError를 발생시킨다
        if self._find_product_or_none(product.code) is not None:
            raise ValueError(f"이미 존재하는 상품 코드입니다: {product.code}")
        self.products.append(product)

    def _find_product_or_none(self, code: str) -> Product | None:
        # code가 일치하는 상품을 찾아 반환하고, 없으면 None을 반환한다
        for product in self.products:
            if product.code == code:
                return product
        return None

    def find_product(self, code: str) -> Product:
        # 상품 코드로 상품을 찾아 반환한다
        # 없으면 ProductNotFoundError를 발생
        product = self._find_product_or_none(code)
        if product is None:
            raise ProductNotFoundError(f"상품 코드 '{code}'를 찾을 수 없습니다")
        return product

    def get_all_products(self) -> list[Product]:
        # 등록된 모든 상품 리스트를 반환힌디
        return self.products

    def get_urgent_reorder_list(self) -> list[Product]:
        # 재고 수량이 URGENT_REORDER_THRESHOLD 미만인 상품만 골라 반환한다
        return [p for p in self.products if p.stock < self.URGENT_REORDER_THRESHOLD]

    def get_total_inventory_value(self) -> int:
        # 전체 재고의 총 금액(get_price() * stock의 합)을 계산
        # 상품 종류를 구분하지 않고 각 객체의 get_price()를 그대로 사용(다형성)
        total = 0
        for product in self.products:
            total += product.get_price() * product.stock
        return total

    def stock_in(self, code: str, amount: int) -> Product:
        # 상품 재고를 amount만큼 증가 & amount가 0 이하이면 ValueError가 발생
        if amount <= 0:
            raise ValueError(f"입고 수량은 1 이상이어야 합니다: {amount}")
        product = self.find_product(code)
        product.stock += amount
        return product

    def stock_out(self, code: str, amount: int) -> Product:
        # 상품 재고를 amount만큼 감소시킨다
        # amount가 0 이하이면 ValueError를 / 재고보다 많으면 OutOfStockError를 발생시킨다
        if amount <= 0:
            raise ValueError(f"출고 수량은 1 이상이어야 합니다: {amount}")
        product = self.find_product(code)
        if amount > product.stock:
            raise OutOfStockError(
                f"재고 부족: '{product.name}'의 현재 재고는 {product.stock}개인데 "
                f"{amount}개를 출고하려고 했습니다"
            )
        product.stock -= amount
        return product

    def update_price(self, code: str, new_price: int) -> Product:
        # 상품 단가를 new_price로 수정
        # new_price가 음수이면 ValueError가 발생한다
        if new_price < 0:
            raise ValueError(f"단가는 0 이상이어야 합니다: {new_price}")
        product = self.find_product(code)
        product.price = new_price
        return product

    def delete_product(self, code: str) -> Product:
        # 상품을 리스트에서 제거한다
        # 없으면 ProductNotFoundError가 발생한다
        product = self.find_product(code)
        self.products.remove(product)
        return product