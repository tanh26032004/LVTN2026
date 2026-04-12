import streamlit as st

def render_sidebar(rf_model, dt_model, svm_model):
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; font-size: 1.4rem; font-weight: 800; color: #0ea5e9; margin-bottom: 25px;'>Bảng Điều Khiển</h2>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 0.9rem; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; margin-top: 10px; opacity: 0.8;'>Thiết lập Mô hình</p>", unsafe_allow_html=True)
        
        model_choice = st.selectbox(
            "Lựa chọn Thuật toán Core:",
            ["Random Forest (Khuyên dùng)", "Decision Tree", "SVM (RBF Kernel)"],
            label_visibility="collapsed"
        )
        
        if model_choice.startswith("Random Forest"): active_model = rf_model
        elif model_choice.startswith("Decision Tree"): active_model = dt_model
        else: active_model = svm_model

        # Tối ưu CSS: Dùng rgba() thay vì mã HEX cứng để đảm bảo viền đẹp trên cả Light & Dark mode
        st.markdown("""
            <div style='padding: 18px 16px; border-radius: 16px; border: 1px solid rgba(150, 150, 150, 0.3); margin-top: 15px; margin-bottom: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);'>
                <p style='margin-top: 0; margin-bottom: 12px; font-weight: 800; font-size: 0.95rem; color: #0ea5e9;'>Phương pháp Cốt lõi</p>
                <p style='font-size: 0.85rem; margin-bottom: 8px; opacity: 0.9;'>Hệ thống đánh giá đa chiều tích hợp:</p>
                <ul style='font-size: 0.85rem; padding-left: 20px; margin-bottom: 0; line-height: 1.6; opacity: 0.9;'>
                    <li><b>Năng lực học tập</b> (Hệ số điểm khối thi)</li>
                    <li><b>Nhóm tính cách</b> tâm lý học (MBTI)</li>
                    <li><b>Lọc cộng tác</b> (Collaborative Filtering - KNN)</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Biến "Mẹo giao diện" thành một hộp thông báo (Alert Box) đẹp mắt
        st.markdown("""
            <div style='background-color: rgba(14, 165, 233, 0.1); padding: 12px 15px; border-radius: 12px; border-left: 4px solid #0ea5e9; font-size: 0.85rem; line-height: 1.5; margin-bottom: 15px;'>
                <b>🌙 Mẹo Giao Diện:</b> Để chuyển đổi <b>Dark Mode</b>, nhấn vào biểu tượng <b>⋮</b> <i>(bánh răng)</i> ở góc trên bên phải ➜ <b>Settings</b> ➜ <b>Theme</b>.
            </div>
        """, unsafe_allow_html=True)
        
        # Footer thông tin đề tài (Đã đặt opacity để làm dịu mắt)
        st.markdown("""
            <div style='text-align: center; font-size: 0.85rem; line-height: 1.6; padding-top: 15px; border-top: 1px solid rgba(150,150,150,0.2); opacity: 0.7;'>
                <b style='letter-spacing: 0.5px;'>THÔNG TIN ĐỀ TÀI</b><br>
                Sinh viên: Nguyễn Quốc Tánh<br>
                MSSV: 224114 | Lớp: DH22TIN02<br>
                Khóa luận tốt nghiệp © 2026
            </div>
        """, unsafe_allow_html=True)
        
    return model_choice, active_model