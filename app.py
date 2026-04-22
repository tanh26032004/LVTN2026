import streamlit as st
import joblib
from utils.firebase_client import seed_firebase_if_empty

# ==========================================
# 1. CẤU HÌNH TRANG & CSS
# ==========================================
st.set_page_config(
    page_title="Hệ thống Gợi ý Chuyên ngành",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Seed Firebase on cold start (chỉ cần chạy một lần)
try:
    seed_firebase_if_empty()
except:
    pass

# ===== UI Components (Views) =====
from views import components
from views import sidebar
from views import tab1_survey, tab2_mbti, tab3_xai

# ==========================================
# 1. CẤU HÌNH TRANG & CSS
# ==========================================
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
        preprocessor = joblib.load('model/preprocessor.joblib')
        target_encoder = joblib.load('model/target_encoder.joblib')
        major_dict = joblib.load('model/major_groups_dict.joblib')
        return rf_model, dt_model, svm_model, preprocessor, target_encoder, major_dict
    except Exception as e:
        return None, None, None, None, None, None

rf_model, dt_model, svm_model, preprocessor, target_encoder, major_dict = load_ml_models()

if rf_model is None or dt_model is None or svm_model is None:
    st.error("Lỗi hệ thống: Không tìm thấy dữ liệu mô hình. Vui lòng kiểm tra thư mục 'model/'.")
    st.stop()

# ==========================================
# 3. ROUTING (QUẢN TRỊ VIÊN)
# ==========================================
query_params = st.query_params
if query_params.get("admin") == "true":
    from views import admin_dashboard
    model_choice, active_model = admin_dashboard.render_admin_dashboard(rf_model, dt_model, svm_model, preprocessor, target_encoder, major_dict)
    st.stop() # Ngăn không render giao diện User bên dưới

# ==========================================
# 4. RENDER GIAO DIỆN NGƯỜI DÙNG BÌNH THƯỜNG
# ==========================================
model_choice = st.session_state.get('admin_model_choice', "Random Forest (Khuyên dùng)")
active_model = st.session_state.get('admin_active_model', rf_model)

# Khai báo các tab công khai
tab_options = ["Khảo sát Phân tích", "Trắc nghiệm MBTI"]

if 'active_panel' not in st.session_state or st.session_state['active_panel'] not in tab_options:
    st.session_state['active_panel'] = tab_options[0]

# --- 4.1. RENDER HERO BANNER (TRÊN CÙNG) ---
if st.session_state['active_panel'] == tab_options[0]:
    components.render_hero(
        title="Hệ Thống Gợi Ý Chuyên Ngành Đại Học", 
        subtitle="Khơi dậy tiềm năng, vững bước tương lai: Cùng AI khám phá ngành học dành riêng cho bạn!"
    )
elif st.session_state['active_panel'] == tab_options[1]:
    components.render_hero(
        title="TRẮC NGHIỆM TÍNH CÁCH MBTI", 
        subtitle="Khám phá bản thân - Định vị năng lực cốt lõi"
    )

# --- 4.2. RENDER MENU TABS (DƯỚI BANNER) ---
st.write("") # Khoảng đệm nhỏ

# Dùng st.pills (Streamlit >= 1.40) để tạo menu ngang mượt mà trên Mobile
selected_tab = st.pills(
    "Tabs", 
    options=tab_options, 
    default=st.session_state['active_panel'], 
    label_visibility="collapsed",
    selection_mode="single"
)

# Cập nhật trạng thái nếu người dùng đổi tab
if selected_tab and selected_tab != st.session_state['active_panel']:
    st.session_state['active_panel'] = selected_tab
    st.rerun()

st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)

# --- 4.3. RENDER NỘI DUNG TƯƠNG ỨNG MỖI TAB ---
if st.session_state['active_panel'] == "Khảo sát Phân tích":
    tab1_survey.render_tab(active_model, model_choice, preprocessor, target_encoder, major_dict)
elif st.session_state['active_panel'] == "Trắc nghiệm MBTI":
    tab2_mbti.render_tab()