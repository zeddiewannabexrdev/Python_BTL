import os

from pymongo import MongoClient

from data.seed_mongodb import DEFAULT_DB_NAME, DEFAULT_MONGO_URI, ensure_indexes, seed_database
from models import Category, DrinkItem, FoodItem, Order

from .menu_service import MenuService
from .search_sort_order_manager import SearchSortOrderManager


class RestaurantManager(MenuService, SearchSortOrderManager):
    """Unified service facade backed by MongoDB."""

    def __init__(
        self,
        mongo_uri: str | None = None,
        db_name: str | None = None,
        auto_seed: bool = True,
    ) -> None:
        self._categories: list[Category] = []
        super().__init__()
        self._mongo_uri = mongo_uri or os.getenv("MONGO_URI", DEFAULT_MONGO_URI)
        self._db_name = db_name or os.getenv("MONGO_DB", DEFAULT_DB_NAME)
        self._client = MongoClient(self._mongo_uri, serverSelectionTimeoutMS=5000)
        self._db = self._client[self._db_name]
        ensure_indexes(self._db)
        if auto_seed and self._db.categories.count_documents({}) == 0 and self._db.menu_items.count_documents({}) == 0:
            seed_database(self._db, reset=False)
        self.load_from_db()

    @property
    def db(self):
        return self._db

    @property
    def categories(self) -> list[Category]:
        return self._categories

    @property
    def menu_items(self) -> list[FoodItem | DrinkItem]:
        return self._menu_items

    @property
    def orders(self) -> list[Order]:
        return self._orders

    def close(self) -> None:
        self._client.close()

    def load_from_db(self) -> None:
        """Load categories, polymorphic menu items, and orders from MongoDB."""
        self._categories = [
            Category(doc["category_id"], doc["category_name"])
            for doc in self._db.categories.find({}, {"_id": 0}).sort("category_id", 1)
        ]

        items: list[FoodItem | DrinkItem] = []
        item_lookup: dict[str, FoodItem | DrinkItem] = {}
        for doc in self._db.menu_items.find({}, {"_id": 0}):
            if doc.get("item_type") == "Food":
                obj = FoodItem(
                    item_id=doc["item_id"],
                    item_name=doc["item_name"],
                    price=doc["price"],
                    category_id=doc["category_id"],
                    availability=doc.get("availability", True),
                    preparation_time=doc.get("preparation_time", 15),
                )
            else:
                obj = DrinkItem(
                    item_id=doc["item_id"],
                    item_name=doc["item_name"],
                    price=doc["price"],
                    category_id=doc["category_id"],
                    availability=doc.get("availability", True),
                    size=doc.get("size", "M"),
                )
            items.append(obj)
            item_lookup[obj.item_id] = obj
        self._menu_items = items

        orders: list[Order] = []
        for raw in self._db.orders.find({}, {"_id": 0}):
            order = Order(
                order_id=raw["order_id"],
                order_date=raw.get("order_date"),
            )
            for entry in raw.get("items", []):
                item_id = entry["item_id"]
                item = item_lookup.get(item_id)
                if item is None:
                    continue
                if isinstance(item, DrinkItem) and entry.get("size"):
                    item = DrinkItem(
                        item_id=item.item_id,
                        item_name=item.item_name,
                        price=item.price,
                        category_id=item.category_id,
                        availability=item.availability,
                        size=entry["size"],
                    )
                order.add_item_to_order(item, entry["quantity"])
            orders.append(order)
        self._orders = orders
