# Nghiên cứu và Xây dựng hệ thống hỗ trợ tư vấn chọn ngành đại học dựa trên kỹ thuật Phân lớp dữ liệu đa yếu tố: Tính cách và Năng lực học tập
**Dự án Khóa luận Tốt nghiệp (LVTN 2026)**

> **Tên đề tài tiếng Anh**: "Development of a University Major Recommendation System using Multi-factor Classification: Personality Traits (MBTI) and Academic Performance"

Đây là một dự án ứng dụng trí tuệ nhân tạo (Học máy lai - Hybrid Machine Learning) nhằm mục đích giải quyết bài toán định hướng nghề nghiệp cho học sinh Trung học Phổ thông. Thay vì chỉ dựa trên điểm số tĩnh hoặc một bài trắc nghiệm đơn điệu, ứng dụng này kết hợp hiệu quả Giới tuyến Sinh trắc học (Trắc nghiệm tính cách MBTI) và Năng lực cốt lõi (Điểm thi THPT) để tạo ra các đề xuất phân ngành phù hợp nhất cho người học.

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

3. **Trợ lý Ảo AI (Gemini Chatbot Integration)**
   - Tích hợp Chatbot thông minh sử dụng **Google Gemini AI** (thông qua SDK `google-genai`).
   - Widget nổi (Floating Widget) góc màn hình, giao diện bong bóng chat hiện đại, hỗ trợ nhận diện và hiển thị giao diện mượt mà trên mọi thiết bị.
   - Hỗ trợ tư vấn, giải đáp thắc mắc về tuyển sinh, ngành nghề và tâm lý học đường theo thời gian thực.
   - Quản trị viên có thể tùy chỉnh Câu hỏi gợi ý mặc định trực tiếp qua Admin Dashboard.

4. **Cấu trúc Cloud-Native (Firebase & Cloudinary Integration)**
   - **Firestore DB**: Lưu trữ cấu hình câu hỏi MBTI, mô tả MBTI, danh sách trường THPT, lịch sử cấu hình và mapping nhóm ngành/ảnh.
   - **Cloudinary CDN**: Lưu trữ, tối ưu hóa và phân phối hình ảnh 3D đại diện cho 16 nhóm tính cách và 12 nhóm ngành học với tốc độ cao.
   - **Auto-Sync**: Dữ liệu từ Admin Dashboard được đồng bộ ngay lập tức tới Frontend thông qua cơ chế Cache thông minh.

5. **Quản Trị Hệ Thống Chuyên Nghiệp (Admin Dashboard)**
   - **Xác thực Firebase Auth**: Đăng nhập Admin bảo mật bằng Email/Password qua hệ thống Firebase.
   - **Quản lý toàn diện**: Cấu hình Chatbot, quản lý câu hỏi MBTI (tải lên file Excel/CSV), cập nhật danh sách trường THPT, thay đổi hình ảnh chuyên ngành, và xem báo cáo.

6. **Trí tuệ nhân tạo có thể giải thích (Explainable AI - XAI)**
   - Tích hợp biểu đồ tương tác **Plotly** giải thích và minh bạch hóa lý do AI đưa ra gợi ý, trích xuất Feature Importances từ thuật toán Cây quyết định (Random Forest). Cung cấp góc nhìn về độ nặng của MBTI hoặc Điểm số tác động như thế nào đến dự đoán.

---

## Kiến Trúc Mã Nguồn (Directory Structure)

```text
LVTN2026/
├── app.py                         # File chạy chính của Web App Streamlit
├── README.md                      # Tài liệu dự án
├── requirements.txt               # Danh sách thư viện Python
├── utils/                         # Các module tiện ích hệ thống
│   ├── cloudinary_client.py       # Client quản lý ảnh với Cloudinary
│   └── firebase_client.py         # Kết nối Firestore, Firebase Auth và cấu hình hệ thống
├── data/                          # Chứa dữ liệu huấn luyện và script khai báo tĩnh
│   ├── rawdata/                   # Các file dữ liệu thô gốc (Excel/CSV)
│   ├── questions/                 # Dữ liệu câu hỏi trắc nghiệm
│   ├── major_db.py                # Khai báo dữ liệu đặc tả mã nhóm ngành
│   └── major_image_mapping.json   # Cấu hình mapping ảnh-ngành
├── assets/                        # Các tài nguyên tĩnh đồ họa và module bổ trợ
│   ├── images/                    # Thư mục chứa hình họa nhóm ngành và MBTI
│   └── mbti_assets.py             # Bộ code xử lý dữ liệu logic MBTI & Ngành học đồng bộ Cloud
├── model/                         # Nơi lưu trữ Pipeline của thuật toán AI (files .joblib)
├── scripts/                       # Chứa mã nguồn tính toán và huấn luyện độc lập
│   ├── data_augmentation.py       # Script tăng cường dữ liệu khớp với phổ Bộ GD ĐT
│   ├── hybrid_recommender.py      # Hệ thống gợi ý lai (Content-based & CF)
│   ├── merge_raw_data.py          # Script kết hợp dữ liệu thô
│   └── train_model.py             # Script xử lý trích lập tập huấn luyện, chấm điểm 3 Models
├── views/                         # Kiến trúc Modules Frontend tách mảnh
│   ├── admin_dashboard.py         # View quản trị nội dung, ảnh & Firebase Auth
│   ├── chatbot_widget.py          # Component giao diện Chatbot nổi
│   ├── components.py              # Xử lý CSS, thiết kế Banner, Button, HTML chung
│   ├── sidebar.py                 # Render sidebar cài đặt thông số mô hình
│   ├── tab1_survey.py             # View phân tích điểm và gợi ý tự động
│   ├── tab2_mbti.py               # View giao diện trắc nghiệm MBTI tương tác
│   └── tab3_xai.py                # View Trí tuệ Giải Thích AI (XAI Charts)
├── docs/                          # Thư mục chứa tài liệu báo cáo và slide bảo vệ
└── .streamlit/                    # Thư mục cấu hình Streamlit
    ├── config.toml                # Quy định bảng màu Theme (Sky Blue) & thuộc tính CSS
    └── secrets.toml               # Lưu trữ Firebase, Cloudinary & Gemini API Keys (Git Ignored)
```

---

## Cài Đặt Và Khởi Chạy Môi Trường

### 1. Chuẩn bị Môi trường
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux (hoặc venv\Scripts\activate trên Windows)
pip install -r requirements.txt
```

### 2. Cấu hình Dịch vụ (Bắt buộc)
Dự án được Cloud hóa hoàn toàn. Bạn cần tạo tệp `.streamlit/secrets.toml` để cấu hình API cho **Firebase**, **Cloudinary** và **Gemini**:
```toml
[firebase]
api_key = "..."

[firebase_service_account]
type = "service_account"
project_id = "..."
private_key = """-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----"""
client_email = "..."

[cloudinary]
cloud_name = "..."
api_key = "..."
api_secret = "..."

[gemini]
api_key = "..."
```

### 3. Tiền khởi tạo Máy Học (Khâu Backend)
```bash
python scripts/merge_raw_data.py
python scripts/data_augmentation.py
python scripts/train_model.py
```
*(Kết quả: Sẽ tạo ra Dataset 8.000 hồ sơ và Pipeline AI tích hợp trong thư mục `model/`)*

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

| Thuật Toán (Algorithm)            | Vai trò           | Train Accuracy | Test Accuracy | Nhận Xét Mục Đích Sử Dụng |
| ---------------------------------- | ----------------- | -------------- | ------------- | ---------------- |
| **Random Forest Classifier**       | **Mô Hình Chính** | `~93.98%`      | `~87.37%`     | Tư vấn chính và tính Feature Importances đa chiều. |
| **SVM (Support Vector Machine)**   | Đối trọng so sánh | `~87.14%`      | `~86.80%`     | Phân cách siêu phẳng Nonlinear (RBF Kernel). |
| **Decision Tree**                  | Đối trọng / XAI   | `~83.50%`      | `~79.55%`     | Diễn giải If-Else tường minh sự rẽ nhánh. |

---
*(Bản quyền mã nguồn mở LVTN2026. Tích hợp AI toàn diện và Cloud-Native architecture).*
