import pandas as pd
import numpy as np
import os

def augment_data(input_file='data/student_data.csv', output_file='data/student_data_augmented.csv', target_multiplier=5):
    """
    Data Augmentation dựa trên phân phối điểm thi THPT Quốc gia 2023.
    """
    df = pd.read_csv(input_file)
    
    # 1. Điểm trung bình kỳ thi THPT Quốc Gia 2023 (tham khảo)
    moe_means = {
        'math_score': 6.25,
        'literature_score': 6.86,
        'english_score': 5.45,
        'physics_score': 6.57,
        'chemistry_score': 6.74,
        'biology_score': 6.39,
        'history_score': 6.03
    }
    
    # Tính mean hiện tại để tìm khoảng dịch chuyển (shift)
    current_means = {col: df[col].mean() for col in moe_means.keys()}
    shift_values = {col: moe_means[col] - current_means[col] for col in moe_means.keys()}
    
    augmented_records = []
    
    # Chúng ta cũng cần sinh student_id mới
    # Tìm ID lớn nhất hiện tại: format 'SVxxxx'
    max_id = 0
    for sid in df['student_id']:
        try:
            num = int(sid.replace('SV', ''))
            if num > max_id:
                max_id = num
        except:
            pass
            
    base_id = max_id + 1
    
    np.random.seed(42)
    
    # 2. Sinh dữ liệu nhân bản
    total_new_rows = len(df) * target_multiplier
    print(f"Bắt đầu nhân bản: từ {len(df)} bản ghi gốc lên {total_new_rows} bản ghi mới...")
    
    # Chúng ta ghép cả df gốc vào (sau khi đã được shift theo MoE)
    for idx, row in df.iterrows():
        # Bản ghi gốc nhưng điều chỉnh shift
        base_record = row.to_dict()
        for col in moe_means.keys():
            base_record[col] = np.clip(round(base_record[col] + shift_values[col], 1), 0, 10)
        augmented_records.append(base_record)
        
        # Tạo thêm (target_multiplier - 1) bản ghi nhiễu
        for _ in range(target_multiplier - 1):
            new_record = row.to_dict()
            new_record['student_id'] = f"SV{base_id:05d}"
            base_id += 1
            
            # Thêm nhiễu ngẫu nhiên phân phối chuẩn (Gaussian noise) và shift theo MoE
            for col in moe_means.keys():
                noise = np.random.normal(0, 0.6)  # phương sai nho nhỏ để tạo đa dạng
                new_val = row[col] + noise + shift_values[col]
                new_record[col] = np.clip(round(new_val, 1), 0, 10)
                
            # Tạo nhiễu cho major_rating (GPA)
            noise_gpa = np.random.normal(0, 0.2)
            new_record['major_rating'] = np.clip(round(row['major_rating'] + noise_gpa, 2), 1.0, 5.0)
            
            augmented_records.append(new_record)
            
    df_aug = pd.DataFrame(augmented_records)
    
    # Shuffle dữ liệu
    df_aug = df_aug.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # In ra báo cáo phân phối
    print("\n--- Thống kê Phân phối Điểm (Sau khi Augment) ---")
    for col in moe_means.keys():
        print(f"{col}: Mean = {df_aug[col].mean():.2f} (Mục tiêu BGD: {moe_means[col]}) | Std = {df_aug[col].std():.2f}")
    
    df_aug.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n=> Đã lưu thành công dữ liệu ({len(df_aug)} dòng) vào {output_file}")

if __name__ == '__main__':
    augment_data()
