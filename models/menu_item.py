from abc import ABC, abstractmethod


class MenuItem(ABC):
    """Abstract base class representing a menu item."""

    def __init__(
        self,
        item_id: str,
        item_name: str,
        price: float,
        category_id: str,
        availability: bool = True,
    ) -> None:
        self._item_id = item_id
        self._item_name = item_name
        self._price = price
        self._category_id = category_id
        self._availability = availability

    @property
    def item_id(self) -> str:
        return self._item_id

    @item_id.setter
    def item_id(self, value: str) -> None:
        self._item_id = value

    @property
    def item_name(self) -> str:
        return self._item_name

    @item_name.setter
    def item_name(self, value: str) -> None:
        self._item_name = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        self._price = value

    @property
    def category_id(self) -> str:
        return self._category_id

    @category_id.setter
    def category_id(self, value: str) -> None:
        self._category_id = value

    @property
    def availability(self) -> bool:
        return self._availability

    @availability.setter
    def availability(self, value: bool) -> None:
        self._availability = value

    @abstractmethod
    def calculate_price(self) -> float:
        pass

    @abstractmethod
    def display_info(self) -> str:
        pass

    def __str__(self) -> str:
        status = "Còn món" if self._availability else "Hết món"
        return f"[{self._item_id}] {self._item_name} - {self._price:,.0f}đ ({status})"


class FoodItem(MenuItem):
    """Concrete menu item representing a food dish."""

    def __init__(
        self,
        item_id: str,
        item_name: str,
        price: float,
        category_id: str,
        availability: bool = True,
        preparation_time: int = 15,
    ) -> None:
        super().__init__(item_id, item_name, price, category_id, availability)
        self._preparation_time = preparation_time

    @property
    def preparation_time(self) -> int:
        return self._preparation_time

    @preparation_time.setter
    def preparation_time(self, value: int) -> None:
        self._preparation_time = value

    def calculate_price(self) -> float:
        pass

    def display_info(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{super().__str__()} | Thời gian chế biến: {self._preparation_time} phút"


class DrinkItem(MenuItem):
    """Concrete menu item representing a beverage."""

    def __init__(
        self,
        item_id: str,
        item_name: str,
        price: float,
        category_id: str,
        availability: bool = True,
        size: str = "M",
    ) -> None:
        super().__init__(item_id, item_name, price, category_id, availability)
        self._size = size

    @property
    def size(self) -> str:
        return self._size

    @size.setter
    def size(self, value: str) -> None:
        self._size = value

    def calculate_price(self) -> float:
        pass

    def display_info(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{super().__str__()} | Size: {self._size}"
