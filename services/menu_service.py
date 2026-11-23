from models import Category, DrinkItem, FoodItem, MenuItem


class MenuService:
    """Mixin service managing menu items and categories with MongoDB persistence."""

    def _find_item(self, item_id: str) -> MenuItem | None:
        return next((item for item in self._menu_items if item.item_id == item_id), None)

    def _validate_category_exists(self, category_id: str) -> None:
        if self._categories and not any(c.category_id == category_id for c in self._categories):
            raise ValueError(f"Danh mục '{category_id}' không tồn tại.")

    @staticmethod
    def _serialize_item(item: MenuItem) -> dict:
        doc = {
            "item_id": item.item_id,
            "item_name": item.item_name,
            "price": float(item.price),
            "category_id": item.category_id,
            "availability": bool(item.availability),
        }
        if isinstance(item, FoodItem):
            doc["item_type"] = "Food"
            doc["preparation_time"] = int(item.preparation_time)
        elif isinstance(item, DrinkItem):
            doc["item_type"] = "Drink"
            doc["size"] = item.size
        return doc

    def add_item(self, item: MenuItem) -> MenuItem:
        if not isinstance(item, MenuItem):
            raise ValueError("Món thêm mới phải là thể hiện của FoodItem hoặc DrinkItem.")
        if not isinstance(item.item_id, str) or not item.item_id.strip():
            raise ValueError("Mã món không được để trống.")
        if not isinstance(item.item_name, str) or not item.item_name.strip():
            raise ValueError("Tên món không được để trống.")
        if self._find_item(item.item_id) is not None:
            raise ValueError(f"Mã món '{item.item_id}' đã tồn tại trong thực đơn.")
        self._validate_category_exists(item.category_id)

        db = getattr(self, "_db", None)
        if db is not None:
            db.menu_items.insert_one(self._serialize_item(item))

        self._menu_items.append(item)
        return item

    def update_item(self, item_id: str, **kwargs) -> MenuItem:
        item = self._find_item(item_id)
        if item is None:
            raise ValueError(f"Không tìm thấy món có mã '{item_id}'.")

        if "category_id" in kwargs and kwargs["category_id"] is not None:
            self._validate_category_exists(kwargs["category_id"])
            item.category_id = kwargs["category_id"]
        if "item_name" in kwargs and kwargs["item_name"] is not None:
            name = str(kwargs["item_name"]).strip()
            if not name:
                raise ValueError("Tên món không được để trống.")
            item.item_name = name
        if "price" in kwargs and kwargs["price"] is not None:
            item.price = float(kwargs["price"])
        if "availability" in kwargs and kwargs["availability"] is not None:
            item.availability = bool(kwargs["availability"])
        if isinstance(item, FoodItem) and "preparation_time" in kwargs and kwargs["preparation_time"] is not None:
            item.preparation_time = int(kwargs["preparation_time"])
        if isinstance(item, DrinkItem) and "size" in kwargs and kwargs["size"] is not None:
            item.size = str(kwargs["size"])

        db = getattr(self, "_db", None)
        if db is not None:
            db.menu_items.update_one({"item_id": item.item_id}, {"$set": self._serialize_item(item)})

        return item

    def delete_item(self, item_id: str) -> MenuItem:
        item = self._find_item(item_id)
        if item is None:
            raise ValueError(f"Không tìm thấy món có mã '{item_id}'.")

        db = getattr(self, "_db", None)
        if db is not None:
            db.menu_items.delete_one({"item_id": item.item_id})

        self._menu_items.remove(item)
        return item

    def display_all_items(self) -> list[MenuItem]:
        return list(self._menu_items)

    def adjust_price_and_status(
        self,
        item_id: str,
        new_price: float | None = None,
        availability: bool | None = None,
    ) -> MenuItem:
        return self.update_item(item_id, price=new_price, availability=availability)

    def add_category(self, category: Category) -> Category:
        if not isinstance(category, Category):
            raise ValueError("Danh mục phải là thể hiện của Category.")
        if any(c.category_id == category.category_id for c in self._categories):
            raise ValueError(f"Mã danh mục '{category.category_id}' đã tồn tại.")

        db = getattr(self, "_db", None)
        if db is not None:
            db.categories.insert_one(category.to_dict())

        self._categories.append(category)
        return category

    def delete_category(self, category_id: str) -> Category:
        cat = next((c for c in self._categories if c.category_id == category_id), None)
        if cat is None:
            raise ValueError(f"Không tìm thấy danh mục '{category_id}'.")
        linked = [item for item in self._menu_items if item.category_id == category_id]
        if linked:
            raise ValueError(
                f"Không thể xóa danh mục '{category_id}' vì đang có {len(linked)} món liên kết."
            )

        db = getattr(self, "_db", None)
        if db is not None:
            db.categories.delete_one({"category_id": cat.category_id})

        self._categories.remove(cat)
        return cat
