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
│   ├── query_service.py       # Search & sort service interface
│   ├── order_report_service.py# Order & analytics service interface
│   ├── search_sort_order_manager.py # Search, sorting, and order workflows
│   └── restaurant_manager.py  # Facade + mock_data.json loader
├── static/
│   └── css/bistro.css         # POS & back-office styles
├── templates/                 # Jinja2 HTML templates
└── tests/
    ├── test_base.py           # Unit tests for models, manager, and all 5 routes
    └── test_search_sort_order.py # Search, sorting, and order workflow tests
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

- `SearchSortOrderManager` implements item search/filter/sort and order creation. `create_order` accepts an order ID and item lines such as `[{"item_id": "FD01", "quantity": 2}]`; it returns the calculated total and saves the order.
- Menu-management methods in `MenuService`, analytics methods in `OrderReportService`, and route handlers in `app.py` still contain TODO placeholders.
