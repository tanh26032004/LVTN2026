import os
import sys

# Add project root to sys.path so we can import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.firebase_client import fb_get_high_schools, fb_save_high_schools

def seed_high_schools():
    existing = fb_get_high_schools()
    if existing and len(existing) > 0:
        print(f"Danh sách trường THPT đã tồn tại ({len(existing)} trường). Bỏ qua seed.")
        return

    # Danh sách mẫu các trường THPT (Seed data)
    seed_data = [
        {"name": "THPT Chuyên Hà Nội - Amsterdam", "province": "Hà Nội"},
        {"name": "THPT Chuyên Khoa học Tự nhiên", "province": "Hà Nội"},
        {"name": "THPT Chuyên Ngoại ngữ", "province": "Hà Nội"},
        {"name": "THPT Chu Văn An", "province": "Hà Nội"},
        {"name": "THPT Kim Liên", "province": "Hà Nội"},
        {"name": "THPT Phan Đình Phùng", "province": "Hà Nội"},
        {"name": "THPT Chuyên Lê Hồng Phong", "province": "Hồ Chí Minh"},
        {"name": "THPT Chuyên Trần Đại Nghĩa", "province": "Hồ Chí Minh"},
        {"name": "THPT Năng khiếu ĐHQG TP.HCM", "province": "Hồ Chí Minh"},
        {"name": "THPT Nguyễn Thượng Hiền", "province": "Hồ Chí Minh"},
        {"name": "THPT Gia Định", "province": "Hồ Chí Minh"},
        {"name": "THPT Bùi Thị Xuân", "province": "Hồ Chí Minh"},
        {"name": "THPT Chuyên Lê Quý Đôn", "province": "Đà Nẵng"},
        {"name": "THPT Phan Châu Trinh", "province": "Đà Nẵng"},
        {"name": "THPT Hoàng Hoa Thám", "province": "Đà Nẵng"},
        {"name": "THPT Chuyên Quốc Học", "province": "Thừa Thiên Huế"},
        {"name": "THPT Hai Bà Trưng", "province": "Thừa Thiên Huế"},
        {"name": "THPT Chuyên Lam Sơn", "province": "Thanh Hóa"},
        {"name": "THPT Chuyên Phan Bội Châu", "province": "Nghệ An"},
        {"name": "THPT Chuyên Trần Phú", "province": "Hải Phòng"},
        {"name": "THPT Chuyên Lê Quý Đôn", "province": "Bà Rịa - Vũng Tàu"},
        {"name": "THPT Chuyên Nguyễn Bỉnh Khiêm", "province": "Quảng Nam"},
        {"name": "THPT Chuyên Lương Văn Chánh", "province": "Phú Yên"},
        {"name": "THPT Chuyên Lê Khiết", "province": "Quảng Ngãi"},
        {"name": "THPT Chuyên Hùng Vương", "province": "Phú Thọ"},
        {"name": "THPT Chuyên Vĩnh Phúc", "province": "Vĩnh Phúc"},
        {"name": "THPT Chuyên Bắc Ninh", "province": "Bắc Ninh"},
        {"name": "THPT Chuyên Bắc Giang", "province": "Bắc Giang"},
        {"name": "THPT Chuyên Thái Bình", "province": "Thái Bình"},
        {"name": "THPT Chuyên Lê Quý Đôn", "province": "Điện Biên"},
        {"name": "THPT Chuyên Thoại Ngọc Hầu", "province": "An Giang"},
        {"name": "THPT Chuyên Quang Trung", "province": "Bình Phước"},
        {"name": "THPT Chuyên Bến Tre", "province": "Bến Tre"},
        {"name": "THPT Chuyên Nguyễn Đình Chiểu", "province": "Đồng Tháp"},
        {"name": "THPT Chuyên Lý Tự Trọng", "province": "Cần Thơ"}
    ]
    
    fb_save_high_schools(seed_data)
    print(f"Đã seed thành công {len(seed_data)} trường THPT lên Firebase.")

if __name__ == "__main__":
    seed_high_schools()
