import re


class MenuItem:
    service_charge = 0.0

    def __init__(self, item_id, item_name, base_price):
        self.item_id = item_id
        self.item_name = item_name.title()
        self.__base_price = base_price
        self.__is_available = True

    @property
    def base_price(self):
        return self.__base_price

    @base_price.setter
    def base_price(self, new_price):
        if new_price <= 0:
            print("Giá đồ uống phải lớn hơn 0!")
            print("Giá cũ được giữ nguyên.")
            return
        self.__base_price = new_price

    @property
    def is_available(self):
        return self.__is_available

    def toggle_availability(self):
        self.__is_available = not self.__is_available

    def calculate_selling_price(self):
        return int(self.__base_price * (1 + MenuItem.service_charge))

    @classmethod
    def update_service_charge(cls, new_rate):
        if 0 <= new_rate <= 1:
            cls.service_charge = new_rate
            return True
        return False

    @staticmethod
    def is_valid_item_id(item_id):
        return bool(re.fullmatch(r"[A-Z]{2}\d{2}", item_id))


menu_db = [
    MenuItem("CF01", "Cà Phê Đen", 30000),
    MenuItem("CF02", "Bạc Xỉu", 45000),
    MenuItem("TE01", "Trà Đào Cam Sả", 50000)
]


def find_item(item_id):
    for item in menu_db:
        if item.item_id == item_id:
            return item
    return None


while True:
    print("\n===== HỆ THỐNG QUẢN LÝ THỰC ĐƠN RIKKEI COFFEE =====")
    print("1. Xem thực đơn & Giá niêm yết")
    print("2. Thêm món mới vào menu")
    print("3. Cập nhật trạng thái (Hết hàng/Còn hàng)")
    print("4. Điều chỉnh giá gốc của món")
    print("5. Cập nhật phụ phí dịch vụ toàn hệ thống")
    print("6. Thoát chương trình")
    print("==================================================")

    choice = input("Chọn chức năng (1-6): ")

    if choice == "1":
        print("\n--- THỰC ĐƠN RIKKEI COFFEE ---")

        if not menu_db:
            print("Chưa có món trong thực đơn.")
        else:
            for i, item in enumerate(menu_db, start=1):
                status = "Đang bán" if item.is_available else "Hết hàng"

                print(
                    f"{i}. Mã: {item.item_id} | "
                    f"Tên: {item.item_name:<20} | "
                    f"Trạng thái: {status:<9} | "
                    f"Giá niêm yết: {item.calculate_selling_price():,} VNĐ"
                )

    elif choice == "2":
        print("\n--- THÊM MÓN MỚI VÀO MENU ---")

        item_id = input("Nhập mã món: ").strip().upper()

        if not MenuItem.is_valid_item_id(item_id):
            print("\nMã món không hợp lệ!")
            print("Mã món phải gồm 2 chữ cái in hoa và 2 chữ số. Ví dụ: CF01.")
            continue

        if find_item(item_id):
            print("\nMã món đã tồn tại!")
            continue

        name = input("Nhập tên món: ")

        try:
            price = int(input("Nhập giá gốc: "))

            if price <= 0:
                print("Giá phải lớn hơn 0.")
                continue

            menu_db.append(MenuItem(item_id, name, price))

            print("\nThêm món mới thành công!")

        except ValueError:
            print("Giá không hợp lệ.")

    elif choice == "3":
            print("\n--- CẬP NHẬT TRẠNG THÁI MÓN ---")

            item_id = input("Nhập mã món cần cập nhật: ").strip().upper()

            item = find_item(item_id)

            if item is None:
                print("Không tìm thấy món.")
                continue

            item.toggle_availability()

            if item.is_available:
                print(f">> Đã cập nhật {item.item_name} thành ĐANG BÁN!")
            else:
                print(f">> Đã cập nhật {item.item_name} thành HẾT HÀNG!")

    elif choice == "4":
        print("\n--- ĐIỀU CHỈNH GIÁ GỐC CỦA MÓN ---")

        item_id = input("Nhập mã món cần đổi giá: ").strip().upper()

        item = find_item(item_id)

        if item is None:
            print("Không tìm thấy món.")
            continue

        try:
            new_price = int(input("Nhập giá tiền mới: "))

            old_price = item.base_price

            item.base_price = new_price

            if item.base_price != old_price:
                print("Cập nhật giá gốc thành công!")

        except ValueError:
            print("Giá tiền không hợp lệ.")

    elif choice == "5":
        print("\n--- CẬP NHẬT PHỤ PHÍ DỊCH VỤ TOÀN HỆ THỐNG ---")
        print(f"Phụ phí hiện tại: {MenuItem.service_charge * 100:.0f}%")

        try:
            new_rate = float(
                input("Nhập phụ phí mới. Ví dụ 0.1 tương ứng 10%: ")
            )

            if MenuItem.update_service_charge(new_rate):
                print("Cập nhật phụ phí dịch vụ thành công!")
            else:
                print("Phụ phí phải nằm trong khoảng từ 0 đến 1.")

        except ValueError:
            print("Dữ liệu không hợp lệ.")

    elif choice == "6":
        print("\nCảm ơn bạn đã sử dụng hệ thống Rikkei Coffee!")
        break

    else:
        print("Lựa chọn không hợp lệ.")