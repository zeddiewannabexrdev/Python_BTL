from datetime import datetime


class Order:
    """Represents a customer order containing menu items and quantities."""

    def __init__(
        self,
        order_id: str,
        order_date: datetime | str | None = None,
        items: list[dict] | None = None,
    ) -> None:
        self._order_id = order_id
        self._order_date = order_date or datetime.now()
        self._items = items if items is not None else []

    @property
    def order_id(self) -> str:
        return self._order_id

    @order_id.setter
    def order_id(self, value: str) -> None:
        self._order_id = value

    @property
    def order_date(self) -> datetime | str:
        return self._order_date

    @order_date.setter
    def order_date(self, value: datetime | str) -> None:
        self._order_date = value

    @property
    def items(self) -> list[dict]:
        return self._items

    @items.setter
    def items(self, value: list[dict]) -> None:
        self._items = value

    def calculate_bill(self) -> float:
        total = 0.0
        for line in self._items:
            unit_price = line.get("unit_price")
            if unit_price is None:
                item = line.get("item")
                if item is None:
                    raise ValueError("Each order line must include a unit price or item")
                unit_price = item.calculate_price()
            total += unit_price * line["quantity"]
        return total

    def __str__(self) -> str:
        return f"Order #{self._order_id} ({self._order_date}) - {len(self._items)} món"
