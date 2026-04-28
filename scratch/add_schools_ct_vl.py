import os
import sys

# Add project root to sys.path so we can import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.firebase_client import fb_get_high_schools, fb_save_high_schools

def add_specific_schools():
    existing_schools = fb_get_high_schools()
    if not existing_schools:
        existing_schools = []
        
    existing_names = {s.get("name"): True for s in existing_schools}

    new_schools = [
        # Cần Thơ
        {"name": "THPT Châu Văn Liêm", "province": "Cần Thơ"},
        {"name": "THPT Thực hành Sư phạm (ĐH Cần Thơ)", "province": "Cần Thơ"},
        {"name": "THPT Nguyễn Việt Hồng", "province": "Cần Thơ"},
        {"name": "THPT Bùi Hữu Nghĩa", "province": "Cần Thơ"},
        {"name": "THPT Bình Thủy", "province": "Cần Thơ"},
        {"name": "THPT Nguyễn Bỉnh Khiêm", "province": "Cần Thơ"},
        {"name": "THPT Phan Ngọc Hiển", "province": "Cần Thơ"},
        {"name": "THPT Thốt Nốt", "province": "Cần Thơ"},
        {"name": "THPT Lưu Hữu Phước", "province": "Cần Thơ"},
        {"name": "THPT Trung An", "province": "Cần Thơ"},
        {"name": "THPT Hà Huy Giáp", "province": "Cần Thơ"},
        {"name": "THPT Thới Lai", "province": "Cần Thơ"},
        {"name": "THPT Cờ Đỏ", "province": "Cần Thơ"},
        {"name": "THPT Vĩnh Thạnh", "province": "Cần Thơ"},
        {"name": "THPT Tân Phú", "province": "Cần Thơ"},
        
        # Vĩnh Long
        {"name": "THPT Vĩnh Long", "province": "Vĩnh Long"},
        {"name": "THPT Lưu Văn Liệt", "province": "Vĩnh Long"},
        {"name": "THPT Nguyễn Thông", "province": "Vĩnh Long"},
        {"name": "THPT Trưng Vương", "province": "Vĩnh Long"},
        {"name": "THPT Phạm Hùng", "province": "Vĩnh Long"},
        {"name": "THPT Mang Thít", "province": "Vĩnh Long"},
        {"name": "THPT Trà Ôn", "province": "Vĩnh Long"},
        {"name": "THPT Hựu Thành", "province": "Vĩnh Long"},
        {"name": "THPT Bình Minh", "province": "Vĩnh Long"},
        {"name": "THPT Hoàng Thái Hiếu", "province": "Vĩnh Long"},
        {"name": "THPT Vũng Liêm", "province": "Vĩnh Long"},
        {"name": "THPT Hiếu Phụng", "province": "Vĩnh Long"},
        {"name": "THPT Tam Bình", "province": "Vĩnh Long"},
        {"name": "THPT Trần Đại Nghĩa", "province": "Vĩnh Long"},
        {"name": "THPT Tân Lược", "province": "Vĩnh Long"}
    ]
    
    # THPT Chuyên Lý Tự Trọng (Cần Thơ) and THPT Chuyên Nguyễn Bỉnh Khiêm (Vĩnh Long)
    # usually were seeded, but let's make sure.
    if "THPT Chuyên Lý Tự Trọng" not in existing_names:
        new_schools.append({"name": "THPT Chuyên Lý Tự Trọng", "province": "Cần Thơ"})
    if "THPT Chuyên Nguyễn Bỉnh Khiêm" not in existing_names:
        new_schools.append({"name": "THPT Chuyên Nguyễn Bỉnh Khiêm", "province": "Vĩnh Long"})

    added_count = 0
    for school in new_schools:
        if school["name"] not in existing_names:
            existing_schools.append(school)
            added_count += 1
            
    if added_count > 0:
        fb_save_high_schools(existing_schools)
        print(f"Đã thêm thành công {added_count} trường từ Cần Thơ và Vĩnh Long vào Firebase.")
    else:
        print("Tất cả các trường này đều đã có sẵn trên hệ thống.")

if __name__ == "__main__":
    add_specific_schools()
