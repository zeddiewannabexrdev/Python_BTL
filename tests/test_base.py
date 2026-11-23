import unittest

from app import app
from models import Category, DrinkItem, FoodItem, MenuItem, Order
from services import (
    MenuService,
    OrderReportService,
    QueryService,
    RestaurantManager,
    SearchSortOrderManager,
)


class TestBaseProject(unittest.TestCase):
    def test_oop_models_structure(self):
        with self.assertRaises(TypeError):
            MenuItem("X1", "Abstract", 10000, "CAT01")

        food = FoodItem("F99", "Phở bò", 65000, "CAT01", True, preparation_time=12)
        food.item_name = "Phở bò tái"
        self.assertEqual(food.item_name, "Phở bò tái")
        self.assertEqual(food.preparation_time, 12)
        self.assertEqual(food.calculate_price(), 65000.0)
        self.assertIn("Phở bò tái", food.display_info())

        drink = DrinkItem("D99", "Cà phê sữa", 35000, "CAT03", True, size="L")
        drink.size = "M"
        self.assertEqual(drink.size, "M")
        self.assertEqual(drink.calculate_price(), 35000.0)

        cat = Category("CAT99", "Món mới")
        self.assertIn("CAT99", str(cat))

        order = Order("ORD-01", "2026-11-13")
        order.add_item_to_order(food, 1)
        self.assertEqual(order.calculate_bill(), 65000.0)

    def test_restaurant_manager_inheritance_and_mongodb_seed(self):
        self.assertTrue(issubclass(RestaurantManager, MenuService))
        self.assertTrue(issubclass(RestaurantManager, QueryService))
        self.assertTrue(issubclass(RestaurantManager, OrderReportService))
        self.assertTrue(issubclass(RestaurantManager, SearchSortOrderManager))

        manager = RestaurantManager(db_name="restaurant_bistro_test")
        try:
            self.assertEqual(len(manager.categories), 4)
            self.assertEqual(len(manager.menu_items), 80)
            for cat in manager.categories:
                cat_count = len([i for i in manager.menu_items if i.category_id == cat.category_id])
                self.assertEqual(cat_count, 20)
            self.assertEqual(len(manager.orders), 5)

            self.assertEqual(len(manager.display_all_items()), 80)
            self.assertEqual(manager.search_by_id("FD01").item_id, "FD01")
            self.assertEqual(len(manager.search_by_criteria()), 80)
            self.assertEqual(len(manager.sort_items()), 80)
            self.assertEqual(manager.calculate_bill([]), 0)
            self.assertGreater(manager.stat_total_revenue(), 0)
            self.assertEqual(len(manager.stat_revenue_by_category()), 4)
            self.assertEqual(len(manager.stat_top_ordered_items(limit=5)), 5)
        finally:
            manager._client.drop_database("restaurant_bistro_test")
            manager.close()

    def test_flask_five_routes_render(self):
        client = app.test_client()
        for path in ["/", "/manage", "/search-sort", "/orders", "/statistics"]:
            resp = client.get(path)
            self.assertEqual(resp.status_code, 200, f"Failed on {path}")


if __name__ == "__main__":
    unittest.main()
