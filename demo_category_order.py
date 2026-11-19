"""Chạy thử độc lập module của Hải bằng: python demo.py"""
import json
from models.category import Category
from models.order import Order


class DummyItem:
    """Chỉ dùng để demo trước khi nhận FoodItem/DrinkItem thật từ Khánh."""

    def __init__(self, item_id, item_name, category_id, price):
        self.item_id = item_id
        self.item_name = item_name
        self.category_id = category_id
        self.price = price

    def calculate_price(self):
        return self.price


if __name__ == "__main__":
    category = Category("C01", "Món chính")
    print(category.display_info())

    pho = DummyItem("F01", "Phở bò", "C01", 45000)
    com = DummyItem("F02", "Cơm gà", "C01", 50000)
    order = Order("HD001")
    order.add_item_to_order(pho, 2)
    order.add_item_to_order(com, 1)
    print("\n" + order.display_info())
    print("\nDữ liệu JSON:\n" + json.dumps(order.to_dict(), ensure_ascii=False, indent=2))
