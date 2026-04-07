from langchain_core.tools import tool


FLIGHTS_DB = {

    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTEL_DB ={
    "Đà Nẵng": [

    {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}
@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'hà nội', 'HÀ NỘI')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'đà nẵng')
    Không phân biệt chữ hoa/thường. Trả về danh sách chuyến bay hoặc các tuyến có sẵn.
    """
    
    # Helper function: format giá tiền kiểu Việt Nam (1.450.000đ)
    def format_price(price: int) -> str:
        return f"{price:,}đ".replace(",", ".")
    
    # Helper function: tìm tuple key từ FLIGHTS_DB (xử lý case-insensitive)
    def find_tuple_key(db: dict, o: str, d: str):
        """Tìm tuple key (origin, destination) từ db, xử lý không phân biệt hoa/thường"""
        o = o.strip().lower()
        d = d.strip().lower()
        
        for (key_o, key_d) in db.keys():
            if key_o.strip().lower() == o and key_d.strip().lower() == d:
                return (key_o, key_d)
        return None
    
    # Chuẩn hóa input - remove whitespace và case-insensitive
    origin = origin.strip()
    destination = destination.strip()
    
    # Bước 1: Tra cứu thuận chiều (origin -> destination)
    key = find_tuple_key(FLIGHTS_DB, origin, destination)
    flights = None
    is_reverse = False
    actual_origin = origin
    actual_destination = destination
    
    if key:
        flights = FLIGHTS_DB[key]
        actual_origin, actual_destination = key
    else:
        # Bước 2: Tra ngược chiều (destination -> origin) nếu không tìm thấy
        reverse_key = find_tuple_key(FLIGHTS_DB, destination, origin)
        if reverse_key:
            flights = FLIGHTS_DB[reverse_key]
            is_reverse = True
            actual_origin, actual_destination = reverse_key
    
    # Nếu vẫn không tìm thấy -> trả về lỗi
    if flights is None:
        available_routes = "\n".join([f"  • {o} → {d}" for (o, d) in FLIGHTS_DB.keys()])
        return (
            f"❌ Không tìm thấy chuyến bay từ {origin} đến {destination}.\n\n"
            f"Các tuyến bay có sẵn:\n{available_routes}"
        )
    
    # Format output
    direction_note = " (ngược chiều)" if is_reverse else ""
    output = f"✈️ Chuyến bay {actual_origin} → {actual_destination}{direction_note}:\n\n"
    
    for i, flight in enumerate(flights, 1):
        output += f"{i}. {flight['airline']}\n"
        output += f"   🕐 Khởi hành: {flight['departure']} | Hạ cánh: {flight['arrival']}\n"
        output += f"   💰 Giá: {format_price(flight['price'])} | Hạng: {flight['class']}\n\n"
    
    return output


pass

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999, min_stars: int = 1) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, lọc theo giá và số sao, sắp xếp theo rating.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'đà nẵng', 'ĐÀ NẴNG')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    - min_stars: số sao tối thiểu (1-5), mặc định không giới hạn
    Không phân biệt chữ hoa/thường. Trả về danh sách khách sạn đã lọc, sắp xếp theo rating.
    """
    
    # Helper function: format giá tiền kiểu Việt Nam (1.450.000đ)
    def format_price(price: int) -> str:
        return f"{price:,}đ".replace(",", ".")
    
    # Chuẩn hóa tên thành phố - remove whitespace, case-insensitive
    city = city.strip()
    
    # Tra cứu thành phố trong HOTEL_DB (không phân biệt hoa/thường)
    hotels = None
    actual_city_name = None
    for city_key in HOTEL_DB.keys():
        if city_key.strip().lower() == city.lower():
            hotels = HOTEL_DB[city_key]
            actual_city_name = city_key  # Lưu tên gốc để display
            break
    
    if hotels is None:
        available_cities = ", ".join(HOTEL_DB.keys())
        return f"❌ Không tìm thấy khách sạn tại '{city}'.\n📍 Các thành phố có sẵn: {available_cities}"
    
    # Lọc theo giá tối đa VÀ số sao tối thiểu
    filtered = [
        h for h in hotels
        if h["price_per_night"] <= max_price_per_night and h["stars"] >= min_stars
    ]
    
    # Nếu không có kết quả sau lọc
    if not filtered:
        total = len(hotels)
        return (
            f"❌ Không tìm thấy khách sạn tại {city} "
            f"với giá dưới {format_price(max_price_per_night)}/đêm"
            f"{f' và từ {min_stars}⭐ trở lên' if min_stars > 1 else ''}.\n"
            f"Có {total} khách sạn tại đây, hãy thử tăng ngân sách hoặc giảm số sao tối thiểu."
        )
    
    # Sắp xếp: rating giảm dần (ưu tiên), giá tăng dần (phụ)
    filtered.sort(key=lambda h: (-h["rating"], h["price_per_night"]))
    
    # Format output
    price_filter_note = f" (giá dưới {format_price(max_price_per_night)}/đêm)" if max_price_per_night < 99999999 else ""
    stars_filter_note = f", từ {min_stars}⭐ trở lên" if min_stars > 1 else ""
    output = f"🏨 Khách sạn tại {actual_city_name}{price_filter_note}{stars_filter_note}:\n"
    output += f"📊 Tìm thấy {len(filtered)}/{len(hotels)} khách sạn (sắp xếp theo rating)\n\n"
    
    for i, hotel in enumerate(filtered, 1):
        stars = "⭐" * hotel["stars"]
        output += f"{i}. {hotel['name']} {stars}\n"
        output += f"   📍 Khu vực: {hotel['area']} | ⭐ Đánh giá: {hotel['rating']}/5\n"
        output += f"   💰 Giá: {format_price(hotel['price_per_night'])}/đêm\n\n"
    
    return output

    
    return output
@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ, phải > 0)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy
      Định dạng: 'tên_khoản:số_tiền,tên_khác:số_tiền'
      VD: 'vé_máy_bay:890000,khách_sạn:650000,ăn_uống:500000'
    Trả về bảng chi tiết các khoản chi, trạng thái ngân sách, % đã dùng.
    """
    
    def format_price(amount: int) -> str:
        """Format số tiền kiểu Việt Nam với dấu chấm phân cách"""
        return f"{amount:,}đ".replace(",", ".")
    
    # Validate total_budget
    if total_budget <= 0:
        return "❌ Ngân sách phải là số dương!"
    
    # Parse chuỗi expenses - Case insensitive friendly
    parsed_expenses = []  # list of (name, amount) để giữ thứ tự
    parse_errors = []

    if expenses.strip():
        items = expenses.split(",")
        for idx, item in enumerate(items, 1):
            item = item.strip()
            if not item:
                continue
            
            # Kiểm tra định dạng 'tên:số_tiền'
            if ":" not in item:
                parse_errors.append(f"  [{idx}] '{item}' → Thiếu ':' (Định dạng: tên:số_tiền)")
                continue
            
            name, amount_str = item.split(":", 1)
            name = name.strip()  # Không phân biệt hoa/thường ở tên
            amount_str = amount_str.strip()
            
            if not name:
                parse_errors.append(f"  [{idx}] '{item}' → Tên khoản chi không được để trống")
                continue
            
            # Parse số tiền: hỗ trợ 890000, 890.000, 890,000, 0.89M
            try:
                # Remove dấu phân cách và convert
                clean_amount = amount_str.replace(".", "").replace(",", "")
                amount = float(clean_amount)
                if amount < 0:
                    parse_errors.append(f"  [{idx}] '{name}' → Số tiền không âm ({amount_str})")
                    continue
                parsed_expenses.append((name, int(amount)))
            except ValueError:
                parse_errors.append(f"  [{idx}] '{name}' → Số tiền không hợp lệ: '{amount_str}'")
                continue
    
    # Nếu có lỗi parse → báo lỗi ngay với gợi ý rõ
    if parse_errors:
        error_msg = "❌ Lỗi định dạng expenses:\n" + "\n".join(parse_errors)
        error_msg += "\n\n✅ Ví dụ đúng: vé:890000,khách:650000,ăn:500000"
        return error_msg
    
    # Tính toán
    total_expenses = sum(amount for _, amount in parsed_expenses)
    remaining = total_budget - total_expenses
    
    # Format output
    output = "💰 BÁO CÁO NGÂN SÁCH\n"
    output += "═" * 45 + "\n\n"
    
    if parsed_expenses:
        output += "📋 Chi tiết các khoản chi:\n"
        for name, amount in parsed_expenses:
            pct = (amount / total_budget * 100) if total_budget > 0 else 0
            output += f"   • {name:<20} {format_price(amount):>15}  ({pct:.1f}%)\n"
        output += "\n"
    
    output += "─" * 45 + "\n"
    output += f"   {'Tổng chi phí:':<22} {format_price(total_expenses):>15}\n"
    output += f"   {'Ngân sách ban đầu:':<22} {format_price(total_budget):>15}\n"
    output += "─" * 45 + "\n"
    
    if remaining >= 0:
        pct_used = (total_expenses / total_budget * 100) if total_budget > 0 else 0
        output += f"   {'Còn lại:':<22} {format_price(remaining):>15}\n"
        output += f"\n✅ Đã dùng {pct_used:.1f}% ngân sách, còn dư {format_price(remaining)}."
    else:
        output += f"   {'Thiếu:':<22} {format_price(abs(remaining)):>15}\n"
        output += f"\n❌ Vượt ngân sách {format_price(abs(remaining))}! Cần điều chỉnh chi tiêu."
    
    return output




