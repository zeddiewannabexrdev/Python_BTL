"""Seed MongoDB database with 4 categories, 80 menu items (20 per category), and 5 sample orders."""
import argparse
import os
from pymongo import MongoClient

DEFAULT_MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DEFAULT_DB_NAME = os.getenv("MONGO_DB", "restaurant_bistro_db")

SEED_CATEGORIES = [
    {"category_id": "CAT01", "category_name": "Món chính"},
    {"category_id": "CAT02", "category_name": "Khai vị & Ăn kèm"},
    {"category_id": "CAT03", "category_name": "Đồ uống pha chế"},
    {"category_id": "CAT04", "category_name": "Tráng miệng"},
]

SEED_MENU_ITEMS = [
    # === CAT01: Món chính (20 món) ===
    {"item_id": "FD01", "item_name": "Bò bít tết sốt tiêu đen", "item_type": "Food", "price": 245000, "category_id": "CAT01", "availability": True, "preparation_time": 18},
    {"item_id": "FD02", "item_name": "Cá hồi áp chảo sốt bơ chanh", "item_type": "Food", "price": 280000, "category_id": "CAT01", "availability": True, "preparation_time": 20},
    {"item_id": "FD03", "item_name": "Mì Ý hải sản sốt kem nấm", "item_type": "Food", "price": 165000, "category_id": "CAT01", "availability": True, "preparation_time": 15},
    {"item_id": "MC04", "item_name": "Sườn cừu nướng thảo mộc", "item_type": "Food", "price": 340000, "category_id": "CAT01", "availability": True, "preparation_time": 25},
    {"item_id": "MC05", "item_name": "Ức vịt áp chảo sốt cam mật ong", "item_type": "Food", "price": 235000, "category_id": "CAT01", "availability": True, "preparation_time": 22},
    {"item_id": "MC06", "item_name": "Gà nướng mật ong lá hương thảo", "item_type": "Food", "price": 175000, "category_id": "CAT01", "availability": True, "preparation_time": 20},
    {"item_id": "MC07", "item_name": "Bò hầm rượu vang đỏ kiểu Pháp", "item_type": "Food", "price": 260000, "category_id": "CAT01", "availability": True, "preparation_time": 25},
    {"item_id": "MC08", "item_name": "Mì Ý sốt bò bằm Bolognese", "item_type": "Food", "price": 135000, "category_id": "CAT01", "availability": True, "preparation_time": 14},
    {"item_id": "MC09", "item_name": "Mì Ý Carbonara thịt xông khói", "item_type": "Food", "price": 145000, "category_id": "CAT01", "availability": True, "preparation_time": 14},
    {"item_id": "MC10", "item_name": "Cơm risotto nấm Truffle đen", "item_type": "Food", "price": 210000, "category_id": "CAT01", "availability": True, "preparation_time": 22},
    {"item_id": "MC11", "item_name": "Cơm risotto hải sản nghệ tây", "item_type": "Food", "price": 225000, "category_id": "CAT01", "availability": True, "preparation_time": 22},
    {"item_id": "MC12", "item_name": "Sườn heo nướng BBQ tảng lớn", "item_type": "Food", "price": 295000, "category_id": "CAT01", "availability": True, "preparation_time": 24},
    {"item_id": "MC13", "item_name": "Cá tuyết nướng sốt miso trắng", "item_type": "Food", "price": 360000, "category_id": "CAT01", "availability": False, "preparation_time": 20},
    {"item_id": "MC14", "item_name": "Tôm sú nướng bơ tỏi phô mai", "item_type": "Food", "price": 255000, "category_id": "CAT01", "availability": True, "preparation_time": 16},
    {"item_id": "MC15", "item_name": "Pizza hải sản phô mai Mozzarella", "item_type": "Food", "price": 195000, "category_id": "CAT01", "availability": True, "preparation_time": 16},
    {"item_id": "MC16", "item_name": "Pizza bò nướng BBQ hành tây", "item_type": "Food", "price": 185000, "category_id": "CAT01", "availability": True, "preparation_time": 16},
    {"item_id": "MC17", "item_name": "Pizza 4 loại phô mai nướng củi", "item_type": "Food", "price": 190000, "category_id": "CAT01", "availability": True, "preparation_time": 15},
    {"item_id": "MC18", "item_name": "Burger bò Wagyu phô mai Cheddar", "item_type": "Food", "price": 180000, "category_id": "CAT01", "availability": True, "preparation_time": 15},
    {"item_id": "MC19", "item_name": "Cơm chiên hải sản trứng muối", "item_type": "Food", "price": 140000, "category_id": "CAT01", "availability": True, "preparation_time": 12},
    {"item_id": "MC20", "item_name": "Thăn ngoại bò Úc nướng đá nóng", "item_type": "Food", "price": 320000, "category_id": "CAT01", "availability": True, "preparation_time": 20},

    # === CAT02: Khai vị & Ăn kèm (20 món) ===
    {"item_id": "FD04", "item_name": "Salad Caesar ức gà nướng", "item_type": "Food", "price": 115000, "category_id": "CAT02", "availability": True, "preparation_time": 10},
    {"item_id": "FD05", "item_name": "Súp bí đỏ kem tươi bánh mì bơ tỏi", "item_type": "Food", "price": 75000, "category_id": "CAT02", "availability": False, "preparation_time": 12},
    {"item_id": "KV03", "item_name": "Súp kem nấm rừng Truffle", "item_type": "Food", "price": 85000, "category_id": "CAT02", "availability": True, "preparation_time": 12},
    {"item_id": "KV04", "item_name": "Súp hành tây kiểu Pháp đút lò", "item_type": "Food", "price": 90000, "category_id": "CAT02", "availability": True, "preparation_time": 14},
    {"item_id": "KV05", "item_name": "Salad cá hồi xông khói bơ sáp", "item_type": "Food", "price": 145000, "category_id": "CAT02", "availability": True, "preparation_time": 10},
    {"item_id": "KV06", "item_name": "Salad rau mầm sốt dầu giấm Ý", "item_type": "Food", "price": 80000, "category_id": "CAT02", "availability": True, "preparation_time": 8},
    {"item_id": "KV07", "item_name": "Salad Burrata cà chua bi húng quế", "item_type": "Food", "price": 155000, "category_id": "CAT02", "availability": True, "preparation_time": 8},
    {"item_id": "KV08", "item_name": "Bánh mì bơ tỏi nướng giòn", "item_type": "Food", "price": 45000, "category_id": "CAT02", "availability": True, "preparation_time": 6},
    {"item_id": "KV09", "item_name": "Bruschetta cà chua phô mai dê", "item_type": "Food", "price": 85000, "category_id": "CAT02", "availability": True, "preparation_time": 8},
    {"item_id": "KV10", "item_name": "Khoai tây chiên sốt phô mai Truffle", "item_type": "Food", "price": 75000, "category_id": "CAT02", "availability": True, "preparation_time": 9},
    {"item_id": "KV11", "item_name": "Khoai tây nghiền bơ Pháp", "item_type": "Food", "price": 60000, "category_id": "CAT02", "availability": True, "preparation_time": 8},
    {"item_id": "KV12", "item_name": "Măng tây xanh xào tỏi bơ", "item_type": "Food", "price": 95000, "category_id": "CAT02", "availability": True, "preparation_time": 8},
    {"item_id": "KV13", "item_name": "Mực vòng chiên giòn sốt Tartar", "item_type": "Food", "price": 110000, "category_id": "CAT02", "availability": True, "preparation_time": 10},
    {"item_id": "KV14", "item_name": "Cánh gà chiên sốt cay Buffalo", "item_type": "Food", "price": 105000, "category_id": "CAT02", "availability": True, "preparation_time": 12},
    {"item_id": "KV15", "item_name": "Pate gan ngỗng kèm bánh mì Brioche", "item_type": "Food", "price": 185000, "category_id": "CAT02", "availability": True, "preparation_time": 10},
    {"item_id": "KV16", "item_name": "Thịt nguội & phô mai tổng hợp (Cold Cut)", "item_type": "Food", "price": 240000, "category_id": "CAT02", "availability": True, "preparation_time": 10},
    {"item_id": "KV17", "item_name": "Vẹm xanh hấp rượu vang trắng", "item_type": "Food", "price": 160000, "category_id": "CAT02", "availability": True, "preparation_time": 12},
    {"item_id": "KV18", "item_name": "Tôm cuộn khoai tây chiên giòn", "item_type": "Food", "price": 125000, "category_id": "CAT02", "availability": True, "preparation_time": 11},
    {"item_id": "KV19", "item_name": "Hành tây chiên giòn vòng lớn", "item_type": "Food", "price": 65000, "category_id": "CAT02", "availability": True, "preparation_time": 8},
    {"item_id": "KV20", "item_name": "Rau củ nướng dầu ô liu thảo mộc", "item_type": "Food", "price": 85000, "category_id": "CAT02", "availability": True, "preparation_time": 10},

    # === CAT03: Đồ uống pha chế (20 đồ uống) ===
    {"item_id": "DR01", "item_name": "Trà đào cam sả", "item_type": "Drink", "price": 55000, "category_id": "CAT03", "availability": True, "size": "L"},
    {"item_id": "DR02", "item_name": "Espresso đá", "item_type": "Drink", "price": 45000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR03", "item_name": "Nước ép cam tươi mật ong", "item_type": "Drink", "price": 60000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR04", "item_name": "Cold Brew cam quế", "item_type": "Drink", "price": 65000, "category_id": "CAT03", "availability": False, "size": "S"},
    {"item_id": "DR05", "item_name": "Cappuccino nóng Ý", "item_type": "Drink", "price": 55000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR06", "item_name": "Latte hạnh nhân ít đường", "item_type": "Drink", "price": 60000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR07", "item_name": "Americano đá", "item_type": "Drink", "price": 45000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR08", "item_name": "Caramel Macchiato đá", "item_type": "Drink", "price": 65000, "category_id": "CAT03", "availability": True, "size": "L"},
    {"item_id": "DR09", "item_name": "Matcha Latte Uji Nhật Bản", "item_type": "Drink", "price": 65000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR10", "item_name": "Trà vải hoa hồng", "item_type": "Drink", "price": 55000, "category_id": "CAT03", "availability": True, "size": "L"},
    {"item_id": "DR11", "item_name": "Trà sen vàng kem phô mai", "item_type": "Drink", "price": 60000, "category_id": "CAT03", "availability": True, "size": "L"},
    {"item_id": "DR12", "item_name": "Trà ô long bưởi hồng mật ong", "item_type": "Drink", "price": 58000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR13", "item_name": "Soda chanh dây bạc hà", "item_type": "Drink", "price": 50000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR14", "item_name": "Soda việt quất tươi", "item_type": "Drink", "price": 55000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR15", "item_name": "Mojito chanh tươi không cồn", "item_type": "Drink", "price": 65000, "category_id": "CAT03", "availability": True, "size": "L"},
    {"item_id": "DR16", "item_name": "Nước ép dứa táo gừng tươi", "item_type": "Drink", "price": 58000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR17", "item_name": "Nước ép dưa hấu bạc hà", "item_type": "Drink", "price": 50000, "category_id": "CAT03", "availability": True, "size": "M"},
    {"item_id": "DR18", "item_name": "Sinh tố xoài dừa nhiệt đới", "item_type": "Drink", "price": 65000, "category_id": "CAT03", "availability": True, "size": "L"},
    {"item_id": "DR19", "item_name": "Sô-cô-la Bỉ nóng Marshmallow", "item_type": "Drink", "price": 62000, "category_id": "CAT03", "availability": True, "size": "S"},
    {"item_id": "DR20", "item_name": "Cà phê muối kem béo Huế", "item_type": "Drink", "price": 52000, "category_id": "CAT03", "availability": True, "size": "M"},

    # === CAT04: Tráng miệng (20 món) ===
    {"item_id": "FD06", "item_name": "Tiramisu cổ điển vị Espresso", "item_type": "Food", "price": 85000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM02", "item_name": "Panna Cotta dâu tây tươi", "item_type": "Food", "price": 70000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM03", "item_name": "Crème Brûlée vani Madagascar", "item_type": "Food", "price": 80000, "category_id": "CAT04", "availability": True, "preparation_time": 6},
    {"item_id": "TM04", "item_name": "Bánh Lava Sô-cô-la chảy kem vani", "item_type": "Food", "price": 95000, "category_id": "CAT04", "availability": True, "preparation_time": 12},
    {"item_id": "TM05", "item_name": "Cheesecake chanh dây nướng", "item_type": "Food", "price": 85000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM06", "item_name": "Basque Burnt Cheesecake cháy cạnh", "item_type": "Food", "price": 90000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM07", "item_name": "Mousse sô-cô-la đen 70%", "item_type": "Food", "price": 82000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM08", "item_name": "Mousse xoài dừa lạnh", "item_type": "Food", "price": 75000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM09", "item_name": "Bánh táo nướng quế kèm kem vani", "item_type": "Food", "price": 88000, "category_id": "CAT04", "availability": True, "preparation_time": 10},
    {"item_id": "TM10", "item_name": "Bánh su kem vỏ giòn Matcha", "item_type": "Food", "price": 65000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM11", "item_name": "Bánh ngàn lớp Mille-Feuille dâu", "item_type": "Food", "price": 95000, "category_id": "CAT04", "availability": True, "preparation_time": 7},
    {"item_id": "TM12", "item_name": "Bánh Opera cà phê Pháp", "item_type": "Food", "price": 88000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM13", "item_name": "Bánh Red Velvet kem phô mai", "item_type": "Food", "price": 80000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM14", "item_name": "Bánh tart chanh vàng Meringue", "item_type": "Food", "price": 78000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM15", "item_name": "Kem Gelato Ý 2 viên tự chọn", "item_type": "Food", "price": 75000, "category_id": "CAT04", "availability": True, "preparation_time": 4},
    {"item_id": "TM16", "item_name": "Affogato kem vani rót Espresso nóng", "item_type": "Food", "price": 85000, "category_id": "CAT04", "availability": True, "preparation_time": 5},
    {"item_id": "TM17", "item_name": "Waffle Bỉ mật ong trái cây tươi", "item_type": "Food", "price": 92000, "category_id": "CAT04", "availability": True, "preparation_time": 10},
    {"item_id": "TM18", "item_name": "Bánh crepe ngàn lớp trà xanh", "item_type": "Food", "price": 85000, "category_id": "CAT04", "availability": False, "preparation_time": 5},
    {"item_id": "TM19", "item_name": "Macaron Pháp hộp 4 vị", "item_type": "Food", "price": 110000, "category_id": "CAT04", "availability": True, "preparation_time": 4},
    {"item_id": "TM20", "item_name": "Đĩa trái cây tươi theo mùa", "item_type": "Food", "price": 95000, "category_id": "CAT04", "availability": True, "preparation_time": 6},
]

SEED_ORDERS = [
    {
        "order_id": "ORD01",
        "order_date": "2026-11-10T12:15:00",
        "items": [
            {"item_id": "FD01", "quantity": 2, "unit_price": 245000},
            {"item_id": "DR01", "quantity": 2, "size": "L", "unit_price": 66000},
        ],
    },
    {
        "order_id": "ORD02",
        "order_date": "2026-11-11T19:30:00",
        "items": [
            {"item_id": "FD02", "quantity": 1, "unit_price": 280000},
            {"item_id": "FD04", "quantity": 1, "unit_price": 115000},
            {"item_id": "DR03", "quantity": 1, "size": "M", "unit_price": 60000},
        ],
    },
    {
        "order_id": "ORD03",
        "order_date": "2026-11-12T18:45:00",
        "items": [
            {"item_id": "FD03", "quantity": 2, "unit_price": 165000},
            {"item_id": "FD06", "quantity": 2, "unit_price": 85000},
            {"item_id": "DR02", "quantity": 2, "size": "M", "unit_price": 45000},
        ],
    },
    {
        "order_id": "ORD04",
        "order_date": "2026-11-13T11:20:00",
        "items": [
            {"item_id": "FD01", "quantity": 1, "unit_price": 245000},
            {"item_id": "FD06", "quantity": 1, "unit_price": 85000},
            {"item_id": "DR01", "quantity": 1, "size": "L", "unit_price": 66000},
        ],
    },
    {
        "order_id": "ORD05",
        "order_date": "2026-11-13T20:10:00",
        "items": [
            {"item_id": "FD02", "quantity": 2, "unit_price": 280000},
            {"item_id": "FD04", "quantity": 2, "unit_price": 115000},
            {"item_id": "DR01", "quantity": 3, "size": "L", "unit_price": 66000},
        ],
    },
]


def ensure_indexes(db) -> None:
    db.categories.create_index("category_id", unique=True)
    db.menu_items.create_index("item_id", unique=True)
    db.orders.create_index("order_id", unique=True)


def seed_database(db, reset: bool = False) -> dict:
    ensure_indexes(db)
    if reset:
        db.categories.delete_many({})
        db.menu_items.delete_many({})
        db.orders.delete_many({})

    if db.categories.count_documents({}) == 0:
        db.categories.insert_many([dict(doc) for doc in SEED_CATEGORIES])
    if db.menu_items.count_documents({}) == 0:
        db.menu_items.insert_many([dict(doc) for doc in SEED_MENU_ITEMS])
    if db.orders.count_documents({}) == 0:
        db.orders.insert_many([dict(doc) for doc in SEED_ORDERS])

    return {
        "categories": db.categories.count_documents({}),
        "menu_items": db.menu_items.count_documents({}),
        "orders": db.orders.count_documents({}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed MongoDB for L'Atelier Bistro")
    parser.add_argument("--uri", default=DEFAULT_MONGO_URI)
    parser.add_argument("--db", default=DEFAULT_DB_NAME)
    parser.add_argument("--reset", action="store_true", help="Drop existing documents before seeding")
    args = parser.parse_args()

    client = MongoClient(args.uri, serverSelectionTimeoutMS=5000)
    try:
        counts = seed_database(client[args.db], reset=args.reset)
        print(
            f"Seeded MongoDB '{args.db}': "
            f"{counts['categories']} categories, {counts['menu_items']} menu_items, {counts['orders']} orders."
        )
    finally:
        client.close()


if __name__ == "__main__":
    main()
