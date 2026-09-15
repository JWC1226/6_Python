"""
    재고 관리용 커스텀 예외 2종과 상품 클래스 계층(Product, NormalProduct, FreshProduct)을 정의합니다
"""
from datetime import date

class OutOfStockError(Exception):
    # 출고하려는 수량이 현재 재고보다 많을 때 발생시키는 예외
    pass

class ProductNotFoundError(Exception):
    # 존재하지 않는 상품 코드로 조회/수정/삭제를 시도할 때 발생시키는 예외
    pass

class Product:
    # 모든 상품의 공통 속성/동작을 정의하는 부모 클래스
    # NormalProduct와 FreshProduct가 이를 상속받아 재사용한다

    def __init__(self, code: str, name: str, price: int, stock: int):
        if price < 0:
            raise ValueError(f"단가는 0 이상이어야 합니다: {price}")
        if stock < 0:
            raise ValueError(f"재고 수량은 0 이상이어야 합니다: {stock}")
        self.code = code
        self.name = name
        self.price = price
        self.stock = stock

    def get_price(self) -> int:
        # 실제 판매 가격을 반환한다
        # FreshProduct는 이를 오버라이딩해 할인가를 반환 (다형성)
        return self.price

    def __str__(self) -> str:
        # 객체를 문자열로 표현한다
        # 자식 클래스는 이를 오버라이딩해 자신만의 추가 정보를 덧붙입니다
        return (
            f"[{self.code}] {self.name} | 단가: {self.price:,}원 | "
            f"재고: {self.stock}개"
        )

class NormalProduct(Product):
    # 일반 물품 클래스
    # 위험물 여부(is_hazardous) 속성을 추가로 가진다

    def __init__(self, code: str, name: str, price: int, stock: int, is_hazardous: bool = False):
        super().__init__(code, name, price, stock)
        self.is_hazardous = is_hazardous

    def __str__(self) -> str:
        base = super().__str__()
        hazard_text = "위험물 O" if self.is_hazardous else "위험물 X"
        return f"{base} | 구분: 일반물품 | {hazard_text}"

class FreshProduct(Product):
    # 신선 식품 클래스
    # 유통기한에 따라 get_price()가 할인가를 반환하도록 오버라이딩

    # 할인 적용 기준일(유통기한까지 남은 일수) / 이 값 이하면 할인 대상
    DISCOUNT_THRESHOLD_DAYS = 3
    # 할인율 (50% 할인)
    DISCOUNT_RATE = 0.5

    def __init__(self, code: str, name: str, price: int, stock: int, expiration_date: date):
        super().__init__(code, name, price, stock)
        self.expiration_date = expiration_date

    def get_price(self) -> int:
        # 유통기한까지 남은 일수가 DISCOUNT_THRESHOLD_DAYS 이하(경과 포함)면 50% 할인가, 아니면 정상가를 반환
        days_left = (self.expiration_date - date.today()).days
        if days_left <= self.DISCOUNT_THRESHOLD_DAYS:
            return int(self.price * self.DISCOUNT_RATE)
        else:
            return self.price

    def __str__(self) -> str:
        base = super().__str__()
        days_left = (self.expiration_date - date.today()).days
        discount_text = " (할인 적용중!)" if days_left <= self.DISCOUNT_THRESHOLD_DAYS else ""
        # D-Day 표기: 남은 경우 D-N(당일은 D-Day), 지난 경우 D+N
        if days_left > 0:
            d_day_text = f"D-{days_left}"
        elif days_left == 0:
            d_day_text = "D-Day"
        else:
            d_day_text = f"D+{abs(days_left)}"
        return (
            f"{base} | 구분: 신선식품 | 유통기한: {self.expiration_date} "
            f"({d_day_text}){discount_text} "
            f"| 실판매가: {self.get_price():,}원"
        )