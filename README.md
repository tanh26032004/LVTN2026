# Hệ thống Gợi ý Chuyên ngành Đại học

Dự án Khóa luận tốt nghiệp: "Development of a University Major Recommendation System using Multi-factor Classification: Personality Traits (MBTI) and Academic Performance"

## Cấu trúc dự án
- `data/`: Chứa dữ liệu thô và mock data.
- `model/`: Các file mô hình học máy (.joblib).
- `scripts/`: Chứa mã nguồn sinh dữ liệu và huấn luyện mô hình.
- `assets/`: Biểu đồ, hình ảnh tĩnh phục vụ cho UI và Document.
- `docs/`: Chứa slide và báo cáo Word.
- `app.py`: Ứng dụng web Streamlit.
- `requirements.txt`: Các thư viện yêu cầu.

## Cài đặt và sử dụng
1. Tạo môi trường ảo và cài đặt thư viện:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Sinh dữ liệu giả lập (Mock data):
   ```bash
   python scripts/generate_mock_data.py
   ```
3. Huấn luyện hệ thống AI:
   ```bash
   python scripts/train_model.py
   ```
4. Khởi chạy Ứng dụng Website:
   ```bash
   streamlit run app.py
   ```
