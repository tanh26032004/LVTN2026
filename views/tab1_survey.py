import streamlit as st
import random
import os
import json
from scripts.hybrid_recommender import get_hybrid_recommendations
from data.major_db import get_major_code
from assets.mbti_assets import get_major_image
from views import chatbot_widget

def record_prediction_usage(user_school="", user_mbti="", khoi_thi="", top1_major="", scores=None):
    """Ghi nhận chi tiết mỗi lần dự đoán thành công vào Firebase."""
    if scores is None: scores = []
    try:
        from datetime import datetime
        from utils.firebase_client import fb_increment_prediction
        
        # Ghi chi tiết lượt sử dụng
        log_entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "truong_thpt": user_school,
            "mbti": user_mbti,
            "khoi_thi": khoi_thi,
            "diem_1": scores[0] if len(scores) > 0 else 0,
            "diem_2": scores[1] if len(scores) > 1 else 0,
            "diem_3": scores[2] if len(scores) > 2 else 0,
            "top1_major": top1_major
        }
        fb_increment_prediction(log_entry)
        
    except Exception:
        pass # Ignore minor network errors in UI


def render_tab(active_model, active_model_name, preprocessor, target_encoder, major_dict):
    col_input, col_result = st.columns([1.2, 1], gap="large")
    
    with col_input:
        st.markdown("<h3 style='font-weight: 800; margin-top: 0; margin-bottom: 20px;'>Thông tin của bạn</h3>", unsafe_allow_html=True)
        
        try:
            from utils.firebase_client import fb_get_high_schools
            schools_list = fb_get_high_schools()
            if schools_list:
                school_names = [f"{s.get('name', '')} - {s.get('province', '')}".strip(" -") for s in schools_list]
                user_school = st.selectbox("Trường THPT bạn đang học", options=school_names, index=None, placeholder="-- Gõ tên trường để tìm kiếm --")
            else:
                user_school = st.text_input("Trường THPT bạn đang học", placeholder="Nhập tên trường THPT...")
        except Exception:
            user_school = st.text_input("Trường THPT bạn đang học", placeholder="Nhập tên trường THPT...")
        
        mbti_options = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
                        "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
        current_mbti = st.session_state.get('user_mbti_result', None)
        default_index = mbti_options.index(current_mbti) if current_mbti in mbti_options else None
        
        user_mbti = st.selectbox("Nhóm tính cách MBTI", options=mbti_options, index=default_index, placeholder="-- Chọn Nhóm tính cách MBTI --")
        if user_mbti:
            st.session_state['user_mbti_result'] = user_mbti
        
        KHOI_SUBJECTS = {
            "Khối A (Toán – Vật lý – Hóa học)": ["Toán học", "Vật lý", "Hóa học"],
            "Khối A1 (Toán – Vật lý – Tiếng Anh)": ["Toán học", "Vật lý", "Tiếng Anh"],
            "Khối B (Toán – Hóa học – Sinh học)": ["Toán học", "Hóa học", "Sinh học"],
            "Khối C (Ngữ văn – Lịch sử – Địa lí)": ["Ngữ văn", "Lịch sử", "Địa lí"],
            "Khối D (Toán – Ngữ văn – Tiếng Anh)": ["Toán học", "Ngữ văn", "Tiếng Anh"]
        }
        SUBJECT_KEY = {
            "Toán học": "math", "Vật lý": "physics", "Hóa học": "chem", "Sinh học": "bio",
            "Ngữ văn": "lit", "Lịch sử": "hist", "Địa lí": "geo", "Tiếng Anh": "eng",
        }
        
        khoi_choice = st.selectbox("Khối thi / Tổ hợp xét tuyển", list(KHOI_SUBJECTS.keys()), index=None, placeholder="-- Chọn Khối thi --")
        
        block_scores_input = {}
        if khoi_choice:
            block_subjects = KHOI_SUBJECTS[khoi_choice]
            
            st.markdown("<div style='font-size: 0.95rem; font-weight: 600; margin-bottom: 10px; margin-top: 20px;'>Điểm trung bình môn (Học bạ / Thi thử)</div>", unsafe_allow_html=True)
            
            # Khung nhập điểm gọn gàng
            block_cols = st.columns(3)
            for col, subj in zip(block_cols, block_subjects):
                with col:
                    block_scores_input[SUBJECT_KEY[subj]] = st.number_input(subj, min_value=0.0, max_value=10.0, value=7.0, step=0.1)

            block_vals  = list(block_scores_input.values())
            if len(block_vals) > 0:
                block_avg   = round(sum(block_vals) / len(block_vals), 2)
                block_total = round(sum(block_vals), 2)

                # Custom UI thay cho st.metric để hiển thị Tổng điểm đẹp hơn
                st.markdown(f"""
                <div style="display: flex; gap: 15px; margin-top: 15px; margin-bottom: 25px;">
                    <div style="flex: 1; background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); padding: 15px; border-radius: 12px; border: 1px solid #cbd5e1; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                        <p style="margin: 0; font-size: 0.8rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Tổng điểm khối</p>
                        <h2 style="margin: 5px 0 0 0; color: #0f172a; font-size: 1.8rem; font-weight: 800;">{block_total:.2f}<span style="font-size: 1rem; color: #94a3b8; font-weight: 600;">/30</span></h2>
                    </div>
                    <div style="flex: 1; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 15px; border-radius: 12px; border: 1px solid #bae6fd; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                        <p style="margin: 0; font-size: 0.8rem; color: #0ea5e9; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Điểm trung bình</p>
                        <h2 style="margin: 5px 0 0 0; color: #082f49; font-size: 1.8rem; font-weight: 800;">{block_avg:.2f}<span style="font-size: 1rem; color: #7dd3fc; font-weight: 600;">/10</span></h2>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        predict_btn = st.button("Khám phá Ngành phù hợp", type="primary", use_container_width=True)

    with col_result:
        st.markdown("<h3 style='font-weight: 800; margin-top: 0; margin-bottom: 10px;'>Ngành học dự đoán</h3>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: #fffbeb; color: #92400e; padding: 12px 16px; border-radius: 12px; border: 1px solid #fde68a; margin-bottom: 20px; font-size: 0.9rem; line-height: 1.5;'><b>Lưu ý:</b> Hệ thống dự đoán hiện đang đạt độ chính xác ước tính khoảng <b>80-85%</b>. Các kết quả gợi ý dưới đây có giá trị <b>tham khảo và định hướng</b>, học sinh nên kết hợp chặt chẽ với đam mê cá nhân và điều kiện gia đình trước khi đưa ra quyết định cuối cùng.</div>", unsafe_allow_html=True)
        
        if predict_btn and (not user_school or not user_mbti or not khoi_choice):
             st.warning("⚠️ Vui lòng hoàn thành thao tác **Nhập Trường THPT**, **Chọn Nhóm tính cách MBTI** và **Khối thi THPT** ở bảng bên trái trước khi phân tích!")
        elif predict_btn:
            with st.spinner('AI đang tính toán không gian vector và trích xuất đặc trưng...'):
                try:
                    neutral_score = 5.0 
                    final_scores = { "math": neutral_score, "lit": neutral_score, "eng": neutral_score, "physics": neutral_score, "chem": neutral_score, "bio": neutral_score, "hist": neutral_score }
                    
                    for subj_name, score in block_scores_input.items():
                        if subj_name in final_scores: final_scores[subj_name] = score
                            
                    user_scores = [final_scores["math"], final_scores["lit"], final_scores["eng"], final_scores["physics"], final_scores["chem"], final_scores["bio"], final_scores["hist"]]
                    
                    top_3_hybrid, ml_scores, cf_scores, matching_students = get_hybrid_recommendations(
                        user_scores=user_scores, user_mbti=user_mbti, base_pipeline=active_model, 
                        preprocessor=preprocessor, target_encoder=target_encoder, major_dict=major_dict
                    )
                    
                    st.session_state['matching_students'] = matching_students
                    top1_group = top_3_hybrid[0][0]
                    top1_prob = top_3_hybrid[0][1] * 100
                    
                    record_prediction_usage(user_school=user_school, user_mbti=user_mbti, khoi_thi=khoi_choice, top1_major=top1_group, scores=block_vals)
                    
                    # Lấy danh sách toàn bộ các ngành thuộc TOP 1
                    top1_majors_list = list(major_dict.get(top1_group, []))
                    
                    # ============ KẾT QUẢ TOP 1 - CARD CHÍNH ============
                    st.markdown(f"""
<div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 1px solid #7dd3fc; padding: 18px 28px; border-radius: 20px; box-shadow: 0 8px 30px -5px rgba(14, 165, 233, 0.15); margin-bottom: 20px; text-align: center;'>
<p style='color: #0284c7; font-weight: 900; margin: 0; font-size: 1.3rem; text-transform: uppercase; letter-spacing: 3px;'>Đề xuất Phù hợp nhất</p>
</div>
""", unsafe_allow_html=True)
                    top1_col_img, top1_col_info = st.columns([1, 2.5])
                    with top1_col_img:
                        try:
                            major_img_path = get_major_image(top1_group)
                            st.image(major_img_path, use_container_width=True)
                        except:
                            pass
                    with top1_col_info:
                        st.markdown(f"""
<h2 style='color: #0369a1; margin: 0 0 10px 0; font-weight: 900; font-size: 1.8rem; letter-spacing: -0.5px;'>{top1_group}</h2>
<div style='display: flex; align-items: center; gap: 12px; margin-bottom: 8px;'>
<div style='flex-grow: 1; background-color: #e0f2fe; height: 12px; border-radius: 6px; overflow: hidden;'>
<div style='width: {top1_prob:.1f}%; background: linear-gradient(90deg, #38bdf8, #0ea5e9); height: 100%; border-radius: 6px;'></div>
</div>
<span style='font-weight: 900; color: #0284c7; font-size: 1.2rem; min-width: 60px; text-align:right;'>{top1_prob:.1f}%</span>
</div>
<p style='color: #64748b; font-size: 0.9rem; margin: 0;'>Mức độ phù hợp dựa trên phân tích tổ hợp MBTI, khối thi và điểm số của bạn.</p>
""", unsafe_allow_html=True)
                    
                    # --- DANH SÁCH CHI TIẾT NGÀNH TOP 1 ---
                    with st.expander(f"Bấm để xem mã ngành thuộc **{top1_group}**", expanded=False):
                        st.markdown("<p style='color:#475569; font-size:0.9rem; margin-bottom:12px;'>Danh sách các chuyên ngành đào tạo đại học:</p>", unsafe_allow_html=True)
                        for major in top1_majors_list:
                            code = get_major_code(major)
                            st.markdown(f"<div style='margin-bottom: 8px; padding-left: 5px;'><code style='color:#0ea5e9; background:#f1f5f9; padding:4px 8px; border-radius:6px; font-weight:600; font-size:0.85rem; margin-right:8px;'>{code}</code> <span style='font-weight:600; color:#334155; font-size: 0.95rem;'>{major}</span></div>", unsafe_allow_html=True)

                    st.markdown("<h4 style='color: #334155; font-size: 1.1rem; font-weight: 700; margin-top: 25px; margin-bottom: 15px;'>Các nhóm ngành tiềm năng khác</h4>", unsafe_allow_html=True)
                    
                    # ============ KẾT QUẢ TOP 2 & 3 ============
                    for i, (group_name, prob) in enumerate(top_3_hybrid[1:]):
                        percentage = prob * 100
                        group_majors_list = list(major_dict.get(group_name, []))
                        
                        with st.container(border=True):
                            sub_col_img, sub_col_info = st.columns([1, 3])
                            with sub_col_img:
                                try:
                                    sub_img_path = get_major_image(group_name)
                                    st.image(sub_img_path, use_container_width=True)
                                except:
                                    pass
                            with sub_col_info:
                                st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
<b style="color: #0f172a; font-size: 1.05rem;">{i+2}. {group_name}</b>
<span style="color: #64748b; font-weight: 600; font-size: 0.95rem;">{percentage:.1f}%</span>
</div>
""", unsafe_allow_html=True)
                                st.progress(float(prob))
                            
                            with st.expander(f"Xem mã ngành thuộc nhóm này", expanded=False):
                                for major in group_majors_list:
                                    code = get_major_code(major)
                                    st.markdown(f"<div style='margin-bottom: 8px; padding-left: 5px;'><code style='color:#0ea5e9; background:#f1f5f9; padding:4px 8px; border-radius:6px; font-weight:600; font-size:0.85rem; margin-right:8px;'>{code}</code> <span style='font-weight:600; color:#334155; font-size: 0.95rem;'>{major}</span></div>", unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Lỗi trong quá trình suy luận: {e}")
        else:
            # QUAN TRỌNG: Căn lề trái tuyệt đối để xử lý lỗi HTML trắng nhách
            st.markdown("""
<div style='background-color: #f8fafc; padding: 50px 20px; border-radius: 20px; border: 2px dashed #cbd5e1; text-align: center; margin-top: 10px;'>
    <h1 style='font-size: 3rem; margin: 0; margin-bottom: 10px;'></h1>
    <h4 style='color: #475569; font-weight: 700; margin-bottom: 10px;'>Đang chờ thông tin từ bạn</h4>
    <p style='color: #64748b; font-size: 0.95rem; max-width: 85%; margin: 0 auto; line-height: 1.6;'>
        Vui lòng chọn <b>Nhóm tính cách MBTI</b> và <b>Khối thi</b> ở bên trái, sau đó nhấn nút <b style="color: #0ea5e9;">Khám phá Ngành phù hợp</b> để hệ thống bắt đầu gợi ý nhé.
    </p>
</div>
""", unsafe_allow_html=True)

    # Bật Chatbot nổi (Floating Chat Widget)
    chatbot_widget.render_floating_chat()