import os
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests

# Firebase Service Account Path (Legacy - using st.secrets now)
CREDENTIAL_PATH = "/Users/wocten/Documents/LVTN2026/.streamlit/lvtn2026-firebase-adminsdk-fbsvc-13fe218315.json"

@st.cache_resource
def get_db():
    if not firebase_admin._apps:
        try:
            # Ưu tiên lấy từ st.secrets (để an toàn khi push GitHub)
            if "firebase_service_account" in st.secrets:
                # Chuyển toml sang dict sạch cho SDK
                service_account_info = dict(st.secrets["firebase_service_account"])
                cred = credentials.Certificate(service_account_info)
            else:
                # Fallback dùng file local
                cred = credentials.Certificate(CREDENTIAL_PATH)
            
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Lỗi khởi tạo Firebase: {e}")
            raise e
    return firestore.client()

# Tên Collection lưu trữ cấu hình App
CONFIG_COLLECTION = "app_config"

def get_base_data_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def seed_firebase_if_empty():
    """Migrate local file contents to Firebase if Firebase documents don't exist yet."""
    db = get_db()
    
    # Migrate: mbti_questions
    doc_q = db.collection(CONFIG_COLLECTION).document("mbti_questions")
    if not doc_q.get().exists:
        try:
            local_path = os.path.join(get_base_data_path(), 'questions', 'mbti_questions.json')
            if os.path.exists(local_path):
                with open(local_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                doc_q.set({"questions": data})
                print("Seeded mbti_questions to Firebase.")
        except Exception as e:
            print(f"Failed to seed mbti_questions: {e}")

    # Migrate: mbti_image_mapping
    doc_mbti_img = db.collection(CONFIG_COLLECTION).document("mbti_image_mapping")
    if not doc_mbti_img.get().exists:
        try:
            local_path = os.path.join(get_base_data_path(), 'mbti_image_mapping.json')
            if os.path.exists(local_path):
                with open(local_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                doc_mbti_img.set(data)
                print("Seeded mbti_image_mapping to Firebase.")
        except Exception as e:
            print(f"Failed to seed mbti_image_mapping: {e}")

    # Migrate: major_image_mapping
    doc_major_img = db.collection(CONFIG_COLLECTION).document("major_image_mapping")
    if not doc_major_img.get().exists:
        try:
            local_path = os.path.join(get_base_data_path(), 'major_image_mapping.json')
            if os.path.exists(local_path):
                with open(local_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                doc_major_img.set(data)
                print("Seeded major_image_mapping to Firebase.")
        except Exception as e:
            print(f"Failed to seed major_image_mapping: {e}")

    # Migrate: mbti_comprehensive
    doc_comp = db.collection(CONFIG_COLLECTION).document("mbti_comprehensive")
    if not doc_comp.get().exists:
        try:
            local_path = os.path.join(get_base_data_path(), 'mbti_comprehensive.json')
            if os.path.exists(local_path):
                with open(local_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                doc_comp.set(data)
                print("Seeded mbti_comprehensive to Firebase.")
        except Exception as e:
            print(f"Failed to seed mbti_comprehensive: {e}")

    # Migrate: usage_statistics
    doc_stats = db.collection(CONFIG_COLLECTION).document("usage_statistics")
    if not doc_stats.get().exists:
        try:
            local_path = os.path.join(get_base_data_path(), 'usage_statistics.json')
            if os.path.exists(local_path):
                with open(local_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                doc_stats.set(data)
                print("Seeded usage_statistics to Firebase.")
            else:
                doc_stats.set({"prediction_count": 0, "logs": []})
        except Exception as e:
            print(f"Failed to seed usage_statistics: {e}")

# ==============================================================================
# QUERIES LẤY DỮ LIỆU
# ==============================================================================

def fb_get_mbti_questions():
    """Lấy danh sách câu hỏi MBTI."""
    try:
        db = get_db()
        doc = db.collection(CONFIG_COLLECTION).document("mbti_questions").get()
        if doc.exists:
            return doc.to_dict().get("questions", [])
    except Exception as e:
        print(f"Firebase fetch error (mbti_questions): {e}")
    return []

def fb_save_mbti_questions(questions_list):
    """Lưu danh sách câu hỏi MBTI."""
    db = get_db()
    db.collection(CONFIG_COLLECTION).document("mbti_questions").set({"questions": questions_list})

def fb_get_mbti_image_mapping():
    """Lấy cấu hình mapping ảnh MBTI."""
    try:
        db = get_db()
        doc = db.collection(CONFIG_COLLECTION).document("mbti_image_mapping").get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"Firebase fetch error (mbti_image_mapping): {e}")
    return {}

def fb_save_mbti_image_mapping(mapping_dict):
    """Lưu cấu hình mapping ảnh MBTI."""
    db = get_db()
    db.collection(CONFIG_COLLECTION).document("mbti_image_mapping").set(mapping_dict)

def fb_get_major_image_mapping():
    """Lấy cấu hình mapping ảnh Ngành."""
    try:
        db = get_db()
        doc = db.collection(CONFIG_COLLECTION).document("major_image_mapping").get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"Firebase fetch error (major_image_mapping): {e}")
    return {}

def fb_save_major_image_mapping(mapping_dict):
    """Lưu cấu hình mapping ảnh Ngành."""
    db = get_db()
    db.collection(CONFIG_COLLECTION).document("major_image_mapping").set(mapping_dict)

def fb_get_usage_statistics():
    """Lấy số liệu thống kê sử dụng."""
    try:
        db = get_db()
        doc = db.collection(CONFIG_COLLECTION).document("usage_statistics").get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"Firebase fetch error (usage_statistics): {e}")
    return {"prediction_count": 0, "logs": []}

def fb_save_usage_statistics(stats_dict):
    """Ghi đè số liệu thống kê (thường dùng khi reset)."""
    db = get_db()
    db.collection(CONFIG_COLLECTION).document("usage_statistics").set(stats_dict)

def fb_get_mbti_comprehensive():
    """Lấy dữ liệu mô tả MBTI chi tiết (markdown/long text)."""
    try:
        db = get_db()
        doc = db.collection(CONFIG_COLLECTION).document("mbti_comprehensive").get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"Firebase fetch error (mbti_comprehensive): {e}")
    return {}

def fb_save_mbti_comprehensive(comp_dict):
    """Lưu dữ liệu mô tả MBTI chi tiết."""
    db = get_db()
    db.collection(CONFIG_COLLECTION).document("mbti_comprehensive").set(comp_dict)

def fb_increment_prediction(log_entry):
    """Increment lượt đếm dự đoán và thêm log."""
    db = get_db()
    doc_ref = db.collection(CONFIG_COLLECTION).document("usage_statistics")
    # Lấy dữ liệu cũ để push vì logs là array, Firestore hỗ trợ `arrayUnion` 
    # nhưng để kiểm soát dễ dàng hơn chúng ta có thể giao dịch (Transaction)
    try:
        data = doc_ref.get()
        if data.exists:
            stats = data.to_dict()
        else:
            stats = {"prediction_count": 0, "logs": []}
            
        stats['prediction_count'] = stats.get('prediction_count', 0) + 1
        logs = stats.get('logs', [])
        logs.append(log_entry)
        stats['logs'] = logs
        
        doc_ref.set(stats)
    except Exception as e:
        print(f"Failed to increment usage stats: {e}")

def verify_admin_login(email, password):
    """
    Xác thực Email/Password qua Firebase Auth REST API.
    Yêu cầu cấu hình [firebase] api_key trong st.secrets.
    """
    try:
        api_key = st.secrets.get("firebase", {}).get("api_key")
        if not api_key:
            return False, "Thiếu Firebase Web API Key trong secrets.toml. Vui lòng kiểm tra lại cấu hình [firebase]."
        
        auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        response = requests.post(auth_url, json=payload)
        res_data = response.json()
        
        if response.status_code == 200:
            return True, "Đăng nhập thành công!"
        else:
            # Lấy thông báo lỗi từ Firebase
            error_msg = res_data.get("error", {}).get("message", "Lỗi xác thực không xác định.")
            # Chuyển đổi một số thông báo lỗi phổ biến sang tiếng Việt
            if "EMAIL_NOT_FOUND" in error_msg or "INVALID_PASSWORD" in error_msg:
                error_msg = "Email hoặc mật khẩu không chính xác."
            elif "USER_DISABLED" in error_msg:
                error_msg = "Tài khoản này đã bị vô hiệu hóa."
            return False, error_msg
            
    except Exception as e:
        return False, f"Lỗi kết nối Firebase Auth: {str(e)}"
