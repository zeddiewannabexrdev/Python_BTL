import unittest

import app as web_app
from models import Category, DrinkItem, FoodItem
from services import RestaurantManager


class TestMenuServiceAndReports(unittest.TestCase):
    def setUp(self):
        self.db_name = "restaurant_bistro_test_mr"
        self.manager = RestaurantManager(db_name=self.db_name)

    def tearDown(self):
        self.manager._client.drop_database(self.db_name)
        self.manager.close()

    def test_add_update_adjust_delete_item(self):
        new_food = FoodItem("FD99", "Cơm chiên hải sản", 125000, "CAT01", True, preparation_time=14)
        self.manager.add_item(new_food)
        self.assertEqual(len(self.manager.display_all_items()), 81)
        self.assertEqual(self.manager.search_by_id("FD99").item_name, "Cơm chiên hải sản")

        # Verify MongoDB persistence across fresh manager instance
        reloaded = RestaurantManager(db_name=self.db_name, auto_seed=False)
        try:
            self.assertEqual(reloaded.search_by_id("FD99").item_name, "Cơm chiên hải sản")
        finally:
            reloaded.close()

        with self.assertRaises(ValueError):
            self.manager.add_item(new_food)

        self.manager.update_item("FD99", item_name="Cơm chiên đặc biệt", preparation_time=16)
        self.assertEqual(self.manager.search_by_id("FD99").item_name, "Cơm chiên đặc biệt")
        self.assertEqual(self.manager.search_by_id("FD99").preparation_time, 16)

        self.manager.adjust_price_and_status("FD99", new_price=135000, availability=False)
        item = self.manager.search_by_id("FD99")
        self.assertEqual(item.price, 135000.0)
        self.assertFalse(item.availability)

        removed = self.manager.delete_item("FD99")
        self.assertEqual(removed.item_id, "FD99")
        self.assertIsNone(self.manager.search_by_id("FD99"))

    def test_category_add_and_delete_integrity(self):
        with self.assertRaises(ValueError):
            self.manager.delete_category("CAT01")

        self.manager.add_category(Category("CAT05", "Món ăn kèm"))
        self.assertEqual(len(self.manager.categories), 5)

        removed = self.manager.delete_category("CAT05")
        self.assertEqual(removed.category_id, "CAT05")
        self.assertEqual(len(self.manager.categories), 4)

    def test_statistics_update_after_new_order(self):
        # 5 mock orders with DrinkItem size L multiplier (DR01: 66,000đ * 6 = +66,000đ vs base 2,985,000đ => 3,051,000đ)
        initial_revenue = self.manager.stat_total_revenue()
        self.assertEqual(initial_revenue, 3051000.0)

        by_cat = self.manager.stat_revenue_by_category()
        self.assertEqual(len(by_cat), 4)
        self.assertEqual(by_cat[0]["category_id"], "CAT01")

        top = self.manager.stat_top_ordered_items(limit=3)
        self.assertEqual(top[0]["item_id"], "DR01")
        self.assertEqual(top[0]["qty"], 6)

        added_total = self.manager.create_order("ORD99", [{"item_id": "FD01", "quantity": 2}])
        self.assertEqual(added_total, 490000.0)
        self.assertEqual(self.manager.stat_total_revenue(), initial_revenue + 490000.0)

    def test_drink_custom_size_when_ordering(self):
        # DR01 base price 55,000, default size L -> order 1x Size S (49,500) + 1x Size L (66,000)
        total = self.manager.create_order(
            "ORD-SIZE",
            [
                {"item_id": "DR01", "quantity": 1, "size": "S"},
                {"item_id": "DR01", "quantity": 1, "size": "L"},
            ],
        )
        self.assertEqual(total, 115500.0)
        order = self.manager.orders[-1]
        self.assertEqual(len(order.items), 2)
        self.assertEqual([line["size"] for line in order.to_dict()["items"]], ["S", "L"])
        # Original menu item size must remain unchanged
        self.assertEqual(self.manager.search_by_id("DR01").size, "L")

        with self.assertRaises(ValueError):
            self.manager.create_order("ORD-BAD-SIZE", [{"item_id": "DR01", "quantity": 1, "size": "XL"}])

        with self.assertRaises(ValueError):
            self.manager.create_order("ORD-FOOD-SIZE", [{"item_id": "FD01", "quantity": 1, "size": "M"}])

    def test_flask_live_crud_and_pos_endpoints(self):
        old_manager = web_app.manager
        web_app.manager = self.manager
        try:
            client = web_app.app.test_client()

            resp = client.post(
                "/manage",
                data={
                    "action": "add_item",
                    "item_type": "drink",
                    "item_id": "DR99",
                    "item_name": "Matcha Latte",
                    "category_id": "CAT03",
                    "price": "50000",
                    "size": "L",
                    "availability": "on",
                },
                follow_redirects=True,
            )
            self.assertEqual(resp.status_code, 200)
            self.assertIsNotNone(web_app.manager.search_by_id("DR99"))

            order_resp = client.post(
                "/orders",
                json={"order_id": "ORD-WEB", "items": [{"item_id": "DR99", "quantity": 2, "size": "S"}]},
            )
            self.assertEqual(order_resp.status_code, 201)
            data = order_resp.get_json()
            self.assertTrue(data["ok"])
            self.assertEqual(data["total"], 90000.0)
            self.assertEqual(data["order"]["items"][0]["size"], "S")

            stats_resp = client.get("/statistics")
            self.assertEqual(stats_resp.status_code, 200)
            self.assertIn("3.141.000đ", stats_resp.get_data(as_text=True))

            search_resp = client.get("/search-sort?exact_id=DR99")
            self.assertEqual(search_resp.status_code, 200)
            self.assertIn("Matcha Latte", search_resp.get_data(as_text=True))

            del_resp = client.post(
                "/manage",
                data={"action": "delete_item", "item_id": "DR99"},
                follow_redirects=True,
            )
            self.assertEqual(del_resp.status_code, 200)
            self.assertIsNone(web_app.manager.search_by_id("DR99"))
        finally:
            web_app.manager = old_manager


if __name__ == "__main__":
    unittest.main()
