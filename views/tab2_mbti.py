import streamlit as st
import random
from mbti_assets import MBTI_DETAILS, MBTI_QUESTIONS, MBTI_COMPREHENSIVE

def render_tab():
    if 'mbti_step' not in st.session_state:
        st.session_state['mbti_step'] = 0

    # Các hàm điều hướng nội bộ của Tab 2
    def set_step_1():
        st.session_state['mbti_step'] = 1
        st.session_state['mbti_sub_step'] = 1
        st.session_state['mbti_answers'] = {}
        st.session_state['mbti_form_error'] = ""
        try:
            q_e_i = random.sample(MBTI_QUESTIONS[0:15], 3)
            q_s_n = random.sample(MBTI_QUESTIONS[15:30], 3)
            q_t_f = random.sample(MBTI_QUESTIONS[30:45], 3)
            q_j_p = random.sample(MBTI_QUESTIONS[45:60], 3)
            st.session_state['selected_mbti_questions'] = q_e_i + q_s_n + q_t_f + q_j_p
        except Exception:
            st.session_state['selected_mbti_questions'] = MBTI_QUESTIONS

    def set_step_0():
        st.session_state['mbti_step'] = 0

    selected_qs = st.session_state.get('selected_mbti_questions', MBTI_QUESTIONS)

    def process_mbti_form():
        s = st.session_state
        answers = s.get('mbti_answers', {})
        q_per_group = len(selected_qs) // 4
        
        def count_score(start_idx, end_idx, target_char):
            keys = [selected_qs[i]["id"] for i in range(start_idx, end_idx)]
            return sum(1 for k in keys if answers.get(k) and answers[k].startswith(target_char))
            
        type_1 = "E" if count_score(0, q_per_group, "E") >= (q_per_group / 2.0) else "I"
        type_2 = "S" if count_score(q_per_group, q_per_group*2, "S") >= (q_per_group / 2.0) else "N"
        type_3 = "T" if count_score(q_per_group*2, q_per_group*3, "T") >= (q_per_group / 2.0) else "F"
        type_4 = "J" if count_score(q_per_group*3, len(selected_qs), "J") >= (q_per_group / 2.0) else "P"
        
        s['user_mbti_result'] = f"{type_1}{type_2}{type_3}{type_4}"
        s['mbti_step'] = 2

    # ==========================================
    # GIAO DIỆN BƯỚC 0: TỔNG QUAN
    # ==========================================
    if st.session_state['mbti_step'] == 0:
        
        # Nút bấm hiện ngay phía dưới banner chung của Tab từ app.py
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1.2, 1])
        with col_btn2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("Bắt đầu khảo sát", on_click=set_step_1, use_container_width=True, type="primary")

        st.divider()

        st.markdown("<h3 style='text-align:center; color: #0ea5e9; font-weight: 800; margin-bottom: 25px;'>Các Nhóm Tính Cách MBTI Điển Hình</h3>", unsafe_allow_html=True)
        
        # CSS CAO CẤP: Thiết kế Card & Expander theo phong cách 16Personalities
        st.markdown("""
        <style>
        /* Tùy chỉnh tổng thể Expander */
        div[data-testid="stExpander"] details {
            border-radius: 16px !important;
            overflow: hidden !important;
            border: 1px solid rgba(0,0,0,0.08) !important;
            box-shadow: 0 4px 10px -2px rgba(0,0,0,0.05) !important;
            margin-bottom: 12px !important;
            background-color: #ffffff !important;
        }
        
        /* Tiêu đề Expander */
        div[data-testid="stExpander"] details summary {
            padding: 15px 20px;
            transition: all 0.3s ease;
        }
        div[data-testid="stExpander"] details summary p {
            font-size: 1.15rem !important;
            font-weight: 800 !important;
            color: #1e293b !important;
            letter-spacing: -0.3px !important;
        }

        /* Gradient & Border trái cho 4 nhóm (Tím, Xanh lá, Xanh lam, Vàng) */
        div[data-testid="stExpander"]:nth-of-type(1) details summary { background: linear-gradient(90deg, #f5f3ff 0%, #ffffff 100%) !important; border-left: 6px solid #a855f7 !important; }
        div[data-testid="stExpander"]:nth-of-type(2) details summary { background: linear-gradient(90deg, #f0fdf4 0%, #ffffff 100%) !important; border-left: 6px solid #22c55e !important; }
        div[data-testid="stExpander"]:nth-of-type(3) details summary { background: linear-gradient(90deg, #f0f9ff 0%, #ffffff 100%) !important; border-left: 6px solid #3b82f6 !important; }
        div[data-testid="stExpander"]:nth-of-type(4) details summary { background: linear-gradient(90deg, #fff7ed 0%, #ffffff 100%) !important; border-left: 6px solid #f97316 !important; }

        /* Giao diện Thẻ Tính Cách (Card) */
        .mbti-premium-card {
            padding: 24px 20px; 
            border-radius: 16px; 
            height: 100%;
            min-height: 240px; 
            margin-bottom: 15px; 
            border: 1px solid rgba(0,0,0,0.05); 
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            display: flex;
            flex-direction: column;
        }
        .mbti-premium-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.1);
        }
        
        .mbti-title {
            font-size: 1.8rem;
            font-weight: 900;
            margin: 0 0 5px 0;
            letter-spacing: -0.5px;
        }
        
        .mbti-subtitle {
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 12px;
            display: block;
        }
        
        .mbti-desc {
            font-size: 0.9rem;
            color: #475569;
            line-height: 1.55;
            margin: 0;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 4; /* Giới hạn 4 dòng */
            -webkit-box-orient: vertical;
        }

        /* 📱 Responsive Mobile */
        @media screen and (max-width: 768px) {
            .mbti-premium-card {
                min-height: auto !important; 
                padding: 18px 16px !important;
                margin-bottom: 10px !important; 
            }
            .mbti-title { font-size: 1.5rem !important; }
            .mbti-subtitle { font-size: 0.95rem !important; margin-bottom: 8px !important; }
            .mbti-desc { font-size: 0.85rem !important; -webkit-line-clamp: 3 !important; }
            div[data-testid="stExpander"] details summary p { font-size: 1rem !important; }
        }
        </style>
        """, unsafe_allow_html=True)

        # Phối màu chuẩn cho 4 nhóm: [Nền, Chữ, Viền Hover]
        style_groups = [
            {"bg": "#faf5ff", "text": "#7e22ce", "border": "#d8b4fe"}, # Analysts (Tím)
            {"bg": "#f0fdf4", "text": "#15803d", "border": "#86efac"}, # Diplomats (Xanh lá)
            {"bg": "#f0f9ff", "text": "#0369a1", "border": "#7dd3fc"}, # Sentinels (Xanh lam)
            {"bg": "#fff7ed", "text": "#c2410c", "border": "#fdba74"}  # Explorers (Cam)
        ]
        
        mbti_keys = list(MBTI_DETAILS.keys())
        mbti_groups = [
            "Nhóm Nhà Phân Tích (Analysts - Tư duy chiến lược & Độc lập)",
            "Nhóm Nhà Ngoại Giao (Diplomats - Sâu sắc & Thấu cảm)",
            "Nhóm Người Lính Gác (Sentinels - Kỷ luật & Thực tế)",
            "Nhóm Nhà Khám Phá (Explorers - Năng động & Linh hoạt)"
        ]

        for row in range(4):
            # Tạo hiệu ứng Hover thay đổi màu viền card bằng CSS inline kết hợp class
            style = style_groups[row]
            st.markdown(f"""
            <style>
                .card-group-{row}:hover {{ border-color: {style['border']} !important; }}
            </style>
            """, unsafe_allow_html=True)

            with st.expander(mbti_groups[row], expanded=True):
                cols = st.columns(4)
                for col in range(4):
                    idx = row * 4 + col
                    if idx < len(mbti_keys):
                        key = mbti_keys[idx]
                        info = MBTI_DETAILS[key]
                        
                        with cols[col]:
                            st.markdown(f"""
                                <div class="mbti-premium-card card-group-{row}" style="background-color: {style['bg']};">
                                    <h4 class="mbti-title" style="color: {style['text']};">{key}</h4>
                                    <span class="mbti-subtitle" style="color: {style['text']};">{info['title']}</span>
                                    <p class="mbti-desc">
                                        {info['description']}
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)

        # Tự động thu gọn Expander trên Mobile
        st.components.v1.html("""
            <script>
            setTimeout(function() {
                if (window.parent.innerWidth <= 768) {
                    const expanders = window.parent.document.querySelectorAll('div[data-testid="stExpander"] details');
                    for(let i=0; i<expanders.length; i++) expanders[i].removeAttribute('open');
                }
            }, 100);
            </script>
        """, height=0)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("Tìm hiểu chuyên sâu về Hệ thống MBTI", expanded=False):
            # FIX LỖI MARKDOWN: Đưa toàn bộ HTML sát lề trái để không bị biến thành Code Block
            st.markdown("""
<div style="padding: 5px 10px;">
<h4 style="color: #0ea5e9; margin-top: 0; font-weight: 800; font-size: 1.15rem;">1. Lịch sử và Nguồn gốc</h4>
<p style="color: #334155; font-size: 0.95rem; line-height: 1.6;"><b>MBTI (Myers-Briggs Type Indicator)</b> được phát triển bởi Katharine Cook Briggs và con gái bà, Isabel Briggs Myers, dựa trên các lý thuyết phân tích tâm lý học nền tảng của bác sĩ tâm thần học lỗi lạc người Thụy Sĩ <b>Carl Jung</b>. Kể từ khi ra mắt, MBTI đã trở thành một trong những công cụ đánh giá tính cách và định hướng nghề nghiệp phổ biến nhất trên toàn cầu.</p>

<h4 style="color: #0ea5e9; margin-top: 25px; font-weight: 800; font-size: 1.15rem;">2. Bốn Khía Cạnh Cốt Lõi (4 Dichotomies)</h4>
<p style="color: #334155; font-size: 0.95rem; line-height: 1.6;">Hệ thống phân loại 16 tính cách được xây dựng dựa trên sự kết hợp của 4 cặp phạm trù đối lập nhau. Mỗi cá nhân sẽ thiên về một cực trong mỗi cặp:</p>

<div style="background-color: #faf5ff; padding: 18px; border-radius: 12px; border-left: 5px solid #a855f7; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<b style="color: #7e22ce; font-size: 1.05rem;">① Nguồn Năng lượng: Hướng ngoại (E) vs Hướng nội (I)</b><br>
<span style="color: #475569; font-size: 0.9rem; line-height: 1.5;">Trả lời cho câu hỏi: <i>Bạn lấy năng lượng từ đâu?</i></span><br>
<ul style="margin-top: 8px; margin-bottom: 0; padding-left: 20px; color: #334155; font-size: 0.9rem; line-height: 1.6;">
<li><b>Extraversion (E - Hướng ngoại):</b> Lấy năng lượng từ thế giới bên ngoài. Thích giao tiếp, hoạt động sôi nổi, làm việc nhóm và thể hiện bản thân qua lời nói.</li>
<li><b>Introversion (I - Hướng nội):</b> Nạp lại năng lượng khi ở một mình. Thích sự yên tĩnh, có xu hướng suy nghĩ sâu sắc trước khi phát biểu và chuộng không gian làm việc độc lập.</li>
</ul>
</div>

<div style="background-color: #f0fdf4; padding: 18px; border-radius: 12px; border-left: 5px solid #22c55e; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<b style="color: #15803d; font-size: 1.05rem;">② Cách Tiếp nhận Thông tin: Cảm giác (S) vs Trực giác (N)</b><br>
<span style="color: #475569; font-size: 0.9rem; line-height: 1.5;">Trả lời cho câu hỏi: <i>Bạn chú ý đến loại thông tin nào nhất?</i></span><br>
<ul style="margin-top: 8px; margin-bottom: 0; padding-left: 20px; color: #334155; font-size: 0.9rem; line-height: 1.6;">
<li><b>Sensing (S - Cảm giác):</b> Tập trung vào hiện tại và thực tế. Tin tưởng vào những gì có thể nhận biết qua 5 giác quan, chuộng dữ liệu cụ thể, chi tiết và kinh nghiệm thực tiễn.</li>
<li><b>Intuition (N - Trực giác):</b> Tập trung vào tương lai và bức tranh tổng thể. Chú trọng đến các mô hình, quy luật, ý nghĩa ẩn giấu và những khả năng sáng tạo mới mẻ.</li>
</ul>
</div>

<div style="background-color: #f0f9ff; padding: 18px; border-radius: 12px; border-left: 5px solid #3b82f6; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<b style="color: #0369a1; font-size: 1.05rem;">③ Cách Đưa ra Quyết định: Lý trí (T) vs Cảm xúc (F)</b><br>
<span style="color: #475569; font-size: 0.9rem; line-height: 1.5;">Trả lời cho câu hỏi: <i>Bạn dựa vào đâu để ra quyết định?</i></span><br>
<ul style="margin-top: 8px; margin-bottom: 0; padding-left: 20px; color: #334155; font-size: 0.9rem; line-height: 1.6;">
<li><b>Thinking (T - Lý trí):</b> Đưa ra quyết định dựa trên logic, sự nhất quán và phân tích khách quan. Coi trọng sự thật, tính hiệu quả và nguyên tắc công bằng hơn là cảm giác.</li>
<li><b>Feeling (F - Cảm xúc):</b> Đưa ra quyết định dựa trên hệ giá trị cá nhân, sự đồng cảm và hoàn cảnh của những người liên quan. Mong muốn duy trì sự hòa hợp và nhân đạo.</li>
</ul>
</div>

<div style="background-color: #fff7ed; padding: 18px; border-radius: 12px; border-left: 5px solid #f97316; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<b style="color: #c2410c; font-size: 1.05rem;">④ Lối sống & Tổ chức: Nguyên tắc (J) vs Linh hoạt (P)</b><br>
<span style="color: #475569; font-size: 0.9rem; line-height: 1.5;">Trả lời cho câu hỏi: <i>Bạn thích tổ chức thế giới bên ngoài của mình như thế nào?</i></span><br>
<ul style="margin-top: 8px; margin-bottom: 0; padding-left: 20px; color: #334155; font-size: 0.9rem; line-height: 1.6;">
<li><b>Judging (J - Nguyên tắc/Đánh giá):</b> Thích cuộc sống có kế hoạch, trật tự, rõ ràng và được kiểm soát. Đề cao tính kỷ luật, đúng hạn và thích đưa ra quyết định dứt điểm.</li>
<li><b>Perceiving (P - Linh hoạt/Nhận thức):</b> Thích lối sống tự phát, cởi mở và linh hoạt. Thích giữ các lựa chọn mở, dễ dàng thích nghi với sự thay đổi và làm việc tùy hứng.</li>
</ul>
</div>

<h4 style="color: #0ea5e9; margin-top: 25px; font-weight: 800; font-size: 1.15rem;">3. Tầm Quan Trọng Trong Hướng Nghiệp</h4>
<p style="color: #334155; font-size: 0.95rem; line-height: 1.6;">Không có nhóm tính cách nào là ưu việt hay yếu kém tuyệt đối. Hệ thống MBTI là tấm bản đồ sinh trắc học tâm lý giúp bạn:</p>
<ul style="color: #334155; font-size: 0.95rem; line-height: 1.6; padding-left: 20px;">
<li><b>Nhận diện cốt lõi:</b> Thấu hiểu điểm mạnh thiên bẩm và những điểm mù cần khắc phục.</li>
<li><b>Tối ưu môi trường:</b> Lựa chọn được văn hóa doanh nghiệp phù hợp (ví dụ: người <b>I</b> chuộng sự tập trung độc lập, người <b>E</b> cần không gian mở tương tác).</li>
<li><b>Định vị nghề nghiệp:</b> Khớp nối bản chất tự nhiên của mình với yêu cầu đặc thù của các khối ngành đào tạo bậc Đại học, từ đó đạt được sự thỏa mãn và thành công cao nhất trong sự nghiệp.</li>
</ul>
</div>
""", unsafe_allow_html=True)
    
    # ==========================================
    # GIAO DIỆN BƯỚC 1: LÀM TRẮC NGHIỆM
    # ==========================================
    elif st.session_state['mbti_step'] == 1:
        st.markdown("""
        <style>
        div[data-testid="stRadio"] {
            background-color: #ffffff; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; margin-bottom: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: all 0.2s ease-in-out;
        }
        div[data-testid="stRadio"]:hover { border-color: #0ea5e9; box-shadow: 0 6px 12px -2px rgba(0,0,0,0.05); }
        div[data-testid="stRadio"] > label { font-weight: 700; color: #0f172a; font-size: 1.1rem; margin-bottom: 12px; }
        .stProgress > div > div > div > div { background-color: #0ea5e9; border-radius: 10px;}
        </style>
        """, unsafe_allow_html=True)
        
        sub_step = st.session_state.get('mbti_sub_step', 1)
        part_titles = [
            "Khía cạnh Tương tác (E/I)",
            "Khía cạnh Nhận thức (S/N)",
            "Khía cạnh Quyết định (T/F)",
            "Khía cạnh Tổ chức (J/P)"
        ]
        
        st.subheader(f"Bộ câu hỏi định chuẩn MBTI - Phần {sub_step}/4")
        st.progress(sub_step / 4.0)
        st.markdown(f"**{sub_step}. {part_titles[sub_step-1]}**")
        
        if st.session_state.get('mbti_form_error'):
            st.error(st.session_state['mbti_form_error'])
            
        q_per_group = len(selected_qs) // 4
        start_idx = (sub_step - 1) * q_per_group
        end_idx = sub_step * q_per_group
        subset = selected_qs[start_idx:end_idx]

        def handle_next_btn():
            s = st.session_state
            # Validate
            unanswered = [q['id'] for q in subset if s.get(q['id']) is None]
            if unanswered:
                s['mbti_form_error'] = f"Bạn còn {len(unanswered)} câu hỏi chưa trả lời ở phần này!"
            else:
                s['mbti_form_error'] = ""
                if 'mbti_answers' not in s:
                    s['mbti_answers'] = {}
                for q in subset:
                    s['mbti_answers'][q['id']] = s[q['id']]
                
                if sub_step < 4:
                    s['mbti_sub_step'] = sub_step + 1
                else:
                    process_mbti_form()

        def handle_back_btn():
            s = st.session_state
            s['mbti_form_error'] = ""
            if 'mbti_answers' not in s:
                s['mbti_answers'] = {}
            for q in subset:
                if s.get(q['id']) is not None:
                    s['mbti_answers'][q['id']] = s[q['id']]
            if sub_step > 1:
                s['mbti_sub_step'] = sub_step - 1
            else:
                set_step_0()

        with st.form(f"mbti_form_part_{sub_step}", border=False):
            answers = st.session_state.get('mbti_answers', {})
            for q in subset:
                saved_ans = answers.get(q['id'])
                idx = None
                if saved_ans in q['options']:
                    idx = q['options'].index(saved_ans)
                st.radio(q['text'], q['options'], key=q['id'], index=idx)
            
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                back_label = "Quay lại Từ đầu" if sub_step == 1 else "← Trở về trang trước"
                st.form_submit_button(back_label, on_click=handle_back_btn, use_container_width=True)
            with c2:
                next_label = "Tiếp theo →" if sub_step < 4 else "Hoàn thành và Xem Kết quả"
                st.form_submit_button(next_label, on_click=handle_next_btn, use_container_width=True, type="primary")

    # ==========================================
    # GIAO DIỆN BƯỚC 2: KẾT QUẢ & PHÂN TÍCH
    # ==========================================
    elif st.session_state['mbti_step'] == 2:
        mbti_res = st.session_state['user_mbti_result']
        mbti_info = MBTI_DETAILS.get(mbti_res, {"title": mbti_res, "description": "Thông tin chi tiết đang được cập nhật...", "image": "assets/images/mbti_analyst.png"})
        
        # Phần Header hiển thị Kết quả MBTI dạng Card hiện đại
        st.markdown(f"""
        <div style='text-align:center; padding: 40px 20px; border-radius: 20px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); margin-bottom: 30px; border: 1px solid rgba(0,0,0,0.05);'>
            <h2 style='color:#0ea5e9; margin-bottom:5px; font-size: 2.8rem; font-weight: 900; letter-spacing: -1px;'>{mbti_res}</h2>
            <p style='font-size:1.3rem; font-weight:700; color: #475569; margin:0;'>{mbti_info['title']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # KHU VỰC CHIA 2 CỘT
        m_col1, m_col2 = st.columns([1, 1.5], gap="large")
        
        with m_col1:
            try:
                st.image(mbti_info['image'], caption=f"Nhóm tính cách {mbti_res}", use_container_width=True)
            except:
                st.info(f"Đang hiển thị nhóm {mbti_res}...")

        with m_col2:
            st.markdown("<h3 style='color: #1e293b; font-weight: 800; margin-top: 0;'>Đặc điểm nổi bật</h3>", unsafe_allow_html=True)
            st.write(mbti_info.get('description', ''))
            
            if 'strengths' in mbti_info:
                st.markdown("<br>", unsafe_allow_html=True)
                scol1, scol2 = st.columns(2)
                
                with scol1:
                    st.markdown("<h4 style='color: #0ea5e9; font-weight: 700; font-size: 1.15rem;'>Điểm mạnh</h4>", unsafe_allow_html=True)
                    for s in mbti_info['strengths']:
                        st.markdown(f"<span style='color: #0ea5e9; margin-right: 5px;'>•</span> {s}", unsafe_allow_html=True)
                        
                with scol2:
                    st.markdown("<h4 style='color: #f43f5e; font-weight: 700; font-size: 1.15rem;'>Điểm yếu</h4>", unsafe_allow_html=True)
                    for w in mbti_info['weaknesses']:
                        st.markdown(f"<span style='color: #f43f5e; margin-right: 5px;'>•</span> {w}", unsafe_allow_html=True)

                st.markdown("<br><h4 style='color: #3b82f6; font-weight: 700; font-size: 1.15rem;'>Gợi ý nghề nghiệp</h4>", unsafe_allow_html=True)
                careers = mbti_info.get('careers', [])
                tags_html = "".join([f"<span style='display: inline-block; background-color: #f0f9ff; color: #0284c7; padding: 6px 14px; border-radius: 20px; margin: 0 8px 8px 0; font-size: 0.9rem; font-weight: 600; border: 1px solid #bae6fd;'>{c}</span>" for c in careers])
                st.markdown(tags_html, unsafe_allow_html=True)
                
        st.divider()

        # Phần hiển thị chi tiết toàn diện (Tràn toàn bộ chiều rộng)
        if mbti_res in MBTI_COMPREHENSIVE:
            st.markdown("<h3 style='color: #1e293b; font-weight: 800;'>Phân tích chuyên sâu</h3>", unsafe_allow_html=True)
            st.markdown(MBTI_COMPREHENSIVE[mbti_res])
            st.divider()
        
        # Khối CTA (Call To Action) điều hướng
        st.markdown(f"""
        <div style='background-color: #f0f9ff; border-left: 5px solid #0ea5e9; padding: 25px; border-radius: 16px; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);'>
            <h3 style='color: #0284c7; margin-top: 0; margin-bottom: 10px; font-weight: 800;'>🚀 Bước tiếp theo: Dự đoán Chuyên ngành</h3>
            <p style='color: #1e293b; margin-bottom: 10px;'>Hệ thống đã ghi nhận tính cách <b>{mbti_res}</b> của bạn.</p>
            <p style='color: #475569; font-size: 0.95rem; margin-bottom: 0; line-height: 1.5;'>Vui lòng chuyển sang tab <b>Khảo sát Phân tích</b> để nhập điểm số học tập. AI sẽ kết hợp phân tích đa chiều và đưa ra gợi ý ngành học chuẩn xác nhất.</p>
        </div>
        """, unsafe_allow_html=True)
        
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            st.button("Làm lại trắc nghiệm", type="secondary", on_click=set_step_0, use_container_width=True)
        with b_col2:
            if st.button("Sang trang Dự đoán Ngành", type="primary", use_container_width=True):
                st.components.v1.html("""
                    <script>
                    const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');
                    if (tabs.length > 0) {
                        tabs[0].click();
                    }
                    </script>
                """, height=0)