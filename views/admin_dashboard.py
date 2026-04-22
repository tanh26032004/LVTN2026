import streamlit as st
import json
import os
from views import tab1_survey, tab2_mbti, tab3_xai

def get_abs_path(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", relative_path))

def render_admin_dashboard(rf_model, dt_model, svm_model, preprocessor, target_encoder, major_dict):
    st.markdown("<h2 style='color:#0ea5e9; text-align:center;'>Trang Quản Trị Hệ Thống (Admin Dashboard)</h2>", unsafe_allow_html=True)
    st.divider()

    # 1. Đăng nhập
    if not st.session_state.get('is_admin_logged_in', False):
        st.markdown("<div style='background-color: #f8fafc; padding: 30px; border-radius: 15px; border: 1px solid #e2e8f0; width: 60%; margin: auto;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #0ea5e9; font-weight: 800; margin-bottom: 25px;'>Xác Thực Cấp Cao</h3>", unsafe_allow_html=True)
        pwd = st.text_input("Nhập mã truy cập (Password):", type="password")
        import hashlib
        if st.button("Đăng Nhập Quản Trị", type="primary", use_container_width=True):
            # Check secret hash
            pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
            try:
                secret_hash = st.secrets["admin"]["password_hash"]
            except Exception:

                secret_hash = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9" 
            
            if pwd_hash == secret_hash:
                st.session_state['is_admin_logged_in'] = True
                st.rerun()
            else:
                st.error("Mật khẩu không chính xác!")
        st.markdown("</div>", unsafe_allow_html=True)
        return "Random Forest (Khuyên dùng)", rf_model # model_choice, active_model fallback
    
    # KHI ĐÃ ĐĂNG NHẬP
    admin_tab1, admin_tab2, admin_tab3, admin_tab4, admin_tab5, admin_tab6 = st.tabs([
        "Lõi Mô Hình", "Quản lý MBTI", "Quản lý Hình Ảnh", "Thống Kê & XAI", "Test: Khảo sát", "Test: MBTI"
    ])
    
    # Tab 1: Cấu hình mô hình
    with admin_tab1:
        st.subheader("Cấu hình Thuật toán Gợi ý cốt lõi")
        model_choice = st.selectbox(
            "Lựa chọn Thuật toán Core (Chỉ áp dụng trong phiên làm việc này):",
            ["Random Forest (Khuyên dùng)", "Decision Tree", "SVM (RBF Kernel)"]
        )
        if model_choice.startswith("Random Forest"): active_model = rf_model
        elif model_choice.startswith("Decision Tree"): active_model = dt_model
        else: active_model = svm_model
        
        # Lưu vào trạng thái
        st.session_state['admin_model_choice'] = model_choice
        st.session_state['admin_active_model'] = active_model
        
        st.success(f"Thuật toán Admin đang hoạt động: {model_choice}")
        
    # Tab 2: Quản lý JSON MBTI
    with admin_tab2:
        st.subheader("Trình Quản Lý Dữ liệu Câu hỏi MBTI")
        mbti_path = get_abs_path("data/questions/mbti_questions.json")
        try:
            with open(mbti_path, 'r', encoding='utf-8') as f:
                mbti_data = json.load(f)
            
            st.info(f"Đang hiển thị {len(mbti_data)} câu hỏi MBTI trong cơ sở dữ liệu. Bấm đúp vào ô để sửa. Có thể thêm dòng mới ở cuối bảng.")
            edited_data = st.data_editor(mbti_data, num_rows="dynamic", use_container_width=True, height=500)
            
            if st.button("Lưu file JSON", type="primary"):
                with open(mbti_path, 'w', encoding='utf-8') as f:
                    json.dump(edited_data, f, ensure_ascii=False, indent=4)
                st.success("Đã ghi đè file mbti_questions.json thành công!")
        except Exception as e:
            st.error(f"Lỗi khi tải dữ liệu MBTI: {e}")
            
    # Tab 3: Quản lý Assets Hình ảnh
    with admin_tab3:
        st.subheader("Chỉnh sửa Asset Giao Diện")
        st.info("Hệ thống thay đổi nhận diện thương hiệu. Các file được upload sẽ ghi đè lên ảnh gốc và ảnh hưởng toàn bộ người dùng ngay lập tức.")
        img_dir = get_abs_path("assets/images")
        if not os.path.exists(img_dir):
            st.warning("Thư mục assets/images chưa tồn tại!")
        else:
            images = [f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
            
            selected_img = st.selectbox("Chọn ảnh cần thay thế:", images)
            if selected_img:
                img_path = os.path.join(img_dir, selected_img)
                c1, c2 = st.columns([1,1])
                with c1:
                    st.image(img_path, caption=f"Ảnh cũ", use_container_width=True)
                with c2:
                    uploaded_file = st.file_uploader(f"Tải ảnh mới từ thiết bị", type=["png", "jpg", "jpeg"])
                    if uploaded_file is not None:
                        if st.button("Upload & Ghi đè", type="primary"):
                            with open(img_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            st.success(f"Quá trình tải lên thành công: {selected_img}")
                            st.rerun()

    # Tab 4: Thống Kê & XAI
    with admin_tab4:
        st.subheader("Báo Cáo Hoạt Động & Phân Tích Nội Tại")
        
        # 1. Đọc và hiển thị số đếm lượt hệ thống được dùng
        stats_file = get_abs_path("data/usage_statistics.json")
        pred_count = 0
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats_data = json.load(f)
                    pred_count = stats_data.get("prediction_count", 0)
            except:
                pass
                
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 20px; border-radius: 12px; border: 1px solid #bae6fd; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 30px;">
            <p style="margin: 0; font-size: 0.95rem; color: #0284c7; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Tổng Lượt Hệ Thống Tư Vấn Thành Công</p>
            <h2 style="margin: 5px 0 0 0; color: #0369a1; font-size: 3rem; font-weight: 900;">{pred_count:,}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("<h3 style='color: #0f172a;'>Giải Thích AI (XAI)</h3>", unsafe_allow_html=True)
        # Render tab XAI
        tab3_xai.render_tab(active_model, model_choice)

    # Tab 5: Test Khảo sát
    with admin_tab5:
        st.subheader("Giao diện Thử nghiệm Thực tế: Khảo sát Phân tích")
        tab1_survey.render_tab(active_model, model_choice, preprocessor, target_encoder, major_dict)

    # Tab 6: Test MBTI
    with admin_tab6:
        st.subheader("Giao diện Thử nghiệm Thực tế: Trắc nghiệm MBTI")
        tab2_mbti.render_tab()

    st.markdown("<hr style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("Đăng xuất & Thoát Dashboard", type="secondary"):
        st.session_state['is_admin_logged_in'] = False
        st.rerun()
        
    return st.session_state.get('admin_model_choice', "Random Forest (Khuyên dùng)"), st.session_state.get('admin_active_model', rf_model)
