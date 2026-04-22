# Nghiên cứu và Xây dựng hệ thống hỗ trợ tư vấn chọn ngành đại học dựa trên kỹ thuật Phân lớp dữ liệu đa yếu tố: Tính cách và Năng lực học tập
**Dự án Khóa luận Tốt nghiệp (LVTN 2026)**



> **Tên đề tài tiếng Anh**: "Development of a University Major Recommendation System using Multi-factor Classification: Personality Traits (MBTI) and Academic Performance"

Đây là một dự án ứng dụng trí tuệ nhân tạo (Học máy lai - Hybrid Machine Learning) nhằm mục đích giải quyết bài toán định hướng nghề nghiệp cho học sinh Trung học Phổ thông. Thay vì chỉ dựa trên điểm số tĩnh hoặc một bài trắc nghiệm đơn điệu, ứng dụng này kết hợp hiệu quả Giới tuyến Sinh trắc học (Trắc nghiệm tính cách MBTI) và Năng lực cốt lõi (Điểm thi THPT 7 môn học) để tạo ra các đề xuất phân ngành phù hợp nhất cho người học.

---

## Các Tính Năng Cốt Cõi (Core Features)

1. **Giao diện Hiện đại (Web Application)**
   - Phát triển hoàn toàn trên nền tảng **Streamlit** với kiến trúc phân rã UI (Modular Architecture).
   - Thiết kế chuẩn Glassmorphism, hỗ trợ tương tác trên cả điện thoại (Mobile) và Máy tính (Desktop). Tự động tương thích độ sáng (Adaptive Dark/Light Mode).
   - Hệ thống bài trắc nghiệm tính cách MBTI chuẩn hóa với phản hồi thời gian thực qua giao diện trực quan.

2. **Cỗ máy Gợi ý Lai (Hybrid Recommender System)**
   - Đề xuất được cấu hình trên thuật toán kết hợp theo tỷ trọng 60:40 giữa hai trường phái:
     - **Content-Based Filtering (60%)**: Ứng dụng mô hình Dữ liệu đa biến với các thuật toán phân lớp (Random Forest Classifier).
     - **Collaborative Filtering (40%)**: K-Nearest Neighbors (KNN) sử dụng độ đo khoảng cách Cosine Similarity để tìm ra "5 người có hồ sơ tương đồng nhất (Láng giềng gần)".

3. **Cấu trúc Cloud-Native (Firebase Integration)**
   - **Firestore DB**: Lưu trữ và quản lý toàn bộ cấu hình câu hỏi, mô tả MBTI và lượt nhật ký truy vấn theo thời gian thực.
   - **Auto-Sync**: Dữ liệu từ Admin Dashboard được đồng bộ ngay lập tức tới người dùng thông qua cơ chế Cache thông minh.
   - **Real-time Logging**: Ghi nhận thống kê sử dụng và kết quả dự đoán trực tiếp lên Cloud để phục vụ phân tích báo cáo.

4. **Quản Trị Hệ Thống Chuyên Nghiệp (Admin Dashboard)**
   - **Xác thực Firebase Auth**: Đăng nhập Admin bảo mật bằng Email/Password qua hệ thống Firebase chính thức.
   - **Quản lý nội dung động**: Chỉnh sửa câu hỏi trắc nghiệm, hình ảnh mapping và nội dung chi tiết MBTI trực tiếp trên Dashboard mà không cần can thiệp mã nguồn.

5. **Trí tuệ nhân tạo có thể giải thích (Explainable AI - XAI)**
   - Tích hợp biểu đồ tương tác **Plotly** giải thích và minh bạch hóa lý do AI đưa ra gợi ý, trích xuất Feature Importances từ thuật toán Cây quyết định diện rộng (Random Forest). Cung cấp góc nhìn về độ nặng của MBTI hoặc Điểm số tác động như thế nào đến tỷ lệ dự đoán.

---

## Kiến Trúc Mã Nguồn (Directory Structure)

```text
LVTN2026/
├── app.py                         # File chạy chính của Web App Streamlit
├── README.md                      # Tài liệu dự án (bạn đang đọc)
├── requirements.txt               # Danh sách thư viện Python (Bổ sung: firebase-admin, requests)
├── utils/                         # Các module tiện ích hệ thống
│   └── firebase_client.py         # Kết nối Firestore và Firebase Auth
├── data/                          # Chứa dữ liệu huấn luyện và script khai báo tĩnh
│   ├── rawdata/                   # Các file dữ liệu thô gốc (Excel/CSV)
│   ├── major_db.py                # Khai báo dữ liệu đặc tả mã nhóm ngành
│   └── student_data.csv           # Dữ liệu chuẩn đã Augment với 8.000 hồ sơ
├── assets/                        # Các tài nguyên tĩnh đồ họa và module bổ trợ
│   ├── images/                    # Thư mục chứa hình họa chuẩn đoán MBTI và banner ngành
│   └── mbti_assets.py             # Bộ code xử lý dữ liệu logic MBTI đồng bộ Cloud
├── model/                         # Nơi lưu trữ Pipeline của thuật toán AI (files .joblib)
├── scripts/                       # Chứa mã nguồn tính toán và huấn luyện độc lập
│   ├── data_augmentation.py       # Script tăng cường dữ liệu khớp với phổ Bộ GD ĐT
│   └── train_model.py             # Script xử lý trích lập tập huấn luyện, chấm điểm 3 Models
├── views/                         # Kiến trúc Modules Frontend tách mảnh
│   ├── admin_dashboard.py         # View quản trị nội dung & Firebase Auth
│   ├── components.py              # Xử lý CSS, thiết kế Banner, Button, HTML chung
│   ├── sidebar.py                 # Render sidebar cài đặt thông số mô hình
│   ├── tab1_survey.py             # View phân tích điểm và gợi ý tự động
│   ├── tab2_mbti.py               # View giao diện trắc nghiệm MBTI tương tác
│   └── tab3_xai.py                # View Trí tuệ Giải Thích AI (XAI Charts)
└── .streamlit/                    # Thư mục cấu hình Streamlit
    ├── config.toml                # Quy định bảng màu Theme (Sky Blue) & thuộc tính CSS
    └── secrets.toml               # Lưu trữ Firebase API Key & Service Account (Git Ignored)
```

---

## Cài Đặt Và Khởi Chạy Môi Trường

### 1. Chuẩn bị Môi trường
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
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

### 3. Tiền khởi tạo Máy Học (Khâu Backend)
```bash
python scripts/merge_raw_data.py
python scripts/data_augmentation.py
python scripts/train_model.py
```
*(Kết quả: Sẽ tạo ra Dataset 8.000 hồ sơ và Pipeline AI tích hợp trong `model/`)*

### 4. Khởi Động Website
```bash
streamlit run app.py
```

---

## Dữ Liệu Huấn Luyện (Datasets)
Bộ Dữ liệu được xây dựng theo hình thức Data Synthesizing & Augmentation từ 3 nguồn (Indonesia MBTI Dataset, Vietnam Student Performance Scores, Vietnam AI Sinh Viên GPA Data).
- **Kích thước mẫu (Samples Size)**: `8.000` bộ hồ sơ học sinh.
- **Phân loại đầu ra (Target Classes)**: 12 nhóm chuyên ngành phổ biến.
- **Không gian Đặc trưng (Feature Space)**: 07 Điểm số thành phần thi THPT và 01 Đặc trưng MBTI sinh trắc.

---

## Thông Số Đo Lường Mô Hình (Metrics)

Kết quả đo lường khách quan thông qua **GridSearchCV** (với tập Test):

| Thuật Toán (Algorithm)            | Vai trò           | Accuracy (Thực tế) | Nhận Xét Mục Đích Sử Dụng |
| ---------------------------------- | ----------------- | -------- | ---------------- |
| **Random Forest Classifier**       | **Mô Hình Chính** | `~87.99%` | Tư vấn chính và tính Feature Importances đa chiều. |
| **SVM (Support Vector Machine)**   | Đối trọng so sánh | `~86.99%` | Phân cách siêu phẳng Nonlinear (RBF Kernel). |
| **Decision Tree**                  | Đối trọng / XAI   | `~82.36%` | Diễn giải If-Else tường minh sự rẽ nhánh. |

---
*(Bản quyền mã nguồn mở LVTN2026. Mọi thay đổi về dữ liệu và cấu hình hiện đã được Cloud hóa hoàn toàn qua Firebase Firestore).*
