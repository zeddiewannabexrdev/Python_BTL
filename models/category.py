class Category:
    """Represents a menu category."""

    def __init__(self, category_id: str, category_name: str) -> None:
        self._category_id = category_id
        self._category_name = category_name

    @property
    def category_id(self) -> str:
        return self._category_id

    @category_id.setter
    def category_id(self, value: str) -> None:
        self._category_id = value

    @property
    def category_name(self) -> str:
        return self._category_name

    @category_name.setter
    def category_name(self, value: str) -> None:
        self._category_name = value

    def __str__(self) -> str:
        return f"[{self._category_id}] {self._category_name}"
