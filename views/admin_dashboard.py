import streamlit as st
import json
import os
from views import tab1_survey, tab2_mbti, tab3_xai

def get_abs_path(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", relative_path))

def render_admin_dashboard(rf_model, dt_model, svm_model, preprocessor, target_encoder, major_dict):
    st.markdown("<h1 style='color:#0ea5e9; text-align:center;'>Trang Quản Trị Hệ Thống</h1>", unsafe_allow_html=True)
    st.divider()

    # 1. Đăng nhập
    if not st.session_state.get('is_admin_logged_in', False):
        st.markdown("<div style='background-color: #f8fafc; padding: 30px; border-radius: 15px; border: 1px solid #e2e8f0; width: 60%; margin: auto;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #0ea5e9; font-weight: 800; margin-bottom: 25px;'>Quản Trị Viên (Firebase Auth)</h3>", unsafe_allow_html=True)
        
        email = st.text_input("Email Quản trị:", placeholder="admin@example.com")
        pwd = st.text_input("Mật khẩu:", type="password")
        
        if st.button("Đăng Nhập Hệ Thống", type="primary", use_container_width=True):
            from utils.firebase_client import verify_admin_login
            success, message = verify_admin_login(email, pwd)
            
            if success:
                st.session_state['is_admin_logged_in'] = True
                st.success(message)
                st.rerun()
            else:
                st.error(f"Đăng nhập thất bại: {message}")
        
        st.markdown("<p style='text-align:center; font-size:0.8rem; color:gray; margin-top:20px;'>Hệ thống sử dụng xác thực bảo mật qua Google Firebase</p>", unsafe_allow_html=True)
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
        st.subheader("Trình Quản Lý Dữ liệu MBTI (Firebase)")
        
        mbti_sub_tab1, mbti_sub_tab2 = st.tabs(["Câu hỏi Trắc nghiệm", "Mô tả Chi tiết (Markdown)"])
        
        with mbti_sub_tab1:
            try:
                from utils.firebase_client import fb_get_mbti_questions, fb_save_mbti_questions
                mbti_data = fb_get_mbti_questions()
                
                st.info(f"Đang hiển thị {len(mbti_data)} câu hỏi MBTI. Bấm đúp vào ô để sửa.")
                edited_questions = st.data_editor(mbti_data, num_rows="dynamic", use_container_width=True, height=400, key="editor_questions")
                
                if st.button("Lưu Câu hỏi", type="primary"):
                    fb_save_mbti_questions(edited_questions)
                    st.success("Đã đồng bộ câu hỏi lên Firebase!")
                    st.cache_data.clear() # Clear cache to reflect changes
            except Exception as e:
                st.error(f"Lỗi: {e}")

        with mbti_sub_tab2:
            try:
                from utils.firebase_client import fb_get_mbti_comprehensive, fb_save_mbti_comprehensive
                comp_data = fb_get_mbti_comprehensive()
                
                st.info("Chỉnh sửa nội dung Markdown mô tả chi tiết cho từng nhóm tính cách.")
                
                all_types = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
                selected_type = st.selectbox("Chọn nhóm tính cách để sửa nội dung:", all_types)
                
                current_text = comp_data.get(selected_type, "Chưa có dữ liệu.")
                new_text = st.text_area(f"Nội dung Markdown cho {selected_type}:", value=current_text, height=300)
                
                if st.button(f"Lưu Nội dung {selected_type}", type="primary"):
                    comp_data[selected_type] = new_text
                    fb_save_mbti_comprehensive(comp_data)
                    st.success(f"Đã cập nhật nội dung cho {selected_type} trên Firebase!")
                    st.cache_data.clear()
            except Exception as e:
                st.error(f"Lỗi: {e}")
            
    # Tab 3: Quản lý Assets Hình ảnh (Cloudinary + Local Fallback)
    with admin_tab3:
        st.subheader("Quản lý Hình ảnh & Gán Tính cách / Ngành học")
        img_dir = get_abs_path("assets/images")
        
        # --- Load mappings từ Firebase ---
        from utils.firebase_client import (
            fb_get_mbti_image_mapping, fb_get_major_image_mapping,
            fb_save_mbti_image_mapping, fb_save_major_image_mapping
        )
        
        ALL_MBTI = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP","ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
        
        # Lấy danh sách ngành thực tế từ dữ liệu hệ thống (major_dict)
        ALL_MAJORS = sorted(list(major_dict.keys()))
        
        current_mbti_map = fb_get_mbti_image_mapping() or {}
        current_major_map = fb_get_major_image_mapping() or {}
        
        # --- Kiểm tra Cloudinary ---
        use_cloudinary = "cloudinary" in st.secrets
        cloud_images = []
        
        if use_cloudinary:
            from utils.cloudinary_client import upload_image, delete_image, list_images
            cloud_images = list_images()
        
        # Dict tra cứu nhanh: filename -> url, filename -> public_id
        cloud_url_map = {img["filename"]: img["url"] for img in cloud_images}
        cloud_pid_map = {img["filename"]: img["public_id"] for img in cloud_images}
        cloud_names = sorted(cloud_url_map.keys())
        
        # Fallback: ảnh cục bộ
        local_images = []
        if os.path.exists(img_dir):
            local_images = sorted([f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
        
        # Danh sách ảnh khả dụng (ưu tiên Cloud)
        available_names = cloud_names if use_cloudinary else local_images
        
        # === PHẦN 1: Upload ảnh mới ===
        st.markdown("#### Upload hình ảnh mới")
        if use_cloudinary:
            st.info("Ảnh sẽ được tải lên **Cloudinary CDN** và đồng bộ tới người dùng ngay lập tức.")
        else:
            st.warning("Chưa cấu hình Cloudinary. Ảnh sẽ lưu cục bộ vào `assets/images/`.")
        
        up_col1, up_col2 = st.columns([1, 1])
        with up_col1:
            uploaded_file = st.file_uploader("Chọn file ảnh từ máy tính", type=["png", "jpg", "jpeg"], key="upload_new")
        with up_col2:
            if uploaded_file:
                new_filename = st.text_input("Tên file lưu:", value=uploaded_file.name)
                if st.button("Tải lên & Lưu", type="primary"):
                    if use_cloudinary:
                        result = upload_image(uploaded_file.getvalue(), new_filename)
                        if result:
                            st.success(f"Đã tải lên Cloudinary: {new_filename}")
                            st.caption(f"URL: `{result['url']}`")
                            st.rerun()
                        else:
                            st.error("Upload lên Cloudinary thất bại!")
                    else:
                        save_path = os.path.join(img_dir, new_filename)
                        with open(save_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        st.success(f"Đã lưu cục bộ: {new_filename}")
                        st.rerun()
        
        st.divider()
        
        # === PHẦN 0: Danh sách ảnh hiện có ===
        used_urls = set(current_mbti_map.values()) | set(current_major_map.values())
        
        if use_cloudinary:
            # Refresh danh sách sau upload
            cloud_images = list_images()
            cloud_url_map = {img["filename"]: img["url"] for img in cloud_images}
            cloud_pid_map = {img["filename"]: img["public_id"] for img in cloud_images}
            cloud_names = sorted(cloud_url_map.keys())
            available_names = cloud_names
            
            with st.expander(f"Danh sách hình ảnh trên Cloud ({len(cloud_images)} ảnh)", expanded=False):
                for img in cloud_images:
                    fname = img["filename"]
                    url = img["url"]
                    pid = img["public_id"]
                    is_used = url in used_urls or fname in used_urls
                    status = "đang sử dụng" if is_used else "chưa gán"
                    
                    col_name, col_status, col_preview, col_action = st.columns([3, 2, 1, 1])
                    with col_name:
                        st.markdown(f"**{fname}**")
                    with col_status:
                        if is_used:
                            st.markdown(f"<span style='color:#16a34a; font-size:0.85rem;'>● {status}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<span style='color:#9ca3af; font-size:0.85rem;'>○ {status}</span>", unsafe_allow_html=True)
                    with col_preview:
                        if st.button("Xem", key=f"preview_{fname}"):
                            st.session_state[f"show_preview_{fname}"] = not st.session_state.get(f"show_preview_{fname}", False)
                    with col_action:
                        if is_used:
                            st.button("Xóa", key=f"del_{fname}", disabled=True, help="Ảnh đang được gán, không thể xóa.")
                        else:
                            if st.button("Xóa", key=f"del_{fname}", type="secondary"):
                                if delete_image(pid):
                                    st.success(f"Đã xóa khỏi Cloudinary: {fname}")
                                else:
                                    st.error("Xóa thất bại!")
                                st.rerun()
                    
                    if st.session_state.get(f"show_preview_{fname}", False):
                        st.image(url, width=200, caption=fname)
        else:
            # Fallback: hiển thị ảnh cục bộ
            with st.expander(f"Danh sách hình ảnh cục bộ ({len(local_images)} ảnh)", expanded=False):
                for img_name in local_images:
                    img_path = os.path.join(img_dir, img_name)
                    is_used = img_name in used_urls
                    status = "đang sử dụng" if is_used else "chưa gán"
                    
                    col_name, col_status, col_preview, col_action = st.columns([3, 2, 1, 1])
                    with col_name:
                        st.markdown(f"**{img_name}**")
                    with col_status:
                        if is_used:
                            st.markdown(f"<span style='color:#16a34a; font-size:0.85rem;'>● {status}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<span style='color:#9ca3af; font-size:0.85rem;'>○ {status}</span>", unsafe_allow_html=True)
                    with col_preview:
                        if st.button("Xem", key=f"preview_{img_name}"):
                            st.session_state[f"show_preview_{img_name}"] = not st.session_state.get(f"show_preview_{img_name}", False)
                    with col_action:
                        if is_used:
                            st.button("Xóa", key=f"del_{img_name}", disabled=True, help="Ảnh đang được gán, không thể xóa.")
                        else:
                            if st.button("Xóa", key=f"del_{img_name}", type="secondary"):
                                os.remove(img_path)
                                st.success(f"Đã xóa: {img_name}")
                                st.rerun()
                    
                    if st.session_state.get(f"show_preview_{img_name}", False):
                        st.image(img_path, width=200, caption=img_name)
        
        st.divider()
        
        # === PHẦN 2: Gán ảnh cho TỪNG loại MBTI ===
        st.markdown("#### Gán hình ảnh cho từng Tính cách MBTI (16 loại)")
        st.info("Chọn ảnh riêng biệt cho mỗi loại MBTI. Thay đổi sẽ cập nhật ngay tới giao diện Người dùng.")
        
        if len(available_names) == 0:
            st.warning("Chưa có ảnh nào. Vui lòng upload ảnh trước khi gán.")
        else:
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
                            cur_val = current_mbti_map.get(mbti_type, "")
                            cur_fname = cur_val
                            if use_cloudinary:
                                for cn, cu in cloud_url_map.items():
                                    if cu == cur_val or cn == cur_val:
                                        cur_fname = cn
                                        break
                            cur_idx = available_names.index(cur_fname) if cur_fname in available_names else 0
                            
                            st.markdown(f"**{mbti_type}**")
                            if use_cloudinary and cur_fname in cloud_url_map:
                                st.image(cloud_url_map[cur_fname], use_container_width=True)
                            elif not use_cloudinary and cur_fname in local_images:
                                st.image(os.path.join(img_dir, cur_fname), use_container_width=True)
                            
                            new_choice = st.selectbox(f"Ảnh {mbti_type}:", available_names, index=cur_idx, key=f"mbti_img_{mbti_type}", label_visibility="collapsed")
                            new_val = cloud_url_map.get(new_choice, new_choice) if use_cloudinary else new_choice
                            if current_mbti_map.get(mbti_type) != new_val:
                                current_mbti_map[mbti_type] = new_val
                                mbti_changed = True
            
            if mbti_changed:
                st.warning("Bạn đã thay đổi cấu hình ảnh MBTI.")
            if st.button("Lưu cấu hình Ảnh MBTI", type="primary", use_container_width=True):
                fb_save_mbti_image_mapping(current_mbti_map)
                st.success("Đã lưu! Giao diện Người dùng sẽ cập nhật ảnh MBTI mới.")
                st.cache_data.clear()
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
                            cur_val = current_major_map.get(major, "")
                            cur_fname = cur_val
                            if use_cloudinary:
                                for cn, cu in cloud_url_map.items():
                                    if cu == cur_val or cn == cur_val:
                                        cur_fname = cn
                                        break
                            cur_idx = available_names.index(cur_fname) if cur_fname in available_names else 0
                            
                            st.markdown(f"**{major}**")
                            new_choice = st.selectbox(f"Ảnh:", available_names, index=cur_idx, key=f"major_img_{major}", label_visibility="collapsed")
                            
                            if use_cloudinary and new_choice in cloud_url_map:
                                st.image(cloud_url_map[new_choice], use_container_width=True, caption=new_choice)
                            elif not use_cloudinary and new_choice in local_images:
                                st.image(os.path.join(img_dir, new_choice), use_container_width=True, caption=new_choice)
                            
                            new_val = cloud_url_map.get(new_choice, new_choice) if use_cloudinary else new_choice
                            if current_major_map.get(major) != new_val:
                                current_major_map[major] = new_val
                                major_changed = True
                
                if major_changed:
                    st.warning("Bạn đã thay đổi cấu hình ảnh Ngành học.")
                if st.button("Lưu cấu hình Ảnh Ngành học", type="primary", use_container_width=True):
                    fb_save_major_image_mapping(current_major_map)
                    st.success("Đã lưu lên Firebase! Ảnh minh họa ngành học sẽ cập nhật ngay.")
                    st.cache_data.clear()
                    st.rerun()

    # Tab 4: Thống Kê & XAI
    with admin_tab4:
        import pandas as pd
        from collections import Counter
        from utils.firebase_client import fb_get_usage_statistics, fb_save_usage_statistics
        
        st.subheader("Báo Cáo Hoạt Động & Phân Tích")
        
        # 1. Đọc dữ liệu thống kê từ Firebase
        stats_data = fb_get_usage_statistics()
        pred_count = stats_data.get("prediction_count", 0)
        logs = stats_data.get("logs", [])
        
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
                fb_save_usage_statistics({"prediction_count": 0, "logs": []})
                st.success("Đã xoá dữ liệu thống kê trên Firebase!")
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
