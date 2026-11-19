import json
import unittest
from datetime import datetime

from models.category import Category
from models.order import Order


class DummyItem:
    def __init__(self, item_id="F01", price=45000):
        self.item_id = item_id
        self.item_name = "Phở bò"
        self.category_id = "C01"
        self.price = price

    def calculate_price(self):
        return self.price


class TestCategory(unittest.TestCase):
    def test_category_valid(self):
        self.assertEqual(Category("C01", "Món chính").category_name, "Món chính")

    def test_category_id_empty(self):
        with self.assertRaises(ValueError):
            Category(" ", "Món chính")

    def test_category_name_empty(self):
        with self.assertRaises(ValueError):
            Category("C01", "")

    def test_category_name_setter(self):
        category = Category("C01", "Món chính")
        category.category_name = "Đồ uống"
        self.assertEqual(category.to_dict()["category_name"], "Đồ uống")

    def test_category_json(self):
        self.assertEqual(json.loads(json.dumps(Category("C01", "Món chính").to_dict()))["category_id"], "C01")


class TestOrder(unittest.TestCase):
    def test_default_date(self):
        self.assertIsInstance(Order("HD001").order_date, datetime)

    def test_custom_iso_date(self):
        self.assertEqual(Order("HD001", "2026-11-13T10:30:00").order_date.hour, 10)

    def test_invalid_order_id(self):
        with self.assertRaises(ValueError):
            Order(" ")

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            Order("HD001", "khong-phai-ngay")

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            Order("HD001").add_item_to_order(DummyItem(), -1)

    def test_float_quantity(self):
        with self.assertRaises(ValueError):
            Order("HD001").add_item_to_order(DummyItem(), 1.5)

    def test_empty_order(self):
        self.assertEqual(Order("HD001").calculate_bill(), 0)

    def test_total_bill(self):
        order = Order("HD001")
        order.add_item_to_order(DummyItem("F01", 45000), 2)
        order.add_item_to_order(DummyItem("F02", 50000), 1)
        self.assertEqual(order.calculate_bill(), 140000)

    def test_duplicate_item_merges(self):
        order = Order("HD001")
        order.add_item_to_order(DummyItem(), 1)
        order.add_item_to_order(DummyItem(), 2)
        self.assertEqual(order.items[0]["quantity"], 3)
        self.assertEqual(len(order.items), 1)

    def test_polymorphic_calculate_price(self):
        class Drink(DummyItem):
            def calculate_price(self):
                return self.price * 1.15

        order = Order("HD001")
        order.add_item_to_order(Drink("D01", 20000), 2)
        self.assertEqual(order.calculate_bill(), 46000)

    def test_order_to_json(self):
        order = Order("HD001")
        order.add_item_to_order(DummyItem(), 2)
        parsed = json.loads(json.dumps(order.to_dict(), ensure_ascii=False))
        self.assertEqual(parsed["items"][0]["subtotal"], 90000)

    def test_display_info(self):
        order = Order("HD001")
        order.add_item_to_order(DummyItem(), 1)
        self.assertIn("TỔNG THANH TOÁN", order.display_info())


if __name__ == "__main__":
    unittest.main()
