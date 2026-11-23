from datetime import datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from models import Category, DrinkItem, FoodItem
from services import RestaurantManager

app = Flask(__name__)
app.secret_key = "latelier-bistro-dev-secret"

manager = RestaurantManager()


def _fmt_vnd(amount: float) -> str:
    return f"{amount:,.0f}".replace(",", ".") + "đ"


def _category_map() -> dict[str, str]:
    return {cat.category_id: cat.category_name for cat in manager.categories}


def _next_order_id() -> str:
    existing = {o.order_id for o in manager.orders}
    idx = len(manager.orders) + 1
    while f"ORD{idx:02d}" in existing:
        idx += 1
    return f"ORD{idx:02d}"


def _build_live_analytics() -> dict:
    total_revenue = manager.stat_total_revenue()
    total_orders = len(manager.orders)
    avg_order = (total_revenue / total_orders) if total_orders > 0 else 0.0
    active_items = len([i for i in manager.menu_items if i.availability])

    rev_by_cat = [
        {
            "category_id": row["category_id"],
            "category_name": row["category_name"],
            "orders": row["orders"],
            "revenue": _fmt_vnd(row["revenue"]),
            "share": row["share"],
        }
        for row in manager.stat_revenue_by_category()
    ]
    top_items = [
        {
            "item_id": row["item_id"],
            "item_name": row["item_name"],
            "category_name": row["category_name"],
            "qty": row["qty"],
            "revenue": _fmt_vnd(row["revenue"]),
        }
        for row in manager.stat_top_ordered_items(limit=5)
    ]

    return {
        "kpis": {
            "total_revenue": _fmt_vnd(total_revenue),
            "total_orders": total_orders,
            "avg_order_value": _fmt_vnd(avg_order),
            "active_items": active_items,
            "total_items": len(manager.menu_items),
        },
        "revenue_by_category": rev_by_cat,
        "top_items": top_items,
    }


@app.route("/")
def index_view():
    items = manager.display_all_items()
    return render_template(
        "index.html",
        active_tab="overview",
        items=items,
        categories=manager.categories,
        category_map=_category_map(),
    )


@app.route("/manage", methods=["GET", "POST"])
def manage_view():
    if request.method == "POST":
        action = request.form.get("action", "").strip()
        try:
            if action == "add_item":
                item_type = request.form.get("item_type", "food").strip().lower()
                item_id = request.form.get("item_id", "").strip()
                item_name = request.form.get("item_name", "").strip()
                category_id = request.form.get("category_id", "").strip()
                price = float(request.form.get("price", 0))
                availability = request.form.get("availability") in ("on", "true", "1")
                if item_type == "drink":
                    size = request.form.get("size", "M").strip().upper()
                    item = DrinkItem(item_id, item_name, price, category_id, availability, size=size)
                else:
                    prep_time = int(request.form.get("preparation_time", 15))
                    item = FoodItem(item_id, item_name, price, category_id, availability, preparation_time=prep_time)
                manager.add_item(item)
                flash(f"Đã thêm món {item.item_id} — {item.item_name}.", "success")

            elif action == "update_item":
                item_id = request.form.get("item_id", "").strip()
                item_name = request.form.get("item_name", "").strip()
                category_id = request.form.get("category_id", "").strip()
                price = float(request.form.get("price", 0))
                availability = request.form.get("availability") in ("on", "true", "1")
                kwargs = {
                    "item_name": item_name,
                    "category_id": category_id,
                    "price": price,
                    "availability": availability,
                }
                if request.form.get("preparation_time"):
                    kwargs["preparation_time"] = int(request.form.get("preparation_time"))
                if request.form.get("size"):
                    kwargs["size"] = request.form.get("size").strip().upper()
                manager.update_item(item_id, **kwargs)
                flash(f"Đã cập nhật món {item_id}.", "success")

            elif action == "delete_item":
                item_id = request.form.get("item_id", "").strip()
                removed = manager.delete_item(item_id)
                flash(f"Đã xóa món {removed.item_id} — {removed.item_name}.", "success")

            elif action == "add_category":
                cat_id = request.form.get("category_id", "").strip()
                cat_name = request.form.get("category_name", "").strip()
                manager.add_category(Category(cat_id, cat_name))
                flash(f"Đã thêm danh mục {cat_id} — {cat_name}.", "success")

            elif action == "delete_category":
                cat_id = request.form.get("category_id", "").strip()
                removed = manager.delete_category(cat_id)
                flash(f"Đã xóa danh mục {removed.category_id}.", "success")
            else:
                flash("Thao tác không hợp lệ.", "error")
        except (ValueError, TypeError) as exc:
            flash(str(exc), "error")
        return redirect(url_for("manage_view"))

    return render_template(
        "manage.html",
        active_tab="manage",
        items=manager.display_all_items(),
        categories=manager.categories,
        category_map=_category_map(),
    )


@app.route("/search-sort", methods=["GET"])
def search_sort_view():
    exact_id = request.args.get("exact_id", "").strip()
    keyword = request.args.get("keyword", "").strip()
    category_id = request.args.get("category_id", "").strip()
    raw_min = request.args.get("min_price", "").strip()
    raw_max = request.args.get("max_price", "").strip()
    sort_by = request.args.get("sort_by", "price").strip() or "price"
    sort_order = request.args.get("sort_order", "ASC").strip().upper() or "ASC"

    try:
        min_price = float(raw_min) if raw_min else None
        max_price = float(raw_max) if raw_max else None
        if exact_id:
            found = manager.search_by_id(exact_id)
            items = [found] if found else []
        elif keyword or category_id or min_price is not None or max_price is not None:
            items = manager.search_by_criteria(
                keyword=keyword,
                category_id=category_id,
                min_price=min_price,
                max_price=max_price,
            )
            ascending = sort_order == "ASC"
            if sort_by == "name":
                items = sorted(items, key=lambda i: i.item_name.casefold(), reverse=not ascending)
            else:
                items = sorted(items, key=lambda i: i.calculate_price(), reverse=not ascending)
        else:
            items = manager.sort_items(by=sort_by, ascending=(sort_order == "ASC"))
    except ValueError as exc:
        flash(str(exc), "error")
        items = manager.display_all_items()

    return render_template(
        "search_sort.html",
        active_tab="search_sort",
        items=items,
        categories=manager.categories,
        category_map=_category_map(),
        filters={
            "exact_id": exact_id,
            "keyword": keyword,
            "category_id": category_id,
            "min_price": raw_min,
            "max_price": raw_max,
            "sort_by": sort_by,
            "sort_order": sort_order,
        },
    )


@app.route("/orders", methods=["GET", "POST"])
def orders_view():
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        order_id = (payload.get("order_id") or "").strip() or _next_order_id()
        items = payload.get("items") or []
        if not items:
            return jsonify({"ok": False, "error": "Đơn hàng phải có ít nhất 1 món."}), 400
        try:
            total = manager.create_order(order_id, items)
            created = manager.orders[-1].to_dict()
            return jsonify({"ok": True, "order_id": order_id, "total": total, "order": created}), 201
        except (ValueError, TypeError) as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400

    live_orders = [order.to_dict() for order in reversed(manager.orders)]
    return render_template(
        "orders.html",
        active_tab="orders",
        items=manager.display_all_items(),
        categories=manager.categories,
        category_map=_category_map(),
        orders=live_orders,
        next_order_id=_next_order_id(),
        now_label=datetime.now().strftime("%d/%m/%Y"),
    )


@app.route("/statistics")
def statistics_view():
    return render_template(
        "statistics.html",
        active_tab="statistics",
        analytics=_build_live_analytics(),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
