class OrderReportService:
    """Mixin service handling order creation and analytics reporting (Stubs for team integration)."""

    def create_order(self, order) -> None:
        # TODO: Gắn hàm xử lý tại đây
        pass

    def calculate_bill(self, order_items: list[dict]) -> float:
        # TODO: Gắn hàm xử lý tại đây
        pass

    def stat_total_revenue(self) -> float:
        # TODO: Gắn hàm xử lý tại đây
        pass

    def stat_revenue_by_category(self) -> list[dict]:
        # TODO: Gắn hàm xử lý tại đây
        pass

    def stat_top_ordered_items(self, limit: int = 5) -> list[dict]:
        # TODO: Gắn hàm xử lý tại đây
        pass
