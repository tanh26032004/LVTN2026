import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
import joblib

def train_and_save_heuristic_model(data_path="data/student_data.csv", model_dir="model", test_size=0.2, random_state=42):
    """
    Tiền xử lý và huấn luyện phân loại chuyên ngành với 8 features (7 môn học + 1 MBTI).
    Huấn luyện song song 3 mô hình (Random Forest, Decision Tree, SVM) để phục vụ báo cáo học thuật.
    """
    print(f"Bắt đầu đọc dữ liệu từ '{data_path}'...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{data_path}'. Vui lòng kiểm tra lại đường dẫn.")
        return
        
    mbti_encoder = LabelEncoder()
    target_encoder = LabelEncoder()
    
    # Mã hóa nhãn (Label Encoding)
    df['mbti_encoded'] = mbti_encoder.fit_transform(df['mbti_type'])
    df['target_encoded'] = target_encoder.fit_transform(df['major_group'])
    
    # Lưu từ điển ánh xạ từ nhóm ngành -> danh sách các ngành cụ thể
    major_dict = df.groupby('major_group')['specific_major'].unique().apply(list).to_dict()
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(major_dict, os.path.join(model_dir, 'major_groups_dict.joblib'))

    # ----- CHỌN ĐẶC TRƯNG (FEATURES) -----
    numerical_score_columns = [
        'math_score', 'literature_score', 'english_score',
        'physics_score', 'chemistry_score', 'biology_score',
        'history_score'
    ]

    features = [c for c in numerical_score_columns if c in df.columns]
    
    if 'mbti_encoded' not in df.columns:
        df['mbti_encoded'] = mbti_encoder.fit_transform(df['mbti_type'])
    
    features.append('mbti_encoded')

    if len(features) < 8:
        print(f"Cảnh báo: Số lượng features lấy được là {len(features)} (kỳ vọng là 8).")

    # Xử lý missing data
    score_features = [f for f in features if f != 'mbti_encoded'] 
    df[score_features] = df[score_features].fillna(df[score_features].mean())

    X = df[features]
    y = df['target_encoded']
    
    # Chia tập train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    
    print("\n" + "="*50)
    print("🚀 ĐANG HUẤN LUYỆN VÀ SO SÁNH 3 MÔ HÌNH MACHINE LEARNING")
    print("="*50)

    # 1. Random Forest (MÔ HÌNH CHÍNH) - TỐI ƯU SIÊU THAM SỐ
    print("⏳ Đang tính toán Tối ưu hóa siêu tham số (GridSearchCV) cho Random Forest...")
    rf_base = RandomForestClassifier(class_weight='balanced', random_state=random_state)
    
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [20, 30, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    
    grid_search = GridSearchCV(estimator=rf_base, param_grid=param_grid, cv=5, n_jobs=-1, scoring='f1_macro')
    grid_search.fit(X_train, y_train)
    
    rf_model = grid_search.best_estimator_
    print(f"🌟 [TỐI ƯU LƯỚI ĐA DIỆN] Tham số cấu hình tốt nhất: {grid_search.best_params_}")

    # 2. Decision Tree (MÔ HÌNH SO SÁNH) - Dễ giải thích bằng cây quyết định
    dt_model = DecisionTreeClassifier(
        max_depth=20, class_weight='balanced', random_state=random_state
    )
    dt_model.fit(X_train, y_train)

    # 3. Support Vector Machine - SVM (MÔ HÌNH SO SÁNH)
    # Lưu ý: Bắt buộc probability=True để có thể dùng predict_proba() trong file hybrid_recommender.py
    svm_model = SVC(
        kernel='rbf', probability=True, class_weight='balanced', random_state=random_state
    )
    svm_model.fit(X_train, y_train)

    # ----- ĐÁNH GIÁ VÀ XUẤT BẢNG SO SÁNH -----
    models = {
        "Random Forest (Main)": rf_model,
        "Decision Tree       ": dt_model,
        "SVM (RBF Kernel)    ": svm_model
    }

    print(f"\n{'MÔ HÌNH':<25} | {'ACCURACY':<10} | {'PRECISION':<10} | {'RECALL':<10} | {'F1-SCORE':<10}")
    print("-" * 75)

    for name, model in models.items():
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        # Tính điểm trung bình (macro) cho các chỉ số
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='macro', zero_division=0)
        
        print(f"{name:<25} | {acc*100:>8.2f}% | {precision*100:>8.2f}% | {recall*100:>8.2f}% | {f1*100:>8.2f}%")

    print("-" * 75)

    # In Báo cáo chi tiết và Feature Importances riêng cho Random Forest
    print("\n[BÁO CÁO ĐÁNH GIÁ CHI TIẾT CỦA MÔ HÌNH RANDOM FOREST]:")
    rf_pred = rf_model.predict(X_test)
    try:
        # In classification report hiển thị rõ f1-score cho từng chuyên ngành
        cls_report = classification_report(y_test, rf_pred, target_names=target_encoder.classes_)
        print(cls_report)
    except Exception as e:
        print(classification_report(y_test, rf_pred))

    print("\n[XAI] MỨC ĐỘ QUAN TRỌNG CỦA CÁC ĐẶC TRƯNG (Theo Random Forest):")
    fi_df = pd.DataFrame({
        'Feature': features, 
        'Importance (%)': rf_model.feature_importances_ * 100
    }).sort_values(by='Importance (%)', ascending=False)
    
    for _, row in fi_df.iterrows():
        print(f" - {row['Feature']:<20}: {row['Importance (%)']:.2f}%")

    # Xuất tất cả các models ra file để sử dụng trên Web App
    joblib.dump(rf_model, os.path.join(model_dir, "random_forest_model.joblib"))
    joblib.dump(dt_model, os.path.join(model_dir, "decision_tree_model.joblib"))
    joblib.dump(svm_model, os.path.join(model_dir, "svm_model.joblib"))
    
    joblib.dump(mbti_encoder, os.path.join(model_dir, "mbti_encoder.joblib"))
    joblib.dump(target_encoder, os.path.join(model_dir, "target_encoder.joblib"))
    
    print(f"\n✅ Đã xuất thành công các file mô hình (.joblib) vào thư mục '{model_dir}'.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Huấn luyện và lưu mô hình gợi ý chuyên ngành.")
    parser.add_argument("--data_path", type=str, default="data/student_data.csv", help="Đường dẫn tới file dữ liệu CSV.")
    parser.add_argument("--model_dir", type=str, default="model", help="Thư mục lưu mô hình joblib.")
    parser.add_argument("--test_size", type=float, default=0.2, help="Tỷ lệ test size khi split dữ liệu.")
    parser.add_argument("--random_state", type=int, default=42, help="Random state cho train_test_split và mô hình.")

    args = parser.parse_args()

    train_and_save_heuristic_model(
        data_path=args.data_path,
        model_dir=args.model_dir,
        test_size=args.test_size,
        random_state=args.random_state
    )