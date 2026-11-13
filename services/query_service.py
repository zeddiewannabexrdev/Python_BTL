class QueryService:
    """Mixin service handling menu search and sorting (Stubs for team integration)."""

    def search_by_id(self, item_id: str):
        # TODO: Gắn hàm xử lý tại đây
        pass

    def search_by_criteria(
        self,
        keyword: str = "",
        category_id: str = "",
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> list:
        # TODO: Gắn hàm xử lý tại đây
        pass

    def sort_items(self, by: str = "price", ascending: bool = True) -> list:
        # TODO: Gắn hàm xử lý tại đây
        pass
