from models import MenuItem, Order

from .order_report_service import OrderReportService
from .query_service import QueryService


class SearchSortOrderManager(QueryService, OrderReportService):
    """Search, sort, and create orders using menu items and orders owned by the manager."""

    def __init__(
        self,
        menu_items: list[MenuItem] | None = None,
        orders: list[Order] | None = None,
    ) -> None:
        self._menu_items = menu_items if menu_items is not None else []
        self._orders = orders if orders is not None else []

    @property
    def menu_items(self) -> list[MenuItem]:
        return self._menu_items

    @property
    def orders(self) -> list[Order]:
        return self._orders

    def search_by_id(self, item_id: str) -> MenuItem | None:
        return next((item for item in self._menu_items if item.item_id == item_id), None)

    def search_by_name(self, keyword: str) -> list[MenuItem]:
        normalized_keyword = keyword.casefold()
        return [
            item
            for item in self._menu_items
            if normalized_keyword in item.item_name.casefold()
        ]

    def filter_by_category(self, category_id: str) -> list[MenuItem]:
        return [
            item for item in self._menu_items if item.category_id == category_id
        ]

    def filter_by_price_range(
        self, min_price: float, max_price: float
    ) -> list[MenuItem]:
        if min_price > max_price:
            raise ValueError("min_price must not be greater than max_price")
        return [
            item
            for item in self._menu_items
            if min_price <= item.calculate_price() <= max_price
        ]

    def sort_by_price(self, reverse: bool = False) -> list[MenuItem]:
        return sorted(
            self._menu_items,
            key=lambda item: item.calculate_price(),
            reverse=reverse,
        )

    def sort_by_name(self, reverse: bool = False) -> list[MenuItem]:
        return sorted(
            self._menu_items,
            key=lambda item: item.item_name.casefold(),
            reverse=reverse,
        )

    def search_by_criteria(
        self,
        keyword: str = "",
        category_id: str = "",
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> list[MenuItem]:
        items = self._menu_items
        if keyword:
            normalized_keyword = keyword.casefold()
            items = [
                item
                for item in items
                if normalized_keyword in item.item_name.casefold()
            ]
        if category_id:
            items = [item for item in items if item.category_id == category_id]
        if min_price is not None:
            items = [
                item for item in items if item.calculate_price() >= min_price
            ]
        if max_price is not None:
            items = [
                item for item in items if item.calculate_price() <= max_price
            ]
        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValueError("min_price must not be greater than max_price")
        return list(items)

    def sort_items(self, by: str = "price", ascending: bool = True) -> list[MenuItem]:
        if by == "price":
            return self.sort_by_price(reverse=not ascending)
        if by == "name":
            return self.sort_by_name(reverse=not ascending)
        raise ValueError("by must be 'price' or 'name'")

    def calculate_bill(self, order_items: list[dict]) -> float:
        total = 0.0
        for line in order_items:
            unit_price = line.get("unit_price")
            if unit_price is None:
                item = line.get("item_obj") or line.get("item")
                if item is None:
                    raise ValueError("Each order line must include a unit price or item")
                unit_price = item.calculate_price()
            total += unit_price * line["quantity"]
        return total

    def create_order(self, order_id: str, items: list[dict]) -> float:
        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("order_id must be a non-empty string")

        validated_lines = []
        for entry in items:
            item_id = entry.get("item_id")
            quantity = entry.get("quantity")
            if not isinstance(item_id, str) or not item_id:
                raise ValueError("Each order line must include an item_id")
            if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
                raise ValueError("quantity must be a positive integer")

            item = self.search_by_id(item_id)
            if item is None:
                raise ValueError(f"Menu item '{item_id}' does not exist")
            if not item.availability:
                raise ValueError(f"Menu item '{item_id}' is not currently available")

            validated_lines.append((item, quantity))

        order = Order(order_id=order_id)
        for item, quantity in validated_lines:
            order.add_item_to_order(item, quantity)

        total = order.calculate_bill()
        self._orders.append(order)
        return total
