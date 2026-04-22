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
        st.subheader("Quản lý Hình ảnh & Gán Tính cách / Ngành học")
        img_dir = get_abs_path("assets/images")
        mbti_mapping_file = get_abs_path("data/mbti_image_mapping.json")
        major_mapping_file = get_abs_path("data/major_image_mapping.json")
        
        if not os.path.exists(img_dir):
            st.warning("Thư mục assets/images chưa tồn tại!")
        else:
            images = sorted([f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
            
            # --- Load mappings ---
            ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
            DEFAULT_MBTI_MAP = {m: f"mbti_{m.lower()}.png" for m in ALL_MBTI}
            
            current_mbti_map = DEFAULT_MBTI_MAP.copy()
            if os.path.exists(mbti_mapping_file):
                try:
                    with open(mbti_mapping_file, 'r', encoding='utf-8') as f:
                        current_mbti_map.update(json.load(f))
                except: pass
            
            ALL_MAJORS = [
                "CNTT & Kỹ thuật Máy tính", "Kinh tế & Quản lý", "Y tế & Sức khỏe",
                "Sư phạm & Giáo dục", "Luật & Chính trị", "Ngoại ngữ & Ngôn ngữ",
                "Nghệ thuật & Thiết kế", "Kỹ thuật & Công nghệ", "Khoa học Tự nhiên",
                "Khoa học Xã hội & Nhân văn", "Nông Lâm Ngư nghiệp", "Báo chí & Truyền thông"
            ]
            DEFAULT_MAJOR_MAP = {
                "CNTT & Kỹ thuật Máy tính": "major_cntt.png", "Kinh tế & Quản lý": "major_kinhtequanly.png",
                "Y tế & Sức khỏe": "major_medical.png", "Sư phạm & Giáo dục": "major_education.png",
                "Luật & Chính trị": "major_education.png", "Ngoại ngữ & Ngôn ngữ": "major_education.png",
                "Nghệ thuật & Thiết kế": "major_education.png", "Kỹ thuật & Công nghệ": "major_engineering.png",
                "Khoa học Tự nhiên": "major_engineering.png", "Khoa học Xã hội & Nhân văn": "major_education.png",
                "Nông Lâm Ngư nghiệp": "major_engineering.png", "Báo chí & Truyền thông": "major_business.png",
            }
            current_major_map = DEFAULT_MAJOR_MAP.copy()
            if os.path.exists(major_mapping_file):
                try:
                    with open(major_mapping_file, 'r', encoding='utf-8') as f:
                        current_major_map.update(json.load(f))
                except: pass
            
            # === PHẦN 1: Upload ảnh mới ===
            st.markdown("#### Upload hình ảnh mới")
            st.info("Tải lên ảnh mới hoặc ghi đè ảnh cũ. Ảnh sẽ được lưu vào thư mục assets/images/.")
            up_col1, up_col2 = st.columns([1, 1])
            with up_col1:
                uploaded_file = st.file_uploader("Chọn file ảnh từ máy tính", type=["png", "jpg", "jpeg"], key="upload_new")
            with up_col2:
                if uploaded_file:
                    new_filename = st.text_input("Tên file lưu (có đuôi .png/.jpg):", value=uploaded_file.name)
                    if st.button("Tải lên & Lưu", type="primary"):
                        save_path = os.path.join(img_dir, new_filename)
                        with open(save_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        st.success(f"Đã lưu thành công: {new_filename}")
                        st.rerun()
            
            st.divider()
            images = sorted([f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
            
            # === PHẦN 2: Gán ảnh cho TỪNG loại MBTI ===
            st.markdown("#### Gán hình ảnh cho từng Tính cách MBTI (16 loại)")
            st.info("Chọn ảnh riêng biệt cho mỗi loại MBTI. Thay đổi sẽ cập nhật ngay tới giao diện Người dùng.")
            
            mbti_changed = False
            MBTI_GROUPS_DISPLAY = {
                "Nhà Phân Tích (Analysts)": ["INTJ", "INTP", "ENTJ", "ENTP"],
                "Nhà Ngoại Giao (Diplomats)": ["INFJ", "INFP", "ENFJ", "ENFP"],
                "Người Canh Gác (Sentinels)": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"],
                "Nhà Thám Hiểm (Explorers)": ["ISTP", "ISFP", "ESTP", "ESFP"],
            }
            for group_name, types in MBTI_GROUPS_DISPLAY.items():
                with st.expander(f"{group_name}", expanded=False):
                    cols = st.columns(len(types))
                    for i, mbti_type in enumerate(types):
                        with cols[i]:
                            cur_img = current_mbti_map.get(mbti_type, images[0] if images else "")
                            cur_idx = images.index(cur_img) if cur_img in images else 0
                            st.markdown(f"**{mbti_type}**")
                            if cur_img in images:
                                st.image(os.path.join(img_dir, cur_img), use_container_width=True)
                            new_choice = st.selectbox(f"Ảnh {mbti_type}:", images, index=cur_idx, key=f"mbti_img_{mbti_type}", label_visibility="collapsed")
                            if current_mbti_map.get(mbti_type) != new_choice:
                                current_mbti_map[mbti_type] = new_choice
                                mbti_changed = True
            
            if mbti_changed:
                st.warning("Bạn đã thay đổi cấu hình ảnh MBTI.")
            if st.button("Lưu cấu hình Ảnh MBTI", type="primary", use_container_width=True):
                with open(mbti_mapping_file, 'w', encoding='utf-8') as f:
                    json.dump(current_mbti_map, f, ensure_ascii=False, indent=2)
                st.success("Đã lưu! Giao diện Người dùng sẽ cập nhật ảnh MBTI mới.")
                st.rerun()
            
            st.divider()
            
            # === PHẦN 3: Gán ảnh cho 12 Nhóm ngành ===
            with st.expander("Gán hình ảnh cho 12 Nhóm ngành Chuyên ngành", expanded=False):
                st.info("Khi dự đoán ngành, hệ thống sẽ hiển thị ảnh minh họa tương ứng với nhóm ngành được gợi ý.")
                
                major_changed = False
                m_cols_per_row = 3
                for row_start in range(0, len(ALL_MAJORS), m_cols_per_row):
                    row_majors = ALL_MAJORS[row_start:row_start + m_cols_per_row]
                    m_cols = st.columns(m_cols_per_row)
                    for i, major in enumerate(row_majors):
                        with m_cols[i]:
                            cur_img = current_major_map.get(major, images[0] if images else "")
                            cur_idx = images.index(cur_img) if cur_img in images else 0
                            st.markdown(f"**{major}**")
                            new_choice = st.selectbox(f"Ảnh:", images, index=cur_idx, key=f"major_img_{major}", label_visibility="collapsed")
                            # Hiển thị ảnh đang chọn (cập nhật ngay khi đổi)
                            if new_choice and new_choice in images:
                                st.image(os.path.join(img_dir, new_choice), use_container_width=True, caption=new_choice)
                            if current_major_map.get(major) != new_choice:
                                current_major_map[major] = new_choice
                                major_changed = True
                
                if major_changed:
                    st.warning("Bạn đã thay đổi cấu hình ảnh Ngành học.")
                if st.button("Lưu cấu hình Ảnh Ngành học", type="primary", use_container_width=True):
                    with open(major_mapping_file, 'w', encoding='utf-8') as f:
                        json.dump(current_major_map, f, ensure_ascii=False, indent=2)
                    st.success("Đã lưu! Ảnh minh họa ngành học sẽ cập nhật ngay.")
                    st.rerun()

    # Tab 4: Thống Kê & XAI
    with admin_tab4:
        import pandas as pd
        from collections import Counter
        
        st.subheader("Báo Cáo Hoạt Động & Phân Tích")
        
        # 1. Đọc dữ liệu thống kê
        stats_file = get_abs_path("data/usage_statistics.json")
        pred_count = 0
        logs = []
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats_data = json.load(f)
                    pred_count = stats_data.get("prediction_count", 0)
                    logs = stats_data.get("logs", [])
            except:
                pass
        
        # ---- METRIC TỔNG QUAN ----
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 20px; border-radius: 12px; border: 1px solid #bae6fd; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <p style="margin: 0; font-size: 0.8rem; color: #0284c7; font-weight: 700; text-transform: uppercase;">Tổng lượt Tư vấn</p>
                <h2 style="margin: 5px 0 0 0; color: #0369a1; font-size: 2.5rem; font-weight: 900;">{pred_count:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            unique_mbti = len(set(l.get("mbti","") for l in logs if l.get("mbti")))
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); padding: 20px; border-radius: 12px; border: 1px solid #86efac; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <p style="margin: 0; font-size: 0.8rem; color: #16a34a; font-weight: 700; text-transform: uppercase;">Loại MBTI đã khảo sát</p>
                <h2 style="margin: 5px 0 0 0; color: #15803d; font-size: 2.5rem; font-weight: 900;">{unique_mbti}/16</h2>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            unique_majors = len(set(l.get("top1_major","") for l in logs if l.get("top1_major")))
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%); padding: 20px; border-radius: 12px; border: 1px solid #fde047; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <p style="margin: 0; font-size: 0.8rem; color: #ca8a04; font-weight: 700; text-transform: uppercase;">Nhóm ngành được gợi ý</p>
                <h2 style="margin: 5px 0 0 0; color: #a16207; font-size: 2.5rem; font-weight: 900;">{unique_majors}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        
        if len(logs) > 0:
            df_logs = pd.DataFrame(logs)
            
            # ---- BIỂU ĐỒ PHÂN BỐ ----
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown("##### Phân bố MBTI được sử dụng")
                if "mbti" in df_logs.columns:
                    mbti_counts = df_logs["mbti"].value_counts()
                    st.bar_chart(mbti_counts)
            
            with chart_col2:
                st.markdown("##### Top Nhóm ngành được gợi ý nhiều nhất")
                if "top1_major" in df_logs.columns:
                    major_counts = df_logs["top1_major"].value_counts()
                    st.bar_chart(major_counts)
            
            st.write("")
            chart_col3, chart_col4 = st.columns(2)
            
            with chart_col3:
                st.markdown("##### Phân bố Khối thi")
                if "khoi_thi" in df_logs.columns:
                    khoi_counts = df_logs["khoi_thi"].value_counts()
                    st.bar_chart(khoi_counts)
            
            with chart_col4:
                st.markdown("##### Lượt truy cập theo ngày")
                if "time" in df_logs.columns:
                    df_logs["date"] = pd.to_datetime(df_logs["time"], errors="coerce").dt.date
                    daily_counts = df_logs.groupby("date").size()
                    st.line_chart(daily_counts)
            
            # ---- BẢNG CHI TIẾT ----
            st.divider()
            st.markdown("##### Nhật ký Truy vấn Gần đây (Mới nhất → Cũ nhất)")
            df_display = df_logs[["time", "mbti", "khoi_thi", "top1_major"]].copy()
            df_display.columns = ["Thời gian", "MBTI", "Khối thi", "Ngành gợi ý Top 1"]
            st.dataframe(df_display.iloc[::-1].reset_index(drop=True), use_container_width=True, height=300)

            # Nút reset
            if st.button("Xoá toàn bộ dữ liệu Thống kê", type="secondary"):
                with open(stats_file, 'w', encoding='utf-8') as f:
                    json.dump({"prediction_count": 0, "logs": []}, f)
                st.success("Đã xoá dữ liệu thống kê!")
                st.rerun()
        else:
            st.info("Chưa có dữ liệu thống kê nào. Hệ thống sẽ bắt đầu ghi nhận khi người dùng thực hiện dự đoán.")
        
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
