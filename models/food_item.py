from models.menu_item import MenuItem


class FoodItem(MenuItem):
    """Món ăn: có thêm thời gian chế biến (phút)."""

    def __init__(self, item_id, item_name, price, category_id,
                 availability=True, preparation_time=15):
        super().__init__(item_id, item_name, price, category_id, availability)
        self.price = price                        # chạy qua setter bên dưới để kiểm tra
        self.preparation_time = preparation_time

    # Viết lại property price của lớp cha, thêm kiểm tra dữ liệu
    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Giá món không được âm")
        self._price = value

    @property
    def preparation_time(self) -> int:
        return self._preparation_time

    @preparation_time.setter
    def preparation_time(self, value: int) -> None:
        if value < 0:
            raise ValueError("Thời gian chế biến không được âm")
        self._preparation_time = value

    def calculate_price(self) -> float:
        # Món ăn tính theo giá niêm yết
        return float(self._price)

    def display_info(self) -> str:
        status = "Còn món" if self._availability else "Hết món"
        return (f"[Món ăn] {self._item_id} | {self._item_name} | "
                f"{self.calculate_price():,.0f}đ | "
                f"Chế biến: {self._preparation_time} phút | {status}")

    def to_dict(self) -> dict:
        return {
            "item_id": self._item_id,
            "item_name": self._item_name,
            "price": self._price,
            "category_id": self._category_id,
            "availability": self._availability,
            "preparation_time": self._preparation_time,
            "type": "food",
        }