import unittest

from services import RestaurantManager


class TestSearchSortOrder(unittest.TestCase):
    def setUp(self):
        self.manager = RestaurantManager()

    def test_search_filters_and_sorts(self):
        self.assertEqual(self.manager.search_by_id("FD01").item_id, "FD01")
        self.assertIsNone(self.manager.search_by_id("missing"))
        self.assertEqual(
            [item.item_id for item in self.manager.search_by_name("BÒ BÍT")],
            ["FD01"],
        )
        self.assertTrue(
            all(
                item.category_id == "CAT03"
                for item in self.manager.filter_by_category("CAT03")
            )
        )
        self.assertEqual(
            [item.item_id for item in self.manager.filter_by_price_range(66000, 66000)],
            ["DR01"],
        )

        by_price = self.manager.sort_by_price()
        self.assertEqual(
            [item.calculate_price() for item in by_price],
            sorted(item.calculate_price() for item in self.manager.menu_items),
        )
        by_name = self.manager.sort_by_name(reverse=True)
        self.assertEqual(
            [item.item_name.casefold() for item in by_name],
            sorted(
                (item.item_name.casefold() for item in self.manager.menu_items),
                reverse=True,
            ),
        )

    def test_create_order_calculates_total_and_saves_order(self):
        total = self.manager.create_order(
            "ORD-NEW",
            [
                {"item_id": "FD01", "quantity": 2},
                {"item_id": "DR01", "quantity": 1},
            ],
        )

        self.assertEqual(total, 556000)
        order = self.manager.orders[-1]
        self.assertEqual(order.order_id, "ORD-NEW")
        self.assertEqual(order.calculate_bill(), total)
        self.assertEqual([line["item_obj"].item_id for line in order.items], ["FD01", "DR01"])

    def test_create_order_rejects_missing_or_unavailable_items_atomically(self):
        initial_order_count = len(self.manager.orders)
        for item_id in ("missing", "FD05"):
            with self.subTest(item_id=item_id):
                with self.assertRaises(ValueError):
                    self.manager.create_order(
                        "ORD-INVALID",
                        [
                            {"item_id": "FD01", "quantity": 1},
                            {"item_id": item_id, "quantity": 1},
                        ],
                    )
                self.assertEqual(len(self.manager.orders), initial_order_count)

    def test_create_order_requires_positive_integer_quantities(self):
        for quantity in (0, -1, 1.5, True):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    self.manager.create_order(
                        "ORD-INVALID",
                        [{"item_id": "FD01", "quantity": quantity}],
                    )


if __name__ == "__main__":
    unittest.main()
