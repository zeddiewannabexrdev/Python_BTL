from flask import Flask, render_template

from services import RestaurantManager

app = Flask(__name__)

# Khởi tạo facade quản lý dữ liệu mẫu từ data/mock_data.json
manager = RestaurantManager()


def _build_static_stats_preview():
    """Tạo dữ liệu hiển thị tĩnh cho trang Thống kê từ mock_data.json (chưa gọi stub service)."""
    return {
        "kpis": {
            "total_revenue": "2.985.000đ",
            "total_orders": len(manager.raw_orders),
            "avg_order_value": "597.000đ",
            "active_items": len([i for i in manager.menu_items if i.availability]),
        },
        "revenue_by_category": [
            {"category_id": "CAT01", "category_name": "Món chính", "orders": 8, "revenue": "1.905.000đ", "share": 64},
            {"category_id": "CAT03", "category_name": "Đồ uống pha chế", "orders": 9, "revenue": "480.000đ", "share": 16},
            {"category_id": "CAT02", "category_name": "Khai vị & Ăn kèm", "orders": 3, "revenue": "345.000đ", "share": 12},
            {"category_id": "CAT04", "category_name": "Tráng miệng", "orders": 3, "revenue": "255.000đ", "share": 8},
        ],
        "top_items": [
            {"item_id": "DR01", "item_name": "Trà đào cam sả", "category_name": "Đồ uống pha chế", "qty": 6, "revenue": "330.000đ"},
            {"item_id": "FD02", "item_name": "Cá hồi áp chảo sốt bơ chanh", "category_name": "Món chính", "qty": 3, "revenue": "840.000đ"},
            {"item_id": "FD01", "item_name": "Bò bít tết sốt tiêu đen", "category_name": "Món chính", "qty": 3, "revenue": "735.000đ"},
            {"item_id": "FD04", "item_name": "Salad Caesar ức gà nướng", "category_name": "Khai vị & Ăn kèm", "qty": 3, "revenue": "345.000đ"},
            {"item_id": "FD06", "item_name": "Tiramisu cổ điển vị Espresso", "category_name": "Tráng miệng", "qty": 3, "revenue": "255.000đ"},
        ],
    }


def _category_map() -> dict[str, str]:
    return {cat.category_id: cat.category_name for cat in manager.categories}


def _item_map() -> dict[str, object]:
    return {item.item_id: item for item in manager.menu_items}


@app.route("/")
def index_view():
    # TODO: Gắn hàm xử lý tại đây (manager.display_all_items)
    return render_template(
        "index.html",
        active_tab="overview",
        items=manager.menu_items,
        categories=manager.categories,
        category_map=_category_map(),
    )


@app.route("/manage", methods=["GET", "POST"])
def manage_view():
    # TODO: Gắn hàm xử lý tại đây (manager.add_item / update_item / delete_item / adjust_price_and_status)
    return render_template(
        "manage.html",
        active_tab="manage",
        items=manager.menu_items,
        categories=manager.categories,
        category_map=_category_map(),
    )


@app.route("/search-sort", methods=["GET"])
def search_sort_view():
    # TODO: Gắn hàm xử lý tại đây (manager.search_by_id / search_by_criteria / sort_items)
    return render_template(
        "search_sort.html",
        active_tab="search_sort",
        items=manager.menu_items,
        categories=manager.categories,
        category_map=_category_map(),
    )


@app.route("/orders", methods=["GET", "POST"])
def orders_view():
    # TODO: Gắn hàm xử lý tại đây (manager.create_order / calculate_bill)
    return render_template(
        "orders.html",
        active_tab="orders",
        items=manager.menu_items,
        categories=manager.categories,
        category_map=_category_map(),
        item_map=_item_map(),
        orders=manager.raw_orders,
    )


@app.route("/statistics")
def statistics_view():
    # TODO: Gắn hàm xử lý tại đây (manager.stat_total_revenue / stat_revenue_by_category / stat_top_ordered_items)
    return render_template(
        "statistics.html",
        active_tab="statistics",
        analytics=_build_static_stats_preview(),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
