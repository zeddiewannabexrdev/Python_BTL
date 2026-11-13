# L'Atelier Bistro — Restaurant Menu Management System

Ứng dụng quản lý thực đơn và gọi món (POS & Back-office) xây dựng theo kiến trúc OOP bằng Python (Flask, Jinja2, TailwindCSS, Alpine.js).

## Cấu trúc dự án

```text
Python/
├── app.py                     # Khởi chạy Flask Web (5 routes: /, /manage, /search-sort, /orders, /statistics)
├── main_console.py            # Giao diện Console tương tác (Menu 1-10)
├── requirements.txt           # Thư viện phụ thuộc (Flask, Jinja2)
├── data/
│   └── mock_data.json         # Dữ liệu mẫu: 4 danh mục, 10 món ăn/đồ uống, 5 hóa đơn
├── models/
│   ├── category.py            # Lớp Category
│   ├── menu_item.py           # Lớp trừu tượng MenuItem (ABC), FoodItem, DrinkItem
│   └── order.py               # Lớp Order
├── services/
│   ├── menu_service.py        # Stub quản lý thực đơn & danh mục
│   ├── query_service.py       # Stub tìm kiếm & sắp xếp
│   ├── order_report_service.py# Stub tạo đơn hàng & thống kê
│   └── restaurant_manager.py  # Lớp tổng hợp đa kế thừa + nạp mock_data.json
├── static/
│   └── css/bistro.css         # CSS giao diện POS
├── templates/                 # Giao diện Web Jinja2
└── tests/
    └── test_base.py           # Unit tests kiểm tra model, service stubs và 5 routes
```

## Cài đặt & Chạy thử

1. **Tạo môi trường ảo và cài thư viện:**
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   # source .venv/bin/activate

   pip install -r requirements.txt
   ```

2. **Chạy Web App (Flask):**
   ```bash
   python app.py
   ```
   Truy cập trình duyệt tại `http://127.0.0.1:5000`.

3. **Chạy Console App:**
   ```bash
   python main_console.py
   ```

4. **Chạy kiểm thử (Unit Tests):**
   ```bash
   python -m unittest discover -s tests -v
   ```

## Ghi chú phát triển nhóm

- Các hàm xử lý nghiệp vụ trong `services/` (`MenuService`, `QueryService`, `OrderReportService`) và các route POST/GET trong `app.py` hiện đang để sẵn comment `# TODO: Gắn hàm xử lý tại đây` để các thành viên ghép logic độc lập, tránh xung đột Git.
