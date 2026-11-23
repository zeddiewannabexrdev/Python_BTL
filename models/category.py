"""Thực thể Category (danh mục món ăn/đồ uống) - Hai."""


class Category:
    """Đóng gói mã và tên danh mục, bảo đảm không được rỗng."""

    def __init__(self, category_id: str, category_name: str):
        self.category_id = category_id
        self.category_name = category_name

    @staticmethod
    def _validate_text(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} phải là chuỗi không rỗng.")
        return value.strip()

    @property
    def category_id(self) -> str:
        return self._category_id

    @category_id.setter
    def category_id(self, value: str) -> None:
        self._category_id = self._validate_text(value, "Mã danh mục")

    @property
    def category_name(self) -> str:
        return self._category_name

    @category_name.setter
    def category_name(self, value: str) -> None:
        self._category_name = self._validate_text(value, "Tên danh mục")

    def display_info(self) -> str:
        """Trả về chuỗi mô tả; tầng Console/Web quyết định cách hiển thị."""
        return f"Mã danh mục: {self.category_id} | Tên danh mục: {self.category_name}"

    def __str__(self) -> str:
        return self.display_info()

    def to_dict(self) -> dict:
        return {"category_id": self.category_id, "category_name": self.category_name}