"""Thực thể Order (đơn hàng) -  Hai.

Quy ước: MenuItem/FoodItem/DrinkItem do Khánh lập trình phải có
item_id, item_name, category_id và calculate_price() trả về đơn giá.
"""
from datetime import datetime
from decimal import Decimal, InvalidOperation
from numbers import Integral


class Order:
    """Lưu các món và số lượng; tính hóa đơn theo tính đa hình của món."""

    def __init__(self, order_id: str, order_date=None):
        self.order_id = order_id
        self.order_date = order_date if order_date is not None else datetime.now()
        self._items = []  # [{"item_obj": đối_tượng_món, "quantity": số_lượng}, ...]

    @property
    def order_id(self) -> str:
        return self._order_id

    @order_id.setter
    def order_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Mã đơn hàng phải là chuỗi không rỗng.")
        self._order_id = value.strip()

    @property
    def order_date(self) -> datetime:
        return self._order_date

    @order_date.setter
    def order_date(self, value) -> None:
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError as exc:
                raise ValueError("Ngày đơn hàng phải theo định dạng ISO 8601.") from exc
        if not isinstance(value, datetime):
            raise ValueError("Ngày đơn hàng phải là datetime hoặc chuỗi ISO 8601.")
        self._order_date = value

    @property
    def items(self) -> list:
        """Danh sách bản sao các dòng đơn (không cho sửa số lượng qua list gốc)."""
        return [line.copy() for line in self._items]

    @staticmethod
    def _unit_price(item_obj) -> Decimal:
        try:
            value = item_obj.calculate_price()
            result = Decimal(str(value))
        except (AttributeError, TypeError, ValueError, InvalidOperation) as exc:
            raise ValueError("Món phải có calculate_price() trả về số hợp lệ.") from exc
        if not result.is_finite() or result < 0:
            raise ValueError("Đơn giá món phải là số hữu hạn, không âm.")
        return result

    def add_item_to_order(self, item_obj, quantity: int) -> None:
        """Thêm món; nếu mã món đã tồn tại thì cộng số lượng."""
        if isinstance(quantity, bool) or not isinstance(quantity, Integral) or quantity <= 0:
            raise ValueError("Số lượng phải là số nguyên dương.")
        if item_obj is None or not callable(getattr(item_obj, "calculate_price", None)):
            raise ValueError("Món phải cung cấp phương thức calculate_price().")
        item_id = getattr(item_obj, "item_id", None)
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError("Món phải có item_id hợp lệ.")
        self._unit_price(item_obj)

        item_size = getattr(item_obj, "size", None)
        for line in self._items:
            if line["item_obj"].item_id == item_id and getattr(line["item_obj"], "size", None) == item_size:
                line["quantity"] += int(quantity)
                return
        self._items.append({"item_obj": item_obj, "quantity": int(quantity)})

    def calculate_bill(self) -> float:
        """Tổng tiền = tổng calculate_price() * quantity cho từng dòng."""
        total = sum(
            (self._unit_price(line["item_obj"]) * line["quantity"] for line in self._items),
            Decimal("0"),
        )
        return float(total)

    def to_dict(self) -> dict:
        """Chuyển dữ liệu sang dict chỉ chứa kiểu JSON-serializable."""
        lines = []
        for line in self._items:
            item = line["item_obj"]
            price = self._unit_price(item)
            quantity = line["quantity"]
            lines.append({
                "item_id": item.item_id,
                "item_name": getattr(item, "item_name", str(item.item_id)),
                "category_id": getattr(item, "category_id", None),
                "size": getattr(item, "size", None),
                "quantity": quantity,
                "unit_price": float(price),
                "subtotal": float(price * quantity),
            })
        return {
            "order_id": self.order_id,
            "order_date": self.order_date.isoformat(timespec="seconds"),
            "items": lines,
            "total": self.calculate_bill(),
        }

    def display_info(self) -> str:
        """Trả về hóa đơn dạng văn bản, dùng được cho Console hoặc Web."""
        data = self.to_dict()
        rows = [
            f"HÓA ĐƠN: {data['order_id']}",
            f"Ngày lập: {data['order_date']}",
            "-" * 76,
            f"{'Mã':<10} {'Tên món':<24} {'SL':>5} {'Đơn giá':>14} {'Thành tiền':>16}",
            "-" * 76,
        ]
        if not data["items"]:
            rows.append("(Đơn hàng chưa có món nào)")
        else:
            for line in data["items"]:
                rows.append(
                    f"{line['item_id']:<10} {line['item_name'][:24]:<24} "
                    f"{line['quantity']:>5} {line['unit_price']:>14,.0f} "
                    f"{line['subtotal']:>16,.0f}"
                )
        rows.extend(["-" * 76, f"TỔNG THANH TOÁN: {data['total']:,.0f} VNĐ"])
        return "\n".join(rows)

    def __str__(self) -> str:
        return self.display_info()
