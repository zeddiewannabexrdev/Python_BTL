import unittest

from app import app
from models import Category, DrinkItem, FoodItem, MenuItem, Order
from services import MenuService, OrderReportService, QueryService, RestaurantManager


class TestBaseProject(unittest.TestCase):
    def test_oop_models_structure(self):
        with self.assertRaises(TypeError):
            MenuItem("X1", "Abstract", 10000, "CAT01")

        food = FoodItem("F99", "Phở bò", 65000, "CAT01", True, preparation_time=12)
        food.item_name = "Phở bò tái"
        self.assertEqual(food.item_name, "Phở bò tái")
        self.assertEqual(food.preparation_time, 12)
        self.assertIsNone(food.calculate_price())
        self.assertIsNone(food.display_info())

        drink = DrinkItem("D99", "Cà phê sữa", 35000, "CAT03", True, size="L")
        drink.size = "M"
        self.assertEqual(drink.size, "M")
        self.assertIsNone(drink.calculate_price())

        cat = Category("CAT99", "Món mới")
        self.assertIn("CAT99", str(cat))

        order = Order("ORD-01", "2026-11-13", [{"item": food, "quantity": 1}])
        self.assertIsNone(order.calculate_bill())

    def test_restaurant_manager_inheritance_and_mock_data(self):
        self.assertTrue(issubclass(RestaurantManager, MenuService))
        self.assertTrue(issubclass(RestaurantManager, QueryService))
        self.assertTrue(issubclass(RestaurantManager, OrderReportService))

        manager = RestaurantManager()
        self.assertEqual(len(manager.categories), 4)
        self.assertEqual(len(manager.menu_items), 10)
        self.assertEqual(len(manager.orders), 5)

        self.assertIsNone(manager.add_item(None))
        self.assertIsNone(manager.update_item("FD01"))
        self.assertIsNone(manager.delete_item("FD01"))
        self.assertIsNone(manager.display_all_items())
        self.assertIsNone(manager.adjust_price_and_status("FD01"))
        self.assertIsNone(manager.search_by_id("FD01"))
        self.assertIsNone(manager.search_by_criteria())
        self.assertIsNone(manager.sort_items())
        self.assertIsNone(manager.create_order(None))
        self.assertIsNone(manager.calculate_bill([]))
        self.assertIsNone(manager.stat_total_revenue())
        self.assertIsNone(manager.stat_revenue_by_category())
        self.assertIsNone(manager.stat_top_ordered_items())

    def test_flask_five_routes_render(self):
        client = app.test_client()
        for path in ["/", "/manage", "/search-sort", "/orders", "/statistics"]:
            resp = client.get(path)
            self.assertEqual(resp.status_code, 200, f"Failed on {path}")


if __name__ == "__main__":
    unittest.main()
