import json
from pathlib import Path

from models import Category, DrinkItem, FoodItem, Order

from .menu_service import MenuService
from .search_sort_order_manager import SearchSortOrderManager


class RestaurantManager(MenuService, SearchSortOrderManager):
    """Unified service facade for menu, search, sorting, and order operations."""

    def __init__(self, mock_filepath: str = "data/mock_data.json") -> None:
        self._categories: list[Category] = []
        super().__init__()
        self._raw_orders: list[dict] = []
        self.load_mock_data(mock_filepath)

    @property
    def categories(self) -> list[Category]:
        return self._categories

    @property
    def menu_items(self) -> list[FoodItem | DrinkItem]:
        return self._menu_items

    @property
    def orders(self) -> list[Order]:
        return self._orders

    @property
    def raw_orders(self) -> list[dict]:
        return self._raw_orders

    def load_mock_data(self, filepath: str = "data/mock_data.json") -> None:
        """Load categories, polymorphic menu items, and sample orders from JSON."""
        path = Path(filepath)
        if not path.is_absolute() and not path.exists():
            path = Path(__file__).resolve().parent.parent / filepath

        with path.open("r", encoding="utf-8-sig") as file:
            payload = json.load(file)

        self._categories = [
            Category(cat["category_id"], cat["category_name"])
            for cat in payload.get("categories", [])
        ]

        items: list[FoodItem | DrinkItem] = []
        item_lookup: dict[str, FoodItem | DrinkItem] = {}
        for row in payload.get("menu_items", []):
            if row.get("item_type") == "Food":
                obj = FoodItem(
                    item_id=row["item_id"],
                    item_name=row["item_name"],
                    price=row["price"],
                    category_id=row["category_id"],
                    availability=row.get("availability", True),
                    preparation_time=row.get("preparation_time", 15),
                )
            else:
                obj = DrinkItem(
                    item_id=row["item_id"],
                    item_name=row["item_name"],
                    price=row["price"],
                    category_id=row["category_id"],
                    availability=row.get("availability", True),
                    size=row.get("size", "M"),
                )
            items.append(obj)
            item_lookup[obj.item_id] = obj
        self._menu_items = items

        self._raw_orders = payload.get("orders", [])
        orders: list[Order] = []
        for raw in self._raw_orders:
            mapped_items = [
                {
                    "item": item_lookup.get(entry["item_id"]),
                    "item_id": entry["item_id"],
                    "quantity": entry["quantity"],
                    "unit_price": entry["unit_price"],
                }
                for entry in raw.get("items", [])
            ]
            orders.append(
                Order(
                    order_id=raw["order_id"],
                    order_date=raw.get("order_date"),
                    items=mapped_items,
                )
            )
        self._orders = orders
