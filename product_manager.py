import json
import os

# Tên file lưu trữ dữ liệu
DATA_FILE = "products.json"

def load_data():
    """
    Đọc dữ liệu từ file products.json.
    Nếu file không tồn tại, trả về danh sách rỗng.
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        # Lần đầu chạy chưa có file thì trả về list rỗng
        return []
    except json.JSONDecodeError:
        # Nếu file lỗi định dạng, cũng trả về rỗng để tránh crash
        return []

def save_data(products):
    """
    Ghi danh sách sản phẩm vào file products.json.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            # ensure_ascii=False để lưu tiếng Việt không bị lỗi font
            json.dump(products, f, indent=4, ensure_ascii=False)
        print(">> Đã lưu dữ liệu thành công!")
    except Exception as e:
        print(f"Lỗi khi lưu file: {e}")

def add_product(products):
    """
    Thêm sản phẩm mới vào danh sách.
    Tự động sinh mã ID (Ví dụ: LT01, LT02...).
    """
    print("\n--- THÊM SẢN PHẨM MỚI ---")
    name = input("Nhập tên sản phẩm: ")
    brand = input("Nhập thương hiệu: ")
    
    # Xử lý nhập giá và số lượng (bắt lỗi nếu nhập sai định dạng)
    while True:
        try:
            price = int(input("Nhập giá sản phẩm (số nguyên): "))
            quantity = int(input("Nhập số lượng tồn kho (số nguyên): "))
            if price < 0 or quantity < 0:
                print("Giá và số lượng phải lớn hơn hoặc bằng 0.")
                continue
            break
        except ValueError:
            print("Vui lòng nhập con số hợp lệ!")

    # Tự động tạo ID: LT + số thứ tự (đơn giản hóa)
    # Để tránh trùng lặp khi xóa, cách tốt nhất là tìm ID lớn nhất hiện có hoặc dùng uuid.
    # Nhưng ở mức độ cơ bản, ta dùng độ dài danh sách + 1 (hoặc random).
    # Ở đây mình dùng logic đếm số lượng hiện tại + 1 cho đơn giản theo yêu cầu.
    new_id = f"LT{len(products) + 1:02d}" 
    
    # Kiểm tra xem ID này đã tồn tại chưa (trường hợp xóa rồi thêm mới có thể trùng)
    # Logic nâng cao hơn: Tìm số lớn nhất trong các ID hiện có để tăng lên.
    existing_ids = [p['id'] for p in products]
    count = len(products) + 1
    while new_id in existing_ids:
        count += 1
        new_id = f"LT{count:02d}"

    new_product = {
        "id": new_id,
        "name": name,
        "brand": brand,
        "price": price,
        "quantity": quantity
    }
    
    products.append(new_product)
    print(f"Đã thêm sản phẩm thành công! Mã sản phẩm: {new_id}")
    return products

def update_product(products):
    """
    Cập nhật thông tin sản phẩm dựa trên ID.
    """
    print("\n--- CẬP NHẬT SẢN PHẨM ---")
    product_id = input("Nhập mã sản phẩm cần sửa (VD: LT01): ").strip()
    
    found = False
    for product in products:
        if product['id'] == product_id:
            found = True
            print(f"Tìm thấy: {product['name']}")
            print("Nhập thông tin mới (nếu không đổi, hãy nhập lại giá trị cũ):")
            
            product['name'] = input(f"Tên mới ({product['name']}): ") or product['name']
            product['brand'] = input(f"Thương hiệu mới ({product['brand']}): ") or product['brand']
            
            # Cập nhật giá và số lượng
            try:
                p_input = input(f"Giá mới ({product['price']}): ")
                if p_input:
                    product['price'] = int(p_input)
                
                q_input = input(f"Số lượng mới ({product['quantity']}): ")
                if q_input:
                    product['quantity'] = int(q_input)
            except ValueError:
                print("Lỗi nhập liệu số! Giữ nguyên giá trị cũ.")

            print("Cập nhật thành công!")
            break
    
    if not found:
        print(f"Không tìm thấy sản phẩm có mã {product_id}")
    
    return products

def delete_product(products):
    """
    Xóa sản phẩm khỏi danh sách theo ID (Cải tiến: Không phân biệt hoa thường).
    """
    print("\n--- XÓA SẢN PHẨM ---")
    
    # Bước 1: Yêu cầu nhập và tự động chuyển sang chữ IN HOA
    # .strip() để loại bỏ khoảng trắng thừa nếu lỡ tay ấn dấu cách
    input_id = input("Nhập mã sản phẩm cần xóa (VD: LT01): ").strip().upper()
    
    found_product = None
    
    # Bước 2: Tìm kiếm sản phẩm
    for p in products:
        # So sánh mã trong kho (chuyển về in hoa) với mã vừa nhập
        if p['id'].upper() == input_id:
            found_product = p
            break
    
    # Bước 3: Xử lý xóa
    if found_product:
        print(f"Đã tìm thấy sản phẩm: {found_product['name']} (Giá: {found_product['price']})")
        confirm = input(f"Bạn chắc chắn muốn xóa không? (y/n): ")
        
        if confirm.lower() == 'y':
            products.remove(found_product)
            print(">> Đã xóa thành công!")
        else:
            print(">> Đã hủy thao tác xóa.")
    else:
        print(f">> KHÔNG TÌM THẤY mã sản phẩm '{input_id}'.")
        
        # Gợi ý cho người dùng biết hiện tại có những mã nào
        print("Các mã sản phẩm hiện có trong kho:", end=" ")
        ids = [p['id'] for p in products]
        print(", ".join(ids))

    return products
def search_product_by_name(products):
    """
    Tìm kiếm sản phẩm theo từ khóa (gần đúng, không phân biệt hoa thường).
    """
    print("\n--- TÌM KIẾM SẢN PHẨM ---")
    keyword = input("Nhập tên sản phẩm cần tìm: ").lower()
    
    results = [p for p in products if keyword in p['name'].lower()]
    
    if results:
        print(f"\nTìm thấy {len(results)} kết quả:")
        display_all_products(results) # Tái sử dụng hàm hiển thị
    else:
        print(f"Không tìm thấy sản phẩm nào chứa từ khóa '{keyword}'")

def display_all_products(products):
    """
    Hiển thị danh sách sản phẩm dạng bảng.
    """
    if not products:
        print("\n>> Kho hàng trống.")
        return

    print("\n" + "="*85)
    print(f"{'MÃ':<10} | {'TÊN SẢN PHẨM':<30} | {'THƯƠNG HIỆU':<15} | {'GIÁ':<12} | {'SL':<5}")
    print("-" * 85)
    
    for p in products:
        # Định dạng giá có dấu phẩy ngăn cách hàng nghìn (VD: 15,000,000)
        formatted_price = "{:,}".format(p['price'])
        print(f"{p['id']:<10} | {p['name']:<30} | {p['brand']:<15} | {formatted_price:<12} | {p['quantity']:<5}")
    
    print("="*85 + "\n")