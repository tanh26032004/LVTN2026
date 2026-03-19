import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_hybrid_recommendations(user_scores, user_mbti_encoded, base_model, mbti_encoder, target_encoder, major_dict, dataset_path="data/student_data.csv", top_k=5, cb_weight=0.6, cf_weight=0.4):
    """
    Hệ thống Gợi ý Lai (Hybrid Recommendation System):
    Kết hợp Content-Based (Sử dụng các mô hình Machine Learning truyền thống như Random Forest, SVM, Decision Tree) 
    và Collaborative Filtering (User-Based KNN).
    
    Lưu ý học thuật: Tuyệt đối KHÔNG sử dụng Deep Learning/Neural Network theo khuyến nghị chống Overfitting với dữ liệu nhỏ.
    """
    
    # --- PHẦN 1: TÍNH ĐIỂM TỪ MACHINE LEARNING MODEL (CONTENT-BASED) ---
    feature_names = [
        'math_score', 'literature_score', 'english_score',
        'physics_score', 'chemistry_score', 'biology_score',
        'history_score', 'mbti_encoded'
    ]
    
    if len(user_scores) != 7:
        raise ValueError("user_scores phải là một danh sách gồm 7 giá trị điểm (math, literature, english, physics, chemistry, biology, history).")

    # Tạo DataFrame để truyền vào mô hình
    feature_input = pd.DataFrame([user_scores + [user_mbti_encoded]], columns=feature_names)
    feature_input_arr = feature_input.values  # Dùng cho thuật toán Cosine Similarity
    
    # Sử dụng base_model (có thể là Random Forest, Decision Tree, hoặc SVM) để dự đoán
    try:
        # Hầu hết các model (RF, DT) đều hỗ trợ predict_proba
        ml_probabilities = base_model.predict_proba(feature_input)[0]
    except AttributeError:
        # Fallback cho SVM nếu SVC không set probability=True lúc train
        # Tuy nhiên, trong Khóa luận, nên set probability=True cho SVM để dùng được hàm này
        ml_predictions = base_model.predict(feature_input)
        ml_probabilities = np.zeros(len(target_encoder.classes_))
        ml_probabilities[ml_predictions[0]] = 1.0
    
    cb_scores = {}
    for i, major_group in enumerate(target_encoder.classes_):
        cb_scores[major_group] = ml_probabilities[i]
        

    # --- PHẦN 2: TÍNH ĐIỂM TỪ COLLABORATIVE FILTERING (USER-BASED KNN) ---
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        sorted_cb = sorted(list(cb_scores.items()), key=lambda x: x[1], reverse=True)[:3]
        return sorted_cb, cb_scores, {}, None 
    
    if 'mbti_encoded' not in df.columns:
        df['mbti_encoded'] = mbti_encoder.transform(df['mbti_type'])
    
    features = [
        'math_score', 'literature_score', 'english_score',
        'physics_score', 'chemistry_score', 'biology_score',
        'history_score', 'mbti_encoded'
    ]
    
    score_features = features[:-1]
    df[score_features] = df[score_features].fillna(df[score_features].mean())
    
    db_matrix = df[features].values
    
    # Tính Cosine Similarity (Khoảng cách vector)
    similarities = cosine_similarity(feature_input_arr, db_matrix)[0]
    
    top_k_indices = similarities.argsort()[::-1][:top_k]
    
    cf_scores = {}
    for major_group in target_encoder.classes_:
         cf_scores[major_group] = 0.0
         
    total_similarity = np.sum(similarities[top_k_indices])
    
    if total_similarity > 0:
        for idx in top_k_indices:
            sim_score = similarities[idx]
            match_student = df.iloc[idx]
            major = match_student['major_group']
            rating = match_student['major_rating']
            
            # Tính trọng số đóng góp
            cf_contribution = (sim_score * (rating / 5.0)) / total_similarity
            
            if major in cf_scores:
                cf_scores[major] += cf_contribution

    # --- PHẦN 3: KẾT HỢP (HYBRID SCORING) ---
    hybrid_scores = {}
    for major_group in target_encoder.classes_:
        # Mặc định: 60% từ ML Model (Content-Based) + 40% từ KNN (Collaborative Filtering)
        final_score = (cb_weight * cb_scores.get(major_group, 0)) + (cf_weight * cf_scores.get(major_group, 0))
        hybrid_scores[major_group] = final_score
        
    sorted_hybrid = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_hybrid[:3], cb_scores, cf_scores, df.iloc[top_k_indices]