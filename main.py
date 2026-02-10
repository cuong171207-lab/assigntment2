import sys
import product_manager as pm

def main():
    print("CHÀO MỪNG ĐẾN VỚI HỆ THỐNG QUẢN LÝ POLYLAP")
    
    # 1. Tải dữ liệu khi khởi động
    products = pm.load_data()
    print(f"Đã tải {len(products)} sản phẩm từ hệ thống.")

    while True:
        print("\n=========== MENU ===========")
        print("1. Hiển thị danh sách sản phẩm")
        print("2. Thêm sản phẩm mới")
        print("3. Cập nhật thông tin sản phẩm")
        print("4. Xóa sản phẩm")
        print("5. Tìm kiếm sản phẩm")
        print("6. Lưu dữ liệu")
        print("0. Thoát chương trình")
        print("============================")
        
        choice = input("Nhập lựa chọn của bạn: ")

        if choice == '1':
            pm.display_all_products(products)
        
        elif choice == '2':
            # Hàm add_product trả về list đã cập nhật (theo yêu cầu)
            products = pm.add_product(products)
        
        elif choice == '3':
            products = pm.update_product(products)
            
        elif choice == '4':
            products = pm.delete_product(products)
            
        elif choice == '5':
            pm.search_product_by_name(products)
            
        elif choice == '6':
            pm.save_data(products)
            
        elif choice == '0':
            print("Đang lưu dữ liệu trước khi thoát...")
            pm.save_data(products)
            print("Cảm ơn bạn đã sử dụng phần mềm POLYLAP. Tạm biệt!")
            break
            
        else:
            print("Lựa chọn không hợp lệ, vui lòng thử lại!")

if __name__ == "__main__":
    main()