# L'Atelier Bistro — Restaurant Menu Management System

A restaurant menu management and Point-of-Sale (POS & Back-office) application built with an OOP architecture in Python (Flask, Jinja2, TailwindCSS, Alpine.js).

## Project Structure

```text
Python/
├── app.py                     # Flask web entry point (5 routes: /, /manage, /search-sort, /orders, /statistics)
├── main_console.py            # Interactive CLI console menu (options 1-10)
├── requirements.txt           # Dependencies (Flask, Jinja2)
├── data/
│   └── mock_data.json         # Sample data: 4 categories, 10 menu items, 5 orders
├── models/
│   ├── category.py            # Category class
│   ├── menu_item.py           # Abstract MenuItem (ABC), FoodItem, DrinkItem
│   └── order.py               # Order class
├── services/
│   ├── menu_service.py        # Menu & category management stubs
│   ├── query_service.py       # Search & sort stubs
│   ├── order_report_service.py# Order & analytics stubs
│   └── restaurant_manager.py  # Multiple-inheritance facade + mock_data.json loader
├── static/
│   └── css/bistro.css         # POS & back-office styles
├── templates/                 # Jinja2 HTML templates
└── tests/
    └── test_base.py           # Unit tests for models, service stubs, and all 5 routes
```

## Setup & Usage

1. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   # source .venv/bin/activate

   pip install -r requirements.txt
   ```

2. **Run the Flask Web App:**
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.

3. **Run the Console App:**
   ```bash
   python main_console.py
   ```

4. **Run Unit Tests:**
   ```bash
   python -m unittest discover -s tests -v
   ```

## Team Integration Notes

- Business logic methods in `services/` (`MenuService`, `QueryService`, `OrderReportService`) and route handlers in `app.py` contain `# TODO: Gắn hàm xử lý tại đây` placeholders so team members can implement modules independently without Git conflicts.
