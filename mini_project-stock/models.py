# models.py
# ------------------------------------------------------------
# 이 파일에는 다음 내용이 정의되어 있습니다.
#   1) 재고 관리 중 발생할 수 있는 커스텀 예외 클래스 2종
#   2) 모든 상품의 공통 속성/기능을 담은 부모 클래스 Product
#   3) Product를 상속받는 자식 클래스 NormalProduct(일반 물품), FreshProduct(신선 식품)
# ------------------------------------------------------------

from datetime import date


# ============================================================
# 1. 커스텀 예외 클래스
# ============================================================

class OutOfStockError(Exception):
    """
    출고(판매/반출) 하려는 수량이 현재 재고 수량보다 많을 때 발생시키는 예외입니다.
    예) 재고가 5개인데 10개를 출고하려고 할 때 사용합니다.
    """
    pass


class ProductNotFoundError(Exception):
    """
    존재하지 않는 상품 코드로 조회/수정/삭제를 시도할 때 발생시키는 예외입니다.
    예) 상품 코드 'A999'가 목록에 없는데 해당 코드를 수정하려고 할 때 사용합니다.
    """
    pass


# ============================================================
# 2. 부모 클래스 Product
# ============================================================

class Product:
    """
    모든 상품의 '공통 속성'과 '공통 동작'을 정의하는 부모(상위) 클래스입니다.
    NormalProduct, FreshProduct는 이 클래스를 상속(inheritance)받아서
    공통 기능은 그대로 재사용하고, 필요한 부분만 추가/수정(오버라이딩)합니다.
    """

    def __init__(self, code: str, name: str, price: int, stock: int):
        # 상품 코드 (예: 'A001') - 상품을 구분하는 고유 값
        self.code = code
        # 품명 (예: '볼펜')
        self.name = name
        # 단가 (할인 등이 적용되지 않은 기본 판매 가격)
        self.price = price
        # 재고 수량
        self.stock = stock

    def get_price(self) -> int:
        """
        상품의 '실제 판매 가격'을 반환하는 메서드입니다.
        부모 클래스에서는 별다른 할인 로직이 없으므로 단가(self.price)를 그대로 반환합니다.
        자식 클래스인 FreshProduct는 이 메서드를 오버라이딩(재정의)하여
        유통기한에 따라 할인된 가격을 반환하도록 동작을 바꿉니다. (다형성)
        """
        return self.price

    def __str__(self) -> str:
        """
        print(product) 등으로 객체를 문자열로 표현할 때 호출되는 메서드입니다.
        자식 클래스들은 이 메서드를 오버라이딩하여 자신만의 추가 정보(위험물 여부, 유통기한 등)를
        함께 출력하도록 확장합니다. 이렇게 하면 어떤 상품이든 동일한 형식으로 출력할 수 있어
        '출력 일관성'을 확보할 수 있습니다.
        """
        return (
            f"[{self.code}] {self.name} | 단가: {self.price:,}원 | "
            f"재고: {self.stock}개"
        )


# ============================================================
# 3. 자식 클래스 NormalProduct (일반 물품)
# ============================================================

class NormalProduct(Product):
    """
    일반 물품을 나타내는 클래스입니다.
    Product의 공통 속성(코드, 품명, 단가, 재고수량)을 그대로 물려받고,
    '위험물 여부(is_hazardous)' 속성을 추가로 가집니다.
    """

    def __init__(self, code: str, name: str, price: int, stock: int, is_hazardous: bool = False):
        # super().__init__(...) : 부모 클래스(Product)의 생성자를 호출하여
        # 공통 속성(code, name, price, stock)을 초기화합니다.
        super().__init__(code, name, price, stock)
        # 일반 물품만 가지는 추가 속성: 위험물 여부
        self.is_hazardous = is_hazardous

    def __str__(self) -> str:
        # 부모의 __str__ 결과를 재사용(super())하고, 위험물 여부 정보만 덧붙입니다.
        base = super().__str__()
        hazard_text = "위험물 O" if self.is_hazardous else "위험물 X"
        return f"{base} | 구분: 일반물품 | {hazard_text}"


# ============================================================
# 4. 자식 클래스 FreshProduct (신선 식품)
# ============================================================

class FreshProduct(Product):
    """
    신선 식품을 나타내는 클래스입니다.
    Product의 공통 속성에 더해 '유통기한(expiration_date)' 속성을 가집니다.

    핵심 포인트: get_price()를 오버라이딩하여
    "유통기한이 오늘로부터 3일 이내로 남았다면 단가를 50% 할인"하는 로직을 구현합니다.
    """

    # 할인 적용 기준일(유통기한까지 남은 일수). 3일 이내면 할인 대상입니다.
    DISCOUNT_THRESHOLD_DAYS = 3
    # 할인율 (50% 할인 -> 가격에 0.5를 곱함)
    DISCOUNT_RATE = 0.5

    def __init__(self, code: str, name: str, price: int, stock: int, expiration_date: date):
        super().__init__(code, name, price, stock)
        # 유통기한: datetime.date 형식으로 저장합니다. (예: date(2026, 9, 18))
        self.expiration_date = expiration_date

    def get_price(self) -> int:
        """
        [다형성의 핵심 예시]
        오늘 날짜와 유통기한(expiration_date)의 차이를 계산하여,
        남은 일수가 3일 이하(0~3일, 이미 지난 경우 포함)이면 단가의 50%를 할인한 가격을 반환합니다.
        그렇지 않으면 부모 클래스와 동일하게 원래 단가를 반환합니다.
        """
        # date.today() : 오늘 날짜를 반환합니다.
        # (유통기한 - 오늘 날짜) 를 계산하면 timedelta 객체가 반환되고,
        # .days 를 통해 '차이 일수(정수)'만 뽑아낼 수 있습니다.
        days_left = (self.expiration_date - date.today()).days

        if days_left <= self.DISCOUNT_THRESHOLD_DAYS:
            # 유통기한이 3일 이내(또는 이미 지남)로 남은 경우 -> 50% 할인가 반환
            # int()로 소수점 이하를 버려 정수 원 단위로 맞춥니다.
            return int(self.price * self.DISCOUNT_RATE)
        else:
            # 여유가 있는 경우 -> 정상 단가 반환
            return self.price

    def __str__(self) -> str:
        base = super().__str__()
        # 유통기한까지 남은 일수를 함께 보여주면 사용자가 상태를 바로 파악할 수 있습니다.
        days_left = (self.expiration_date - date.today()).days
        discount_text = " (할인 적용중!)" if days_left <= self.DISCOUNT_THRESHOLD_DAYS else ""
        d_day_text = f"D+{days_left}" if days_left >= 0 else f"D-{abs(days_left)}"
        return (
            f"{base} | 구분: 신선식품 | 유통기한: {self.expiration_date} "
            f"({d_day_text}){discount_text} "
            f"| 실판매가: {self.get_price():,}원"
        )
