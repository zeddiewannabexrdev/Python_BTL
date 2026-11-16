from models.menu_item import MenuItem

SIZE_MULTIPLIER = {"S": 0.9, "M": 1.0, "L": 1.2}


class DrinkItem(MenuItem):
    """Đồ uống: giá thay đổi theo size S/M/L."""

    def __init__(self, item_id, item_name, price, category_id,
                 availability=True, size="M"):
        super().__init__(item_id, item_name, price, category_id, availability)
        self.price = price
        self.size = size

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Giá món không được âm")
        self._price = value

    @property
    def size(self) -> str:
        return self._size

    @size.setter
    def size(self, value: str) -> None:
        value = value.upper()
        if value not in SIZE_MULTIPLIER:
            raise ValueError("Size chỉ nhận S, M hoặc L")
        self._size = value

    def calculate_price(self) -> float:
        # Cùng tên hàm với FoodItem nhưng cách tính khác nhau => đa hình
        return self._price * SIZE_MULTIPLIER[self._size]

    def display_info(self) -> str:
        status = "Còn món" if self._availability else "Hết món"
        return (f"[Đồ uống] {self._item_id} | {self._item_name} | "
                f"Size {self._size} | {self.calculate_price():,.0f}đ | {status}")

    def to_dict(self) -> dict:
        return {
            "item_id": self._item_id,
            "item_name": self._item_name,
            "price": self._price,
            "category_id": self._category_id,
            "availability": self._availability,
            "size": self._size,
            "type": "drink",
        }