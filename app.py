import streamlit as st
import joblib

# ===== UI Components (Views) =====
from views import components
from views import sidebar
from views import tab1_survey, tab2_mbti, tab3_xai

# ==========================================
# 1. CẤU HÌNH TRANG & CSS
# ==========================================
st.set_page_config(
    page_title="Hệ thống Gợi ý Chuyên ngành",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo state gốc
if 'theme_mode' not in st.session_state:
    st.session_state['theme_mode'] = 'Light'
if 'user_mbti_result' not in st.session_state:
    st.session_state['user_mbti_result'] = None

components.inject_custom_css()

# ==========================================
# 2. TẢI MÔ HÌNH VÀ DATA
# ==========================================
@st.cache_resource(show_spinner="Đang khởi tạo không gian tri thức...")
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
    st.error("Lỗi hệ thống: Không tìm thấy dữ liệu mô hình. Vui lòng kiểm tra thư mục 'model/'.")
    st.stop()

# ==========================================
# 3. RENDER SIDEBAR
# ==========================================
model_choice, active_model = sidebar.render_sidebar(rf_model, dt_model, svm_model)

# ==========================================
# 4. RENDER CÁC TAB CHÍNH
# ==========================================
# Khai báo các tab
tab1, tab2, tab3 = st.tabs(["Khảo sát Phân tích", "Trắc nghiệm MBTI", "Giải thích Mô hình (XAI)"])

# Nội dung Tab 1
with tab1:
    components.render_hero(
        title="Hệ Thống Gợi Ý Chuyên Ngành Đại Học", 
        subtitle=f"Nhận diện năng lực cốt lõi dựa trên <b>{model_choice}</b> kết hợp không gian vector <b>KNN</b>"
    )
    tab1_survey.render_tab(active_model, model_choice, mbti_encoder, target_encoder, major_dict)

# Nội dung Tab 2
with tab2:
    components.render_hero(
        title="TRẮC NGHIỆM TÍNH CÁCH MBTI", 
        subtitle="Khám phá bản thân - Định vị năng lực cốt lõi"
    )
    tab2_mbti.render_tab()

# Nội dung Tab 3
with tab3:
    components.render_hero(
        title="GIẢI THÍCH HOẠT ĐỘNG CỦA MÔ HÌNH", 
        subtitle="Hiểu rõ cách thuật toán phân tích và đưa ra gợi ý chuyên ngành"
    )
    tab3_xai.render_tab(active_model, model_choice)