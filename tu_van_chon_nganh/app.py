import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.hybrid_recommender import get_hybrid_recommendations
import os

# 1. CẤU HÌNH TRANG & CSS TÙY CHỈNH
st.set_page_config(
    page_title="Hệ thống Gợi ý Chuyên ngành",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    div[data-testid="stForm"], div[data-testid="stExpander"] {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stButton > button {
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .stProgress > div > div > div > div {
        border-radius: 10px;
    }
    button[data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
    div.row-widget.stRadio > div {
        flex-direction: column;
        gap: 0px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 2. TẢI CÁC MÔ HÌNH VÀ KHỞI TẠO STATE
@st.cache_resource(show_spinner="Đang tải các mô hình AI...")
def load_ml_models():
    try:
        rf_model = joblib.load('model/random_forest_model.joblib')
        dt_model = joblib.load('model/decision_tree_model.joblib')
        svm_model = joblib.load('model/svm_model.joblib')
        mbti_encoder = joblib.load('model/mbti_encoder.joblib')
        target_encoder = joblib.load('model/target_encoder.joblib')
        major_dict = joblib.load('model/major_groups_dict.joblib')
        return rf_model, dt_model, svm_model, mbti_encoder, target_encoder, major_dict
    except Exception as e:
        return None, None, None, None, None, None

rf_model, dt_model, svm_model, mbti_encoder, target_encoder, major_dict = load_ml_models()

if rf_model is None or dt_model is None or svm_model is None:
    st.error("Lỗi: Không tìm thấy đủ 3 file mô hình (.joblib) trong thư mục 'model/'. Vui lòng chạy lại file `scripts/train_model.py` để tạo đủ 3 mô hình.")
    st.stop()

if 'user_mbti_result' not in st.session_state:
    st.session_state['user_mbti_result'] = "INTJ"

# 3. THANH ĐIỀU HƯỚNG BÊN (SIDEBAR)
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <img src='https://cdn-icons-png.flaticon.com/512/3135/3135810.png' width='85' style='margin-bottom: 10px;'>
        <h2 style='margin: 0; font-size: 1.4rem; font-weight: 700; color: #1E88E5;'>Cấu hình AI</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Lựa chọn Thuật toán")
    model_choice = st.selectbox(
        "Mô hình Core (Content-Based):",
        ["Random Forest (Khuyên dùng)", "Decision Tree", "SVM (RBF Kernel)"]
    )
    
    if model_choice.startswith("Random Forest"):
        active_model = rf_model
    elif model_choice.startswith("Decision Tree"):
        active_model = dt_model
    else:
        active_model = svm_model

    st.markdown("""
    <div style='background-color: #f8f9fa; padding: 15px; border-radius: 12px; border-left: 4px solid #1E88E5; font-size: 0.95rem; line-height: 1.6; margin-top: 20px; margin-bottom: 20px;'>
        Hệ thống đánh giá đa chiều kết hợp:
        <ul style='margin-top: 8px; margin-bottom: 0; padding-left: 20px; color: #424242;'>
            <li>Năng lực học tập (Khối thi)</li>
            <li>Tính cách MBTI</li>
            <li>Collaborative Filtering (KNN)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #fff3e0; padding: 15px; border-radius: 12px; border-left: 4px solid #ff9800; font-size: 0.85rem; line-height: 1.5; margin-bottom: 20px;'>
        <b>⚠️ Tuyên bố khoa học:</b><br>
        Hệ thống đóng vai trò <i>tham khảo và hỗ trợ ra quyết định</i> với độ chính xác ~70-89%. AI này <b>không thay thế</b> hoàn toàn chuyên gia tư vấn hướng nghiệp.
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: gray; font-size: 0.85rem; line-height: 1.4;'>
            Sinh viên thực hiện: <b>Nguyễn Quốc Tánh</b><br>
            Mã số sinh viên: <b>224114</b><br>
            Lớp: <b>DH22TIN02</b><br>
            <span style='font-size: 0.8rem;'>Khóa luận tốt nghiệp © 2026</span>
        </div>
    """, unsafe_allow_html=True)

# 4. KHU VỰC NỘI DUNG CHÍNH (MAIN CONTENT)
st.title("HỆ THỐNG GỢI Ý CHUYÊN NGÀNH ĐẠI HỌC")
st.markdown(f"Hệ thống AI hiện đang chạy trên nền tảng: **{model_choice}** kết hợp **KNN**.")

tab1, tab2, tab3 = st.tabs(["Khảo sát & Nhận gợi ý", "Trắc nghiệm MBTI", "Phân tích XAI & Dữ liệu"])

# ================= TAB 1: NHẬP LIỆU & DỰ ĐOÁN =================
with tab1:
    col_input, col_result = st.columns([1.2, 1], gap="large")
    
    with col_input:
        st.subheader("1. Thông Hồ sơ")
        
        mbti_options = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
                        "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
        default_index = mbti_options.index(st.session_state['user_mbti_result']) if st.session_state['user_mbti_result'] in mbti_options else 3
        
        user_mbti = st.selectbox("Nhóm tính cách MBTI của bạn", options=mbti_options, index=default_index)
        st.session_state['user_mbti_result'] = user_mbti
        
        KHOI_SUBJECTS = {
            "Khối A  (Toán – Vật lý – Hóa học)":      ["Toán học", "Vật lý",    "Hóa học"],
            "Khối A1 (Toán – Vật lý – Tiếng Anh)":    ["Toán học", "Vật lý",    "Tiếng Anh"],
            "Khối B  (Toán – Hóa học – Sinh học)":     ["Toán học", "Hóa học",   "Sinh học"],
            "Khối C  (Ngữ văn – Lịch sử – Địa lí)":   ["Ngữ văn",  "Lịch sử",   "Địa lí"],
            "Khối D  (Toán – Ngữ văn – Tiếng Anh)":   ["Toán học", "Ngữ văn",   "Tiếng Anh"]
        }
        SUBJECT_KEY = {
            "Toán học":   "math",  "Vật lý":    "physics",
            "Hóa học":    "chem",  "Sinh học":  "bio",
            "Ngữ văn":    "lit",   "Lịch sử":   "hist",
            "Địa lí":     "geo",   "Tiếng Anh": "eng",
        }
        
        st.markdown("**Khối xét tuyển của bạn**")
        khoi_choice = st.radio("Chọn khối thi THPT Quốc gia", list(KHOI_SUBJECTS.keys()), label_visibility="collapsed")
        block_subjects = KHOI_SUBJECTS[khoi_choice]
        
        st.markdown(f"<div style='margin-top: 15px;'><b>Điểm 3 môn trong khối</b> *(thang 10)*</div>", unsafe_allow_html=True)
        
        with st.container(border=True):
            block_cols = st.columns(3)
            block_scores_input = {}
            for col, subj in zip(block_cols, block_subjects):
                with col:
                    block_scores_input[SUBJECT_KEY[subj]] = st.slider(subj, 0.0, 10.0, 7.0, 0.1)

        block_vals  = list(block_scores_input.values())
        block_avg   = round(sum(block_vals) / len(block_vals), 2)
        block_total = round(sum(block_vals), 2)

        s1, s2 = st.columns(2)
        s1.metric("Tổng điểm khối", f"{block_total:.2f} / 30")
        s2.metric("Điểm trung bình khối", f"{block_avg:.2f} / 10")

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("PHÂN TÍCH & NHẬN GỢI Ý", type="primary", use_container_width=True)

    with col_result:
        st.subheader("2. Kết quả Dự báo")
        
        if predict_btn:
            with st.spinner(f'AI đang phân tích bằng {model_choice}...'):
                try:
                    user_mbti_encoded = mbti_encoder.transform([user_mbti])[0]
                    
                    # Logic mô phỏng ép điểm các môn phụ
                    neutral_score = 5.0 
                    
                    # Khởi tạo ma trận 7 môn
                    final_scores = {
                        "math": neutral_score,
                        "lit": neutral_score,
                        "eng": neutral_score,
                        "physics": neutral_score,
                        "chem": neutral_score,
                        "bio": neutral_score,
                        "hist": neutral_score
                    }
                    
                    # Ghi đè điểm và xử lý môn Địa
                    for subj_name, score in block_scores_input.items():
                        if subj_name in final_scores:
                            final_scores[subj_name] = score
                        elif subj_name == "geo":
                            pass # Bỏ qua 'geo' khi truyền vào AI
                            
                    # Tạo list đúng 7 môn
                    user_scores = [
                        final_scores["math"], final_scores["lit"], final_scores["eng"],
                        final_scores["physics"], final_scores["chem"], final_scores["bio"],
                        final_scores["hist"]
                    ]
                    
                    top_3_hybrid, ml_scores, cf_scores, matching_students = get_hybrid_recommendations(
                        user_scores=user_scores,
                        user_mbti_encoded=user_mbti_encoded,
                        base_model=active_model, 
                        mbti_encoder=mbti_encoder,
                        target_encoder=target_encoder,
                        major_dict=major_dict
                    )
                    
                    st.session_state['matching_students'] = matching_students
                    st.success(f"Tích hợp AI Lai ({model_choice} + KNN) - Đã tìm thấy lộ trình phù hợp!")
                    
                    import random
                    top1_group = top_3_hybrid[0][0]
                    top1_prob = top_3_hybrid[0][1]*100
                    top1_specifics = ", ".join(random.sample(list(major_dict[top1_group]), min(3, len(major_dict[top1_group]))))
                    
                    st.markdown(f"""
                    <div style='padding: 20px; background-color: #f0f2f6; border-radius: 15px; border-left: 5px solid #ff4b4b;'>
                        <h3 style='margin:0; color: #ff4b4b;'>🏆 Top 1: KHỐI NGÀNH {top1_group.upper()}</h3>
                        <p style='margin:10px 0 0 0; font-size: 1.2rem;'>Độ phù hợp (Hybrid Score): <b>{top1_prob:.1f}%</b></p>
                        <p style='margin:5px 0 0 0; font-size: 0.95rem; color: #555;'>💡 Gợi ý chuyên ngành cụ thể: <i>{top1_specifics}...</i></p>
                    </div>
                    <br>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("#### Các khối ngành tiềm năng khác:")
                    for i, (group_name, prob) in enumerate(top_3_hybrid[1:]):
                        percentage = prob * 100
                        specifics = ", ".join(random.sample(list(major_dict[group_name]), min(3, len(major_dict[group_name]))))
                        
                        st.markdown(f"**#{i+2}. {group_name} — {percentage:.1f}%**")
                        st.markdown(f"<span style='font-size: 0.85rem; color: gray;'>↳ Gợi ý: {specifics}...</span>", unsafe_allow_html=True)
                        st.progress(float(prob))
                        
                except Exception as e:
                    st.error(f"Lỗi phân tích: {e}")
        else:
            st.info("Nhập điểm 3 môn bên trái và nhấn nút 'Phân tích' để xem các gợi ý chuyên ngành dành riêng cho bạn.")

# ================= TAB 2: TRẮC NGHIỆM MBTI =================
with tab2:
    st.subheader("Trắc nghiệm Tính cách Rút gọn (12 câu)")
    st.markdown("Nếu bạn chưa biết hoặc muốn xác nhận lại nhóm tính cách của mình, hãy trả lời nhanh các câu hỏi dưới đây.")
    
    with st.form("mbti_form"):
        col_q1, col_q2 = st.columns(2, gap="large")
        
        with col_q1:
            st.markdown("##### 1. Xu hướng Tự nhiên (E/I)")
            q1 = st.radio("1. Sau một tuần học tập và làm việc căng thẳng, bạn thường phục hồi năng lượng bằng cách:", 
                          ["E: Ra ngoài gặp gỡ, giao lưu với bạn bè hoặc tham gia các hoạt động tập thể.", 
                           "I: Dành thời gian một mình ở không gian yên tĩnh để đọc sách, xem phim hoặc nghỉ ngơi."])
            q2 = st.radio("2. Trong một cuộc họp nhóm hoặc thảo luận lớp, phong cách của bạn là:", 
                          ["E: Thoải mái nêu ý kiến, suy nghĩ thành tiếng và phát triển ý tưởng ngay trong lúc nói.", 
                           "I: Lắng nghe, xử lý thông tin cẩn thận trong đầu rồi mới phát biểu ý kiến chắt lọc nhất."])
            q3 = st.radio("3. Khi làm quen với một môi trường mới, bạn thường:", 
                          ["E: Dễ dàng bắt chuyện, làm quen nhanh chóng với nhiều người xung quanh.", 
                           "I: Giữ thái độ quan sát, cởi mở từ từ và chỉ thân thiết với một vài người nhất định."])
            
            st.markdown("##### 2. Cách thức Nhận thức (S/N)")
            q4 = st.radio("4. Khi tiếp nhận một thông tin hoặc kiến thức mới, bạn thích cách tiếp cận nào hơn?", 
                          ["S: Chú ý đến các dữ kiện, con số cụ thể, tính thực tế và khả năng áp dụng ngay.", 
                           "N: Hứng thú với các khái niệm trừu tượng, bức tranh tổng thể và những tiềm năng tương lai."])
            q5 = st.radio("5. Bạn miêu tả bản thân mình là người thiên về:", 
                          ["S: Thực tế, bám sát hiện tại và tin tưởng vào những kinh nghiệm đã được chứng minh.", 
                           "N: Giàu trí tưởng tượng, thường suy tư về những ý tưởng mới mẻ và khác biệt."])
            q6 = st.radio("6. Khi giải quyết một vấn đề khó, xu hướng của bạn là:", 
                          ["S: Làm theo quy trình từng bước, dựa vào các phương pháp đã có hiệu quả từ trước.", 
                           "N: Tìm kiếm những góc nhìn mới, thử nghiệm những cách làm đột phá chưa từng có."])

        with col_q2:
            st.markdown("##### 3. Tiêu chí Quyết định (T/F)")
            q7 = st.radio("7. Đứng trước một lựa chọn quan trọng, bạn thường dựa vào đâu để ra quyết định?", 
                          ["T: Phân tích logic, tính đúng/sai khách quan và cân nhắc lợi/hại một cách lý trí.", 
                           "F: Lắng nghe cảm xúc, nhạy cảm với hệ quả và quan tâm đến sự hòa hợp của những người liên quan."])
            q8 = st.radio("8. Khi nhận xét hoặc góp ý cho một người bạn làm sai, bạn có xu hướng:", 
                          ["T: Góp ý thẳng thắn, trực diện vào vấn đề để họ sửa đổi và tiến bộ.", 
                           "F: Góp ý khéo léo, nhẹ nhàng để bảo vệ cảm xúc và duy trì mối quan hệ tốt đẹp."])
            q9 = st.radio("9. Bạn đánh giá cao phẩm chất nào ở một người lãnh đạo hoặc quản lý hơn?", 
                          ["T: Sự công bằng, minh bạch, năng lực giải quyết vấn đề bằng lý trí sắc bén.", 
                           "F: Sự thấu cảm, tinh thần truyền cảm hứng và khả năng gắn kết tập thể."])
            
            st.markdown("##### 4. Nguyên tắc Sống (J/P)")
            q10 = st.radio("10. Phong cách làm việc và quản lý thời gian tiêu biểu của bạn là:", 
                           ["J: Lên kế hoạch chi tiết, có danh sách công việc rõ ràng và thích hoàn thành xong sớm mọi thứ.", 
                            "P: Linh hoạt, thích nghi với hoàn cảnh, thường làm việc năng suất nhất khi sát hạn chót."])
            q11 = st.radio("11. Đứng trước một thay đổi bất ngờ làm xáo trộn lịch trình, bạn cảm thấy:", 
                           ["J: Khá khó chịu, bối rối và muốn nhanh chóng thiết lập lại trật tự kiểm soát.", 
                            "P: Thoải mái đón nhận, xem đó là một trải nghiệm ngẫu hứng thú vị và dễ dàng tự điều chỉnh."])
            q12 = st.radio("12. Quan điểm của bạn về các quy tắc và quy định là:", 
                           ["J: Rất cần thiết để duy trì nền nếp, kỷ luật và định hướng mọi người đi đúng quỹ đạo.", 
                            "P: Có thể linh động nới lỏng, đôi khi quy tắc quá cứng nhắc sẽ kìm hãm sự sáng tạo."])
            
        submit_mbti = st.form_submit_button("TÍNH TOÁN KẾT QUẢ", type="primary")
        
        if submit_mbti:
            type_1 = "E" if sum([1 for q in [q1, q2, q3] if q.startswith("E")]) >= 2 else "I"
            type_2 = "S" if sum([1 for q in [q4, q5, q6] if q.startswith("S")]) >= 2 else "N"
            type_3 = "T" if sum([1 for q in [q7, q8, q9] if q.startswith("T")]) >= 2 else "F"
            type_4 = "J" if sum([1 for q in [q10, q11, q12] if q.startswith("J")]) >= 2 else "P"
            
            final_mbti = f"{type_1}{type_2}{type_3}{type_4}"
            st.session_state['user_mbti_result'] = final_mbti
            st.success(f"**Nhóm tính cách của bạn là: {final_mbti}**")
            st.info("Kết quả này đã được tự động điền vào Form Nhập liệu ở Tab 'Khảo sát & Nhận gợi ý'. Bạn có thể chuyển sang Tab đó để tiếp tục!")

# ================= TAB 3: EXPLAINABLE AI (XAI) & DATA =================
with tab3:
    st.subheader("Giải mã Trí tuệ Nhân tạo (Explainable AI - XAI)")
    st.info("Hệ thống **KHÔNG sử dụng Black-box AI**. Thay vào đó, hệ thống ứng dụng **White-box AI (AI có thể giải thích)** thông qua thuật toán máy học và KNN, cho phép truy xuất chính xác mức độ ảnh hưởng của từng yếu tố lên quyết định cuối cùng.")
    st.divider()
    
    xai_col1, xai_col2 = st.columns(2, gap="large")
    
    with xai_col1:
        st.markdown(f"#### 1. Mức độ ảnh hưởng ({model_choice})")
        
        if model_choice.startswith("SVM"):
            st.warning("Thuật toán **Support Vector Machine (SVM)** với RBF Kernel hoạt động dựa trên các siêu mặt phẳng phi tuyến tính trong không gian đa chiều. Do tính chất toán học phức tạp này, SVM được xem là một 'Hộp đen một phần' (Partial Black-box) và **không hỗ trợ trích xuất độ quan trọng của từng đặc trưng (Feature Importances)** trực quan như các thuật toán dạng Cây (Tree-based).")
            st.info("💡 Bạn có thể chọn lại mô hình **Random Forest** hoặc **Decision Tree** ở thanh Menu bên trái để xem biểu đồ XAI nhé!")
        else:
            st.markdown(f"Biểu đồ trích xuất từ **{model_choice}** chứng minh thuật toán đưa ra dự đoán dựa trên nền tảng logic rõ ràng:")
            
            ALL_FEATURE_LABELS = [
                'Toán', 'Ngữ văn', 'Tiếng Anh',
                'Vật lý', 'Hóa học',
                'Sinh học', 'Lịch sử', 'MBTI'
            ]
            importances = active_model.feature_importances_
            n = len(importances)
            feature_names = ALL_FEATURE_LABELS[:n] if n <= len(ALL_FEATURE_LABELS) else [f"Feature {i+1}" for i in range(n)]
            
            fi_df = pd.DataFrame({'Yếu tố': feature_names, 'Đóng góp (%)': importances * 100})
            fi_df = fi_df.sort_values(by='Đóng góp (%)', ascending=False)
            
            fig, ax = plt.subplots(figsize=(8, max(4, n * 0.65)))
            sns.barplot(x='Đóng góp (%)', y='Yếu tố', data=fi_df, palette='viridis', hue='Yếu tố', legend=False, ax=ax)
            
            ax.set_title("Trọng số ảnh hưởng cốt lõi", pad=15, fontweight='bold')
            ax.set_xlabel("Phần trăm đóng góp (%)")
            ax.set_ylabel("")
            
            sns.despine(left=True, bottom=False)
            st.pyplot(fig)

    with xai_col2:
        st.markdown("#### 2. Kiểm định Dữ liệu (Tránh Data Bias)")
        st.markdown("Hệ thống quét trực tiếp tệp `student_data.csv` để chứng minh tập dữ liệu khảo sát được phân bổ cân bằng, **không bị thiên lệch 90% vào ngành CNTT**:")
        
        try:
            df_data = pd.read_csv("data/student_data.csv")
            major_counts = df_data['major_group'].value_counts()
            
            fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
            ax_pie.pie(major_counts, labels=major_counts.index, autopct='%1.1f%%', 
                       startangle=140, colors=sns.color_palette('pastel', len(major_counts)))
            ax_pie.axis('equal') 
            st.pyplot(fig_pie)
            
            st.markdown("<div style='font-size: 0.85rem; color: gray; margin-top: 10px;'><i>*Tỉ lệ này được trích xuất trực tiếp từ Dataset khảo sát.</i></div>", unsafe_allow_html=True)
        except Exception as e:
            st.warning("📊 Biểu đồ phân bổ dữ liệu sẽ tự động hiển thị khi hệ thống đọc được file `data/student_data.csv`.")
            
    st.divider()
    
    st.markdown("#### 3. Thuật toán Collaborative Filtering (User-Based KNN)")
    st.markdown("Bên cạnh đó, AI dùng Cosine Similarity tìm ra những sinh viên đi trước có **hồ sơ y hệt bạn** để tham khảo chéo.")
    
    if 'matching_students' in st.session_state and st.session_state['matching_students'] is not None:
        st.markdown("<br><b>🤝 Top 5 sinh viên có độ tương đồng cao nhất:</b>", unsafe_allow_html=True)
        for i, (_, student) in enumerate(st.session_state['matching_students'].iterrows()):
            html_card = f"""
            <div style='background-color:#ffffff; padding:12px; margin-bottom:10px; border-radius:8px; border-left:4px solid #1E88E5; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <div style='display:flex; justify-content:space-between; margin-bottom:4px;'>
                    <span style='font-weight:bold; color:#1E88E5;'>{student.get('student_id', f'SV_0{i+1}')} (MBTI: {student['mbti_type']})</span>
                    <span style='color:#f39c12; font-weight:bold;'>⭐ {student['major_rating']:.1f}/5.0</span>
                </div>
                <div style='font-size:0.9rem; color:#444;'>
                    <b>Ngành học:</b> {student['specific_major']}<br>
                    <span style='color:#777; font-size:0.8rem;'>(Khối: {student['major_group']})</span>
                </div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
    else:
        st.info("👈 Vui lòng ấn **'Phân tích & Nhận gợi ý'** ở ngoài Tab 1 để gọi thuật toán quét tìm sinh viên.")