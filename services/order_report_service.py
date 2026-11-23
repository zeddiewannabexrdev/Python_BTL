from decimal import Decimal


class OrderReportService:
    """Mixin service handling order creation and analytics reporting."""

    def create_order(self, order) -> None:
        # Overridden by SearchSortOrderManager
        pass

    def calculate_bill(self, order_items: list[dict]) -> float:
        # Overridden by SearchSortOrderManager
        pass

    def stat_total_revenue(self) -> float:
        total = sum((Decimal(str(order.calculate_bill())) for order in self._orders), Decimal("0"))
        return float(total)

    def stat_revenue_by_category(self) -> list[dict]:
        cat_stats: dict[str, dict] = {
            cat.category_id: {
                "category_id": cat.category_id,
                "category_name": cat.category_name,
                "orders": 0,
                "revenue": Decimal("0"),
            }
            for cat in self._categories
        }

        for order in self._orders:
            for line in order.to_dict()["items"]:
                cat_id = line["category_id"] or "UNKNOWN"
                if cat_id not in cat_stats:
                    cat_stats[cat_id] = {
                        "category_id": cat_id,
                        "category_name": cat_id,
                        "orders": 0,
                        "revenue": Decimal("0"),
                    }
                cat_stats[cat_id]["orders"] += int(line["quantity"])
                cat_stats[cat_id]["revenue"] += Decimal(str(line["subtotal"]))

        total_rev = sum((entry["revenue"] for entry in cat_stats.values()), Decimal("0"))
        results = []
        for entry in cat_stats.values():
            rev_float = float(entry["revenue"])
            share = round((entry["revenue"] / total_rev) * 100) if total_rev > 0 else 0
            results.append({
                "category_id": entry["category_id"],
                "category_name": entry["category_name"],
                "orders": entry["orders"],
                "revenue": rev_float,
                "share": int(share),
            })

        results.sort(key=lambda row: (-row["revenue"], row["category_id"]))
        return results

    def stat_top_ordered_items(self, limit: int = 5) -> list[dict]:
        cat_map = {cat.category_id: cat.category_name for cat in self._categories}
        item_stats: dict[str, dict] = {}

        for order in self._orders:
            for line in order.to_dict()["items"]:
                item_id = line["item_id"]
                if item_id not in item_stats:
                    cat_id = line["category_id"]
                    item_stats[item_id] = {
                        "item_id": item_id,
                        "item_name": line["item_name"],
                        "category_name": cat_map.get(cat_id, cat_id or ""),
                        "qty": 0,
                        "revenue": Decimal("0"),
                    }
                item_stats[item_id]["qty"] += int(line["quantity"])
                item_stats[item_id]["revenue"] += Decimal(str(line["subtotal"]))

        ranked = sorted(
            item_stats.values(),
            key=lambda row: (-row["qty"], -row["revenue"], row["item_id"]),
        )
        return [
            {
                "item_id": row["item_id"],
                "item_name": row["item_name"],
                "category_name": row["category_name"],
                "qty": row["qty"],
                "revenue": float(row["revenue"]),
            }
            for row in ranked[:limit]
        ]
