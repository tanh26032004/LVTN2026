# Nghiên cứu và Xây dựng hệ thống hỗ trợ tư vấn chọn ngành đại học dựa trên kỹ thuật Phân lớp dữ liệu đa yếu tố: Tính cách và Năng lực học tập
**Dự án Khóa luận Tốt nghiệp (LVTN 2026)**

> **Tên đề tài tiếng Anh**: "Development of a University Major Recommendation System using Multi-factor Classification: Personality Traits (MBTI) and Academic Performance"

Đây là một dự án ứng dụng trí tuệ nhân tạo (Học máy lai - Hybrid Machine Learning) nhằm mục đích giải quyết bài toán định hướng nghề nghiệp cho học sinh Trung học Phổ thông. Thay vì chỉ dựa trên điểm số tĩnh hoặc một bài trắc nghiệm đơn điệu, ứng dụng này kết hợp hiệu quả Giới tuyến Sinh trắc học (Trắc nghiệm tính cách MBTI) và Năng lực cốt lõi (Điểm thi THPT 7 môn học) để tạo ra các đề xuất phân ngành phù hợp nhất cho người học.

---

## 🌟 Các Tính Năng Cốt Lõi (Core Features)

1. **Giao diện Hiện đại (Web Application)**
   - Phát triển hoàn toàn trên nền tảng **Streamlit** với kiến trúc phân rã UI (Modular Architecture).
   - Thiết kế chuẩn Glassmorphism, hỗ trợ tương tác trên cả điện thoại (Mobile) và Máy tính (Desktop). Tự động tương thích độ sáng (Adaptive Dark/Light Mode).
   - Hệ thống bài trắc nghiệm tính cách MBTI chuẩn hóa với phản hồi thời gian thực qua giao diện trực quan.

2. **Cỗ máy Gợi ý Lai (Hybrid Recommender System)**
   - Đề xuất được cấu hình trên thuật toán kết hợp theo tỷ trọng 60:40 giữa hai trường phái:
     - **Content-Based Filtering (60%)**: Ứng dụng mô hình Dữ liệu đa biến với các thuật toán phân lớp (Random Forest Classifier).
     - **Collaborative Filtering (40%)**: K-Nearest Neighbors (KNN) sử dụng độ đo khoảng cách Cosine Similarity để tìm ra "5 người có hồ sơ tương đồng nhất (Láng giềng gần)".

3. **Tối ưu Hóa Máy Học (Machine Learning Optimization)**
   - **Feature Engineering** Tự động tổng hợp điểm Nhóm ngành Khoa học Tự nhiên (KHTN), Khoa học Xã hội (KHXH), và Điểm Trung Bình.
   - **One-Hot Encoding**: Đặc trưng MBTI được rẽ nhánh nhị phân chống lệch không gian vectơ.
   - **Tham số hóa tự động với Pipeline**: Toàn bộ điểm số được nội suy qua `StandardScaler` tích hợp sâu trong `sklearn.pipeline` trước khi chấm điểm SVM hay KNN.
   - Lưới GridSearchCV quét cạn để xác lập tối ưu tham số (Hyperparameter tuning).

4. **Trí tuệ nhân tạo có thể giải thích (Explainable AI - XAI)**
   - Tích hợp biểu đồ tương tác **Plotly** giải thích và minh bạch hóa lý do AI đưa ra gợi ý, trích xuất Feature Importances từ thuật toán Cây quyết định diện rộng (Random Forest). Cung cấp góc nhìn về độ nặng của MBTI hoặc Toán/Văn tác động như thế nào đến tỷ lệ.

---

## 📂 Kiến Trúc Mã Nguồn (Directory Structure)

```text
LVTN2026/
├── app.py                         # FIle chạy chính của Web App Streamlit
├── README.md                      # Tài liệu dự án (bạn đang đọc)
├── requirements.txt               # Danh sách thư viện Python cần thiết
├── data/                          # Chứa kho dữ liệu
│   └── student_data.csv           # File Mock Data (Sinh ngẫu nhiên với luật ruleset chuyên ngành)
├── docs/                          # Thư mục lưu trữ báo cáo, slide báo cáo KLTN
├── assets/                        # Các icon, hình ảnh dùng trong dự án
├── model/                         # Lưu trữ các file Model Machine Learning (.joblib) đã được Train
├── scripts/                       # Chứa mã nguồn tính toán Logic, ML, Data
│   ├── generate_mock_data.py      # Sinh dữ liệu giả lập cho 12 nhóm ngành
│   ├── hybrid_recommender.py      # Thuật toán tính toán lai (Hybrid) cho web
│   └── train_model.py             # Script nạp dữ liệu, tiền xử lý, huấn luyện 3 thuật toán và lưu file
└── views/                         # Kiến trúc Modules (Tái cấu trúc từ Monolithic) cho Frontend
    ├── components.py              # Xử lý CSS, thiết kế Banner, HTML dùng chung
    ├── sidebar.py                 # Render sidebar tùy chỉnh ML Models
    ├── tab1_survey.py             # View phân tích điểm số
    ├── tab2_mbti.py               # View làm trắc nghiệm MBTI
    └── tab3_xai.py                # View Explainable AI Interactive Charts
```

---

## ⚙️ Cài Đặt Và Khởi Chạy Môi Trường

### 1. Chuẩn bị Môi trường Ảo (Khuyên dùng)
Dự án được xây dựng và tối ưu tính nhất quán qua môi trường nội bộ.
```bash
python -m venv venv

# Kích hoạt trên Mac/Linux
source venv/bin/activate
# Hoặc trên Windows:
# venv\Scripts\activate

# Cài đặt toàn bộ thư viện (Pandas, Plotly, Scikit-learn, Streamlit...)
pip install -r requirements.txt
```

### 2. Tiền khởi tạo Máy Học (Khâu Backend)
Hệ thống AI không tự sinh ra, bạn cần tạo dữ liệu và dạy cho nó học trước khi lên Web. Thực thi hai lệnh sau theo thứ tự:

Cú pháp để **sinh dữ liệu giả lập**:
```bash
python scripts/generate_mock_data.py
```
*(Kết quả: Sẽ tạo ra file `data/student_data.csv` mô phỏng 2500 học sinh).*

Cú pháp để **Huấn luyện Mô hình AI**:
```bash
python scripts/train_model.py
```
*(Kết quả: Sẽ tạo ra Pipeline tích hợp Scaler, OneHot và Model dưới dạng đuôi `.joblib` vào ngăn `model/`)*

### 3. Khởi Động Website
Mọi thông số kỹ thuật đã sẵn sàng, hãy triển khai Frontend Framework:
```bash
streamlit run app.py
```

Trình duyệt của bạn sẽ tự bật lên ở cổng `http://localhost:8501`.

---

## 📊 Dữ Liệu Huấn Luyện (Datasets)
Bộ Dữ liệu (Mock Data) được xây dựng theo hình thức Data Synthesizing (Tự động sinh thực thể ảo), mô phỏng ma trận điểm số và tính cách dựa trên các hệ luật thực tiễn của quy chế tuyển sinh Đại học và tâm lý học hành vi:
- **Kích thước mẫu (Samples Size)**: `2500` học sinh (chia test_size=0.2 để huấn luyện độc lập).
- **Phân loại đầu ra (Target Classes)**: Tổng cộng 12 nhóm chuyên ngành phổ biến như `CNTT & Kỹ thuật Máy tính`, `Kinh tế & Quản lý`, `Nghệ thuật & Thiết kế`, `Y tế & Sức khỏe`, v.v...
- **Không gian Đặc trưng (Feature Space)**:
  - 07 Điểm số thành phần khối phổ thông: Toán, Ngữ Văn, Tiếng Anh, Vật lý, Hóa học, Sinh học, Lịch sử.
  - 01 Đặc trưng MBTI sinh trắc tâm lý.
- **Dữ liệu phái sinh tự động (Derived Features)**: Trung bình cộng `avg_score`, KHTN Tổ hợp `natural_science_score`, KHXH Tổ hợp `social_science_score`.

---

## 🔬 Thông Số Đo Lường Mô Hình Đã Huấn Luyện (Metrics)
Trong quá trình đào tạo với cơ sở dữ liệu trên, dự án đã sử dụng *GridSearchCV* để tối ưu siêu tham số. Kết quả trả về trên File phân tích tập Test độc lập đạt báo cáo đo lường cực kỳ khả quan:

| Thuật Toán (Algorithm)            | Vai trò           | Accuracy | Precision | F1-Score | Mục Đích Sử Dụng |
| ---------------------------------- | ----------------- | -------- | --------- | -------- | ---------------- |
| **Random Forest Classifier**       | **Mô Hình Chính** | `91.80%` | 92.06%    | 91.81%   | Là cỗ máy phân loại chính, không bị Overfitting do dùng tập hợp nhiều cây quyết định, có Explainable AI để trích xuất Feature Importances. |
| **Decision Tree**                  | Đối trọng / XAI   | `90.20%` | 90.42%    | 90.21%   | Dễ vẽ cây nội suy, giải thích rõ các node if-else bị rẽ nhánh bởi Môn học hay MBTI. |
| **SVM (Support Vector Machine)**   | Đối trọng so sánh | `89.80%` | 90.53%    | 89.84%   | Ứng dụng chiếu Nonlinear (RBF Kernel). Đã lược bớt siêu tham số (C=0.05) để điều chỉnh biên học nhằm giảm overfitting trong tập mẫu nhỏ. |

*(Bản quyền mã nguồn mở LVTN2026. Sinh viên có thể tùy biến source code với hàm lượng Dataset mở rộng để ứng dụng cho Đăng ký Tuyển Sinh thực tế)*.
