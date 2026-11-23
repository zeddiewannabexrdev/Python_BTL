from models import DrinkItem, FoodItem
from services import RestaurantManager


def print_menu_header() -> None:
    print("\n" + "=" * 72)
    print("   L'ATELIER BISTRO — HỆ THỐNG QUẢN LÝ THỰC ĐƠN (CONSOLE)")
    print("=" * 72)
    print("  1.  Thêm mới món ăn / đồ uống")
    print("  2.  Cập nhật thông tin món theo mã")
    print("  3.  Xóa món theo mã (có xác nhận Y/N)")
    print("  4.  Hiển thị danh sách thực đơn theo cột")
    print("  5.  Sắp xếp thực đơn (Giá / Tên, Tăng / Giảm dần)")
    print("  6.  Tìm kiếm cơ bản (theo mã chính xác)")
    print("  7.  Nghiệp vụ đặc thù: Điều chỉnh giá/trạng thái & Lập đơn hàng mới")
    print("  8.  Tìm kiếm nâng cao (theo tên, nhóm món, khoảng giá)")
    print("  9.  Thống kê & Báo cáo (Tổng doanh thu, nhóm món, top món)")
    print("  10. Thoát chương trình an toàn (nhập 0 hoặc 10)")
    print("-" * 72)


def print_items_table(items: list, manager: RestaurantManager) -> None:
    if not items:
        print("(Danh sách trống)")
        return
    cat_map = {c.category_id: c.category_name for c in manager.categories}
    print(f"\n{'MÃ':<6} {'TÊN MÓN':<32} {'NHÓM':<18} {'LOẠI':<7} {'CHI TIẾT':<10} {'GIÁ BÁN':>11} {'TRẠNG THÁI':<10}")
    print("-" * 102)
    for item in items:
        item_type = "Food" if isinstance(item, FoodItem) else "Drink"
        detail = f"{item.preparation_time} phút" if isinstance(item, FoodItem) else f"Size {item.size}"
        status = "Còn món" if item.availability else "Hết món"
        cat_name = cat_map.get(item.category_id, item.category_id)
        print(
            f"{item.item_id:<6} {item.item_name[:31]:<32} {cat_name[:17]:<18} "
            f"{item_type:<7} {detail:<10} {item.calculate_price():>10,.0f}đ {status:<10}"
        )


def read_menu_choice() -> int:
    while True:
        try:
            raw = input("Nhập lựa chọn của bạn (0-10): ").strip()
            if not raw:
                print("[Lỗi] Không được để trống lựa chọn. Vui lòng nhập số từ 0 đến 10.")
                continue
            choice = int(raw)
            if choice < 0 or choice > 10:
                print("[Lỗi] Lựa chọn ngoài phạm vi (0-10). Vui lòng nhập lại.")
                continue
            return choice
        except ValueError:
            print("[Lỗi] Dữ liệu nhập không phải số nguyên hợp lệ. Vui lòng thử lại.")


def read_non_empty(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("[Lỗi] Giá trị không được để trống. Vui lòng nhập lại.")


def handle_choice(choice: int, manager: RestaurantManager) -> bool:
    if choice in (0, 10):
        print("Đang thoát chương trình an toàn. Tạm biệt!")
        return False

    if choice == 1:
        print("\n--- [1] THÊM MỚI MÓN ĂN / ĐỒ UỐNG ---")
        item_type = read_non_empty("Loại món (food/drink): ").lower()
        item_id = read_non_empty("Nhập mã món (VD: FD07): ")
        item_name = read_non_empty("Nhập tên món: ")
        cat_id = read_non_empty("Nhập mã danh mục (VD: CAT01): ")
        price = float(read_non_empty("Nhập giá gốc (VNĐ): "))
        if item_type == "drink":
            size = read_non_empty("Nhập kích cỡ (S/M/L): ").upper()
            item = DrinkItem(item_id, item_name, price, cat_id, True, size=size)
        elif item_type == "food":
            prep = int(read_non_empty("Nhập thời gian chế biến (phút): "))
            item = FoodItem(item_id, item_name, price, cat_id, True, preparation_time=prep)
        else:
            raise ValueError("Loại món chỉ nhận 'food' hoặc 'drink'.")
        manager.add_item(item)
        print(f"Đã thêm thành công: {item.display_info()}")

    elif choice == 2:
        print("\n--- [2] CẬP NHẬT THÔNG TIN MÓN THEO MÃ ---")
        item_id = read_non_empty("Nhập mã món cần cập nhật: ")
        new_name = input("Tên món mới (Enter giữ nguyên): ").strip() or None
        raw_price = input("Giá gốc mới (Enter giữ nguyên): ").strip()
        new_price = float(raw_price) if raw_price else None
        updated = manager.update_item(item_id, item_name=new_name, price=new_price)
        print(f"Đã cập nhật: {updated.display_info()}")

    elif choice == 3:
        print("\n--- [3] XÓA MÓN THEO MÃ ---")
        item_id = read_non_empty("Nhập mã món cần xóa: ")
        confirm = input(f"Bạn có chắc chắn muốn xóa mã '{item_id}'? (Y/N): ").strip().upper()
        if confirm == "Y":
            removed = manager.delete_item(item_id)
            print(f"Đã xóa món: {removed.item_id} — {removed.item_name}")
        else:
            print("Đã hủy thao tác xóa.")

    elif choice == 4:
        print("\n--- [4] DANH SÁCH THỰC ĐƠN THEO CỘT ---")
        print_items_table(manager.display_all_items(), manager)

    elif choice == 5:
        print("\n--- [5] SẮP XẾP THỰC ĐƠN ---")
        by = input("Tiêu chí sắp xếp (price/name) [mặc định price]: ").strip() or "price"
        order = input("Thứ tự (ASC/DESC) [mặc định ASC]: ").strip().upper() or "ASC"
        sorted_items = manager.sort_items(by=by, ascending=(order == "ASC"))
        print_items_table(sorted_items, manager)

    elif choice == 6:
        print("\n--- [6] TÌM KIẾM CƠ BẢN (THEO MÃ CHÍNH XÁC) ---")
        item_id = read_non_empty("Nhập mã món cần tìm: ")
        found = manager.search_by_id(item_id)
        if found:
            print(found.display_info())
        else:
            print(f"Không tìm thấy món có mã '{item_id}'.")

    elif choice == 7:
        print("\n--- [7] ĐIỀU CHỈNH GIÁ/TRẠNG THÁI & LẬP ĐƠN HÀNG ---")
        print("  a. Điều chỉnh giá / trạng thái phục vụ")
        print("  b. Lập đơn hàng mới & tính tiền")
        sub = input("Chọn nhánh (a/b): ").strip().lower()
        if sub == "a":
            item_id = read_non_empty("Nhập mã món: ")
            raw_price = input("Giá mới (Enter bỏ qua): ").strip()
            raw_avail = input("Trạng thái còn món? (Y/N, Enter bỏ qua): ").strip().upper()
            new_price = float(raw_price) if raw_price else None
            avail = True if raw_avail == "Y" else (False if raw_avail == "N" else None)
            updated = manager.adjust_price_and_status(item_id, new_price=new_price, availability=avail)
            print(f"Đã cập nhật: {updated.display_info()}")
        elif sub == "b":
            order_id = read_non_empty("Nhập mã đơn hàng: ")
            raw_items = read_non_empty(
                "Nhập món dạng MÃ_MÓN:SỐ_LƯỢNG hoặc MÃ_MÓN:SỐ_LƯỢNG:SIZE (VD: FD01:1,DR01:2:S): "
            )
            items = []
            for entry in raw_items.split(","):
                parts = [p.strip() for p in entry.strip().split(":")]
                if len(parts) not in (2, 3) or not parts[0]:
                    raise ValueError("Mỗi món phải có dạng MÃ_MÓN:SỐ_LƯỢNG hoặc MÃ_MÓN:SỐ_LƯỢNG:SIZE.")
                line = {"item_id": parts[0], "quantity": int(parts[1])}
                if len(parts) == 3 and parts[2]:
                    line["size"] = parts[2].upper()
                items.append(line)
            total = manager.create_order(order_id, items)
            print(f"Đã lập đơn '{order_id}'. Tổng tiền: {total:,.0f}đ.")
        else:
            print("[Lỗi] Nhánh lựa chọn không hợp lệ (chỉ nhận 'a' hoặc 'b').")

    elif choice == 8:
        print("\n--- [8] TÌM KIẾM NÂNG CAO ---")
        keyword = input("Từ khóa tên món (Enter bỏ qua): ").strip()
        cat_id = input("Mã nhóm món (VD: CAT01, Enter bỏ qua): ").strip()
        raw_min = input("Giá tối thiểu (Enter bỏ qua): ").strip()
        raw_max = input("Giá tối đa (Enter bỏ qua): ").strip()
        results = manager.search_by_criteria(
            keyword=keyword,
            category_id=cat_id,
            min_price=float(raw_min) if raw_min else None,
            max_price=float(raw_max) if raw_max else None,
        )
        print_items_table(results, manager)

    elif choice == 9:
        print("\n--- [9] THỐNG KÊ & BÁO CÁO ---")
        total_rev = manager.stat_total_revenue()
        print(f"Tổng doanh thu ({len(manager.orders)} hóa đơn): {total_rev:,.0f}đ")
        print("\nDoanh thu theo nhóm món:")
        for row in manager.stat_revenue_by_category():
            print(f"  - [{row['category_id']}] {row['category_name']:<20}: {row['revenue']:>10,.0f}đ ({row['share']}%, {row['orders']} phần)")
        print("\nTop món đặt nhiều nhất:")
        for idx, row in enumerate(manager.stat_top_ordered_items(limit=5), start=1):
            print(f"  #{idx} [{row['item_id']}] {row['item_name']:<30}: {row['qty']} phần | {row['revenue']:>10,.0f}đ")

    return True


def main() -> None:
    manager = RestaurantManager()
    print(
        f"Đã nạp dữ liệu mẫu: {len(manager.categories)} nhóm món, "
        f"{len(manager.menu_items)} món ăn/đồ uống, {len(manager.orders)} hóa đơn."
    )

    while True:
        try:
            print_menu_header()
            choice = read_menu_choice()
            if not handle_choice(choice, manager):
                break
        except (KeyboardInterrupt, EOFError):
            print("\nNhận tín hiệu ngắt (Ctrl+C / EOF). Đang thoát chương trình an toàn.")
            break
        except Exception as exc:
            print(f"[Lỗi hệ thống] {exc}. Quay lại menu chính.")


if __name__ == "__main__":
    main()
