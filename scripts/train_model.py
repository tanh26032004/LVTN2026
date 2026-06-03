import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
import joblib

def engineer_features(df):
    """ Tối ưu hóa đặc trưng bằng Data Engineering """
    df = df.copy()
    
    score_cols = ['math_score', 'literature_score', 'english_score',
                  'physics_score', 'chemistry_score', 'biology_score', 'history_score']
    
    for col in score_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())
            
    # Tính các biến tổng quát giúp Mô Hình dễ đưa ra luật
    df['avg_score'] = df[score_cols].mean(axis=1)
    df['natural_science_score'] = df[['math_score', 'physics_score', 'chemistry_score', 'biology_score']].mean(axis=1)
    df['social_science_score'] = df[['literature_score', 'history_score', 'english_score']].mean(axis=1)
    
    return df

def train_and_save_heuristic_model(data_path="data/student_data.csv", model_dir="model", test_size=0.2, random_state=42):
    """
    Huấn luyện AI với Pipeline: StandardScaler + OneHotEncoder -> ML Model.
    """
    print(f"Bắt đầu đọc dữ liệu từ '{data_path}'...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{data_path}'. Vui lòng kiểm tra lại đường dẫn.")
        return
        
    target_encoder = LabelEncoder()
    df['target_encoded'] = target_encoder.fit_transform(df['major_group'])
    
    # Lưu từ điển ánh xạ từ nhóm ngành -> danh sách các ngành cụ thể
    major_dict = df.groupby('major_group')['specific_major'].unique().apply(list).to_dict()
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(major_dict, os.path.join(model_dir, 'major_groups_dict.joblib'))

    # ----- TIỀN XỬ LÝ VÀ CHỌN ĐẶC TRƯNG -----
    df = engineer_features(df)
    
    numerical_features = [
        'math_score', 'literature_score', 'english_score',
        'physics_score', 'chemistry_score', 'biology_score',
        'history_score', 'avg_score', 'natural_science_score', 'social_science_score'
    ]
    
    categorical_features = ['mbti_type']
    
    X = df[numerical_features + categorical_features]
    y = df['target_encoded']
    
    # Chia tập train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    
    # Thiết lập ColumnTransformer để áp StandardScaler & OneHotEncoder
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ])
    
    print("\n" + "="*50)
    print("🚀 ĐANG HUẤN LUYỆN VÀ SO SÁNH 3 MÔ HÌNH MACHINE LEARNING")
    print("="*50)

    # 1. Random Forest (MÔ HÌNH CHÍNH) - TỐI ƯU SIÊU THAM SỐ
    print("⏳ Đang tính toán Tối ưu hóa siêu tham số (GridSearchCV) cho Random Forest...")
    rf_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(class_weight='balanced', random_state=random_state))
    ])
    
    param_grid = {
        'classifier__n_estimators': [100, 200],
        'classifier__max_depth': [8, 12, 16],
        'classifier__min_samples_split': [10, 15, 20],
        'classifier__min_samples_leaf': [4, 6, 8]
    }
    
    grid_search = GridSearchCV(estimator=rf_pipeline, param_grid=param_grid, cv=5, n_jobs=-1, scoring='f1_macro')
    grid_search.fit(X_train, y_train)
    
    rf_model = grid_search.best_estimator_
    print(f"🌟 [TỐI ƯU LƯỚI ĐA DIỆN] Tham số cấu hình tốt nhất: {grid_search.best_params_}")

    # 2. Decision Tree (MÔ HÌNH SO SÁNH)
    dt_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', DecisionTreeClassifier(max_depth=10, min_samples_split=15, min_samples_leaf=4, class_weight='balanced', random_state=random_state))
    ])
    dt_pipeline.fit(X_train, y_train)

    # 3. Support Vector Machine - SVM (MÔ HÌNH SO SÁNH)
    svm_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', SVC(kernel='rbf', C=0.05, probability=True, class_weight='balanced', random_state=random_state))
    ])
    svm_pipeline.fit(X_train, y_train)

    # ----- ĐÁNH GIÁ VÀ XUẤT BẢNG SO SÁNH -----
    models = {
        "Random Forest (Main)": rf_model,
        "Decision Tree       ": dt_pipeline,
        "SVM (RBF Kernel)    ": svm_pipeline
    }

    print(f"\n{'MÔ HÌNH':<25} | {'TRAIN ACC':<10} | {'TEST ACC':<10} | {'PRECISION':<10} | {'RECALL':<10} | {'F1-SCORE':<10}")
    print("-" * 88)

    for name, model in models.items():
        y_train_pred = model.predict(X_train)
        y_pred = model.predict(X_test)
        
        train_acc = accuracy_score(y_train, y_train_pred)
        acc = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='macro', zero_division=0)
        
        print(f"{name:<25} | {train_acc*100:>8.2f}% | {acc*100:>8.2f}% | {precision*100:>8.2f}% | {recall*100:>8.2f}% | {f1*100:>8.2f}%")

    print("-" * 88)

    # In Báo cáo chi tiết và Feature Importances riêng cho Random Forest
    print("\n[BÁO CÁO ĐÁNH GIÁ CHI TIẾT CỦA MÔ HÌNH RANDOM FOREST]:")
    rf_pred = rf_model.predict(X_test)
    try:
        cls_report = classification_report(y_test, rf_pred, target_names=target_encoder.classes_)
        print(cls_report)
    except Exception as e:
        print(classification_report(y_test, rf_pred))

    print("\n[XAI] MỨC ĐỘ QUAN TRỌNG CỦA CÁC ĐẶC TRƯNG (Theo Random Forest):")
    # Sử dụng preprocessor tích hợp trong pipeline để lấy đúng tên biến sau OneHot Encoding
    ohe_step = rf_model.named_steps['preprocessor'].named_transformers_['cat']
    ohe_feature_names = ohe_step.get_feature_names_out(categorical_features)
    all_feature_names = numerical_features + list(ohe_feature_names)
    
    rf_classifier = rf_model.named_steps['classifier']
    
    fi_df = pd.DataFrame({
        'Feature': all_feature_names, 
        'Importance (%)': rf_classifier.feature_importances_ * 100
    }).sort_values(by='Importance (%)', ascending=False)
    
    # Chỉ trích xuất & lưu lại danh sách Feature Importance (hiển thị cho XAI Tab)
    joblib.dump(fi_df, os.path.join(model_dir, "rf_feature_importances.joblib"))
    
    # Rút gọn việc in ấn tránh console quá dài
    for _, row in fi_df.head(15).iterrows():
        print(f" - {row['Feature']:<30}: {row['Importance (%)']:.2f}%")

    # Xuất tất cả các models ra file để sử dụng trên Web App
    joblib.dump(rf_model, os.path.join(model_dir, "random_forest_model.joblib"))
    joblib.dump(dt_pipeline, os.path.join(model_dir, "decision_tree_model.joblib"))
    joblib.dump(svm_pipeline, os.path.join(model_dir, "svm_model.joblib"))
    
    # Preprocessor cũng tiện dùng cho KNN ở file Recommender
    joblib.dump(rf_model.named_steps['preprocessor'], os.path.join(model_dir, "preprocessor.joblib"))
    joblib.dump(target_encoder, os.path.join(model_dir, "target_encoder.joblib"))
    
    # Xoá encoder MBTI cũ nếu tồn tại
    old_mbti = os.path.join(model_dir, "mbti_encoder.joblib")
    if os.path.exists(old_mbti):
        os.remove(old_mbti)
        
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