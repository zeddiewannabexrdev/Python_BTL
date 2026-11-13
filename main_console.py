from models import DrinkItem, FoodItem
from services import RestaurantManager


def print_menu_header() -> None:
    print("\n" + "=" * 72)
    print("   L'ATELIER BISTRO — HỆ THỐNG QUẢN LÝ THỰC ĐƠN (CONSOLE SHELL)")
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


def print_items_table(manager: RestaurantManager) -> None:
    cat_map = {c.category_id: c.category_name for c in manager.categories}
    print(f"\n{'MÃ':<6} {'TÊN MÓN':<34} {'NHÓM':<18} {'LOẠI':<7} {'CHI TIẾT':<12} {'GIÁ GỐC':>11} {'TRẠNG THÁI':<10}")
    print("-" * 104)
    for item in manager.menu_items:
        item_type = "Food" if isinstance(item, FoodItem) else "Drink"
        detail = f"{item.preparation_time} phút" if isinstance(item, FoodItem) else f"Size {item.size}"
        status = "Còn món" if item.availability else "Hết món"
        cat_name = cat_map.get(item.category_id, item.category_id)
        print(
            f"{item.item_id:<6} {item.item_name[:33]:<34} {cat_name[:17]:<18} "
            f"{item_type:<7} {detail:<12} {item.price:>10,.0f}đ {status:<10}"
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
        item_id = read_non_empty("Nhập mã món (VD: FD07): ")
        # TODO: Gắn hàm xử lý tại đây
        manager.add_item(None)
        print(f"[Stub] Đã gọi RestaurantManager.add_item() cho mã '{item_id}'.")

    elif choice == 2:
        print("\n--- [2] CẬP NHẬT THÔNG TIN MÓN THEO MÃ ---")
        item_id = read_non_empty("Nhập mã món cần cập nhật: ")
        # TODO: Gắn hàm xử lý tại đây
        manager.update_item(item_id)
        print(f"[Stub] Đã gọi RestaurantManager.update_item('{item_id}').")

    elif choice == 3:
        print("\n--- [3] XÓA MÓN THEO MÃ ---")
        item_id = read_non_empty("Nhập mã món cần xóa: ")
        confirm = input(f"Bạn có chắc chắn muốn xóa mã '{item_id}'? (Y/N): ").strip().upper()
        if confirm == "Y":
            # TODO: Gắn hàm xử lý tại đây
            manager.delete_item(item_id)
            print(f"[Stub] Đã gọi RestaurantManager.delete_item('{item_id}').")
        else:
            print("Đã hủy thao tác xóa.")

    elif choice == 4:
        print("\n--- [4] DANH SÁCH THỰC ĐƠN THEO CỘT ---")
        # TODO: Gắn hàm xử lý tại đây
        manager.display_all_items()
        print_items_table(manager)

    elif choice == 5:
        print("\n--- [5] SẮP XẾP THỰC ĐƠN ---")
        by = input("Tiêu chí sắp xếp (price/name) [mặc định price]: ").strip() or "price"
        order = input("Thứ tự (ASC/DESC) [mặc định ASC]: ").strip().upper() or "ASC"
        # TODO: Gắn hàm xử lý tại đây
        manager.sort_items(by=by, ascending=(order == "ASC"))
        print(f"[Stub] Đã gọi RestaurantManager.sort_items(by='{by}', ascending={order == 'ASC'}).")

    elif choice == 6:
        print("\n--- [6] TÌM KIẾM CƠ BẢN (THEO MÃ CHÍNH XÁC) ---")
        item_id = read_non_empty("Nhập mã món cần tìm: ")
        # TODO: Gắn hàm xử lý tại đây
        manager.search_by_id(item_id)
        print(f"[Stub] Đã gọi RestaurantManager.search_by_id('{item_id}').")

    elif choice == 7:
        print("\n--- [7] ĐIỀU CHỈNH GIÁ/TRẠNG THÁI & LẬP ĐƠN HÀNG ---")
        print("  a. Điều chỉnh giá/trạng thái (adjust_price_and_status)")
        print("  b. Lập đơn hàng mới & tính tiền (create_order / calculate_bill)")
        sub = input("Chọn nhánh (a/b): ").strip().lower()
        if sub == "a":
            item_id = read_non_empty("Nhập mã món: ")
            # TODO: Gắn hàm xử lý tại đây
            manager.adjust_price_and_status(item_id)
            print(f"[Stub] Đã gọi RestaurantManager.adjust_price_and_status('{item_id}').")
        elif sub == "b":
            # TODO: Gắn hàm xử lý tại đây
            manager.create_order(None)
            manager.calculate_bill([])
            print("[Stub] Đã gọi RestaurantManager.create_order() & calculate_bill().")
        else:
            print("[Lỗi] Nhánh lựa chọn không hợp lệ (chỉ nhận 'a' hoặc 'b').")

    elif choice == 8:
        print("\n--- [8] TÌM KIẾM NÂNG CAO ---")
        keyword = input("Từ khóa tên món (Enter bỏ qua): ").strip()
        cat_id = input("Mã nhóm món (VD: CAT01, Enter bỏ qua): ").strip()
        # TODO: Gắn hàm xử lý tại đây
        manager.search_by_criteria(keyword=keyword, category_id=cat_id)
        print(f"[Stub] Đã gọi RestaurantManager.search_by_criteria(keyword='{keyword}', category_id='{cat_id}').")

    elif choice == 9:
        print("\n--- [9] THỐNG KÊ & BÁO CÁO ---")
        # TODO: Gắn hàm xử lý tại đây
        manager.stat_total_revenue()
        manager.stat_revenue_by_category()
        manager.stat_top_ordered_items()
        print("[Stub] Đã gọi stat_total_revenue(), stat_revenue_by_category(), stat_top_ordered_items().")

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
