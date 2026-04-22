# Nghiên cứu và Xây dựng hệ thống hỗ trợ tư vấn chọn ngành đại học dựa trên kỹ thuật Phân lớp dữ liệu đa yếu tố: Tính cách và Năng lực học tập
**Dự án Khóa luận Tốt nghiệp (LVTN 2026)**

> **Tên đề tài tiếng Anh**: "Development of a University Major Recommendation System using Multi-factor Classification: Personality Traits (MBTI) and Academic Performance"

Đây là một dự án ứng dụng trí tuệ nhân tạo (Học máy lai - Hybrid Machine Learning) nhằm mục đích giải quyết bài toán định hướng nghề nghiệp cho học sinh Trung học Phổ thông. Ứng dụng kết hợp hiệu quả Giới tuyến Sinh trắc học (Trắc nghiệm tính cách MBTI) và Năng lực cốt lõi (Điểm thi THPT) để tạo ra các đề xuất phân ngành phù hợp nhất cho người học.

---

## 🌟 Các Tính Năng Cốt Lõi (Core Features)

1. **Giao diện Hiện đại (Web Application)**
   - Phát triển hoàn toàn trên nền tảng **Streamlit** với kiến trúc phân rã UI (Modular Architecture).
   - Thiết kế chuẩn Glassmorphism, hỗ trợ tương tác trên cả điện thoại (Mobile) và Máy tính (Desktop). Tự động tương thích độ sáng (Adaptive Dark/Light Mode).

2. **Cấu trúc Cloud-Native (Firebase Integration)**
   - **Firestore DB**: Lưu trữ và quản lý toàn bộ cấu hình câu hỏi, mô tả MBTI và lượt nhật ký truy vấn theo thời gian thực.
   - **Auto-Sync**: Dữ liệu từ Admin Dashboard được đồng bộ ngay lập tức tới người dùng thông qua cơ chế Cache.
   - **Real-time Logging**: Ghi nhận thống kê sử dụng và kết quả dự đoán trực tiếp lên Cloud để phục vụ phân tích.

3. **Quản Trị Hệ Thống Chuyên Nghiệp (Admin Dashboard)**
   - **Xác thực Firebase Auth**: Đăng nhập Admin bảo mật bằng Email/Password qua hệ thống Firebase chính thức.
   - **Quản lý nội dung động**: Chỉnh sửa câu hỏi trắc nghiệm, hình ảnh mapping và nội dung chi tiết MBTI trực tiếp trên Dashboard mà không cần can thiệp mã nguồn.

4. **Trí tuệ nhân tạo có thể giải thích (Explainable AI - XAI)**
   - Tích hợp biểu đồ tương tác **Plotly** giải thích và minh bạch hóa lý do AI đưa ra gợi ý, trích xuất Feature Importances từ thuật toán Cây quyết định diện rộng (Random Forest).

---

## 📂 Kiến Trúc Mã Nguồn (Directory Structure)

```text
LVTN2026/
├── app.py                         # File chạy chính của Web App Streamlit
├── README.md                      # Tài liệu dự án
├── requirements.txt               # Danh sách thư viện Python (Firebase-admin, Requests...)
├── utils/                         # Các module tiện ích hệ thống
│   └── firebase_client.py         # Kết nối Firestore và Firebase Auth
├── data/                          # Chứa dữ liệu huấn luyện và script khai báo
│   ├── major_db.py                # Khai báo dữ liệu đặc tả mã nhóm ngành
│   └── student_data.csv           # Dữ liệu chuẩn đã Augment (8.000 hồ sơ)
├── assets/                        # Các tài nguyên tĩnh
│   ├── images/                    # Thư mục chứa hình họa MBTI và banner ngành
│   └── mbti_assets.py             # Xử lý dữ liệu MBTI đồng bộ Cloud
├── model/                         # Nơi lưu trữ Pipeline AI (.joblib)
├── scripts/                       # Mã nguồn huấn luyện độc lập
│   ├── data_augmentation.py       # Script tăng cường dữ liệu
│   └── train_model.py             # Script huấn luyện mô hình
├── views/                         # Kiến trúc Frontend Modules
│   ├── admin_dashboard.py         # Trang quản trị (Cập nhật Firebase Auth)
│   ├── components.py              # Xử lý CSS và HTML UI chung
│   ├── sidebar.py                 # Sidebar cài đặt hệ thống
│   ├── tab1_survey.py             # View phân tích và gợi ý chuyên ngành
│   ├── tab2_mbti.py               # View trắc nghiệm MBTI tương tác
│   └── tab3_xai.py                # View Trí tuệ Giải Thích AI
└── .streamlit/                    # Cấu hình Streamlit
    ├── config.toml                # Quy định theme và giao diện
    └── secrets.toml               # Lưu trữ Firebase Api Key & Service Account (Git Ignored)
```

---

## ⚙️ Cài Đặt Và Khởi Chạy

### 1. Chuẩn bị Môi trường
Dự án yêu cầu Python 3.9+ và các thư viện trong `requirements.txt`.
```bash
python -m venv venv
source venv/bin/activate  # Trên Mac/Linux
pip install -r requirements.txt
```

### 2. Cấu hình Firebase (Bắt buộc)
Dự án được Cloud hóa hoàn toàn, bạn cần cấu hình tệp `.streamlit/secrets.toml` để kết nối:
```toml
[firebase]
api_key = "WEB_API_KEY_CỦA_DỰ_ÁN"

[firebase_service_account]
type = "service_account"
project_id = "..."
private_key = """-----BEGIN PRIVATE KEY-----
Mã khóa bí mật của bạn ở đây
-----END PRIVATE KEY-----"""
client_email = "..."
# ... (copy toàn bộ từ file Service Account JSON)
```

### 3. Huấn luyện Mô hình
Thực thi các lệnh sau để chuẩn bị bộ não cho AI:
```bash
python scripts/merge_raw_data.py
python scripts/data_augmentation.py
python scripts/train_model.py
```

### 4. Khởi Động Website
```bash
streamlit run app.py
```

---

## 🔬 Thông Số Đo Lường Mô Hình (Metrics)

Kết quả đo lường thông qua **GridSearchCV** (với tập Test):

| Thuật Toán (Algorithm)            | Vai trò           | Accuracy | Nhận Xét Mục Đích Sử Dụng |
| ---------------------------------- | ----------------- | -------- | ---------------- |
| **Random Forest Classifier**       | **Mô Hình Chính** | `~87.99%` | Tư vấn chính và tính Feature Importances đa chiều. |
| **SVM (Support Vector Machine)**   | Đối trọng         | `~86.99%` | Thiết lập C chặn nhiễu cực tốt, bám sát Random Forest. |
| **Decision Tree**                  | Đối trọng / XAI   | `~82.36%` | Diễn giải logic rẽ nhánh If-Else tường minh. |

---
*(Bản quyền mã nguồn mở LVTN2026. Mọi thay đổi về cấu hình hiện được quản lý tập trung trên Firebase Firestore).*
