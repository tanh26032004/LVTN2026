import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scripts.train_model import engineer_features

def get_hybrid_recommendations(user_scores, user_mbti, base_pipeline, preprocessor, target_encoder, major_dict, dataset_path="data/student_data.csv", top_k=5, cb_weight=0.6, cf_weight=0.4):
    """
    Hệ thống Gợi ý Lai:
    Kết hợp Content-Based (ML Models) và Collaborative Filtering (KNN).
    Đã được tối ưu bằng Data Engineering, StandardScaler và OneHotEncoding.
    """
    
    if len(user_scores) != 7:
        raise ValueError("user_scores phải là một danh sách gồm 7 giá trị điểm (math, lit, eng, phys, chem, bio, hist).")

    # Tạo DataFrame chứa RAW features
    raw_columns = ['math_score', 'literature_score', 'english_score',
                   'physics_score', 'chemistry_score', 'biology_score', 'history_score']
    
    df_input = pd.DataFrame([user_scores], columns=raw_columns)
    df_input['mbti_type'] = user_mbti
    
    # 1. Tự động nội suy các features phái sinh (Feature Engineering)
    df_input = engineer_features(df_input)
    
    # Thứ tự cột phải khớp với lúc train (numerical + categorical)
    numerical_features = [
        'math_score', 'literature_score', 'english_score',
        'physics_score', 'chemistry_score', 'biology_score',
        'history_score', 'avg_score', 'natural_science_score', 'social_science_score'
    ]
    categorical_features = ['mbti_type']
    
    # Bảm bảo chuẩn format feature input
    feature_input = df_input[numerical_features + categorical_features]
    
    # --- PHẦN 1: CONTENT-BASED (MACHINE LEARNING MODEL) ---
    # base_pipeline đã bao gồm preprocessor và classifier, ta cứ truyền thẳng
    try:
        # Hầu hết các model hỗ trợ predict_proba (RF, DT, SVM đã set prob=True)
        ml_probabilities = base_pipeline.predict_proba(feature_input)[0]
    except AttributeError:
        ml_predictions = base_pipeline.predict(feature_input)
        ml_probabilities = np.zeros(len(target_encoder.classes_))
        ml_probabilities[ml_predictions[0]] = 1.0
    
    cb_scores = {}
    for i, major_group in enumerate(target_encoder.classes_):
        cb_scores[major_group] = ml_probabilities[i]

    # --- PHẦN 2: COLLABORATIVE FILTERING (USER-BASED KNN) ---
    try:
        df_db = pd.read_csv(dataset_path)
    except FileNotFoundError:
        sorted_cb = sorted(cb_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        return sorted_cb, cb_scores, {}, None 
        
    # Tính toán features phái sinh cho Database
    df_db = engineer_features(df_db)
    
    # Trích xuất đúng cột
    db_features = df_db[numerical_features + categorical_features]
    
    # Áp dụng StandardScaler & OneHotEncoder độc lập cho Cosine Similarity 
    # Bắt buộc phải dùng để các features (0-10 vs 0-1) không đè lẫn nhau 
    input_transformed = preprocessor.transform(feature_input)
    db_transformed = preprocessor.transform(db_features)
    
    # Cosine Similarity (Vector N chiều)
    similarities = cosine_similarity(input_transformed, db_transformed)[0]
    
    top_k_indices = similarities.argsort()[::-1][:top_k]
    
    cf_scores = {major_group: 0.0 for major_group in target_encoder.classes_}
    total_similarity = np.sum(similarities[top_k_indices])
    
    if total_similarity > 0:
        for idx in top_k_indices:
            sim_score = similarities[idx]
            match_student = df_db.iloc[idx]
            major = match_student['major_group']
            rating = match_student['major_rating']
            
            # Trọng số phụ thuộc Rating và khoảng cách vector
            cf_contribution = (sim_score * (rating / 5.0)) / total_similarity
            cf_scores[major] = cf_scores.get(major, 0.0) + cf_contribution

    # --- PHẦN 3: HYBRID SCORING ---
    hybrid_scores = {}
    for major_group in target_encoder.classes_:
        # Mặc định: 60% từ ML Model + 40% từ KNN
        final_score = (cb_weight * cb_scores.get(major_group, 0)) + (cf_weight * cf_scores[major_group])
        hybrid_scores[major_group] = final_score
        
    sorted_hybrid = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_hybrid[:3], cb_scores, cf_scores, df_db.iloc[top_k_indices]