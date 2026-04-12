import pandas as pd
import numpy as np
import os
from sklearn.neighbors import KNeighborsClassifier

def map_major_to_group(major):
    major_groups = {
        "Công nghệ Thông tin & Kỹ thuật Máy tính": [
            "Khoa học Máy tính", "Khoa học máy tính", "Kỹ thuật phần mềm", "Mạng máy tính và truyền thông dữ liệu", 
            "An toàn thông tin", "An ninh mạng", "Công nghệ thông tin", "Thiết kế vi mạch", "Khoa học dữ liệu",
            "Blockchain và Tiền mã hóa", "Kỹ thuật máy tính", "Hệ thống thông tin", "Công nghệ đa phương tiện",
            "Trí tuệ nhân tạo và Học máy"
        ],
        "Y tế & Sức khỏe": [
            "Y khoa", "Y đa khoa", "Răng - Hàm - Mặt", "Dược học", "Điều dưỡng", "Y học dự phòng", 
            "Y học cổ truyền", "Kỹ thuật phục hồi chức năng", "Kỹ thuật hình ảnh y học", "Quản lý bệnh viện", "Kỹ thuật y sinh"
        ],
        "Kinh tế & Quản lý": [
            "Kinh tế", "Kinh tế quốc tế", "Quản trị kinh doanh", "Kinh doanh quốc tế", "Marketing",
            "Tài chính - Ngân hàng", "Kế toán", "Kiểm toán", "Thương mại điện tử", "Hệ thống thông tin quản lý",
            "Kinh tế số", "Logistics và Quản lý chuỗi cung ứng", "Fintech", "Quan hệ quốc tế"
        ],
        "Sư phạm & Giáo dục": [
            "Sư phạm Toán học", "Sư phạm Toán", "Sư phạm Ngữ văn", "Sư phạm Tiếng Anh", "Giáo dục Mầm non", 
            "Giáo dục Tiểu học", "Sư phạm Tin học", "Sư phạm Vật lý", "Tâm lý học giáo dục", "Sư phạm Lịch sử"
        ],
        "Ngôn ngữ & Văn hóa": [
            "Ngôn ngữ Anh", "Ngôn ngữ Trung Quốc", "Ngôn ngữ Hàn Quốc", "Ngôn ngữ Nhật", 
            "Tiếng Việt và văn hoá Việt Nam", "Văn học", "Ngôn ngữ học", "Đông phương học", "Quốc tế học"
        ],
        "Truyền thông & Báo chí": [
            "Truyền thông đa phương tiện", "Báo chí", "Quan hệ công chúng", "Truyền thông đại chúng", 
            "Công nghệ truyền thông", "Lưu trữ học", "Thông tin - thư viện"
        ],
        "Nghệ thuật & Thiết kế": [
            "Thiết kế đồ họa", "Thiết kế thời trang", "Thiết kế nội thất", "Kiến trúc", 
            "Thiết kế công nghiệp", "Thanh nhạc", "Hội họa", "Điêu khắc", "Đạo diễn Điện ảnh - Truyền hình", "Âm nhạc học"
        ],
        "Luật & Xã hội": [
            "Luật", "Luật kinh tế", "Luật quốc tế", "Tâm lý học", "Xã hội học", 
            "Chính trị học", "Quản lý nhà nước", "Công tác xã hội"
        ],
        "Kỹ thuật, Cơ khí & Ô tô": [
            "Kỹ thuật cơ khí", "Công nghệ kỹ thuật ô tô", "Kỹ thuật cơ điện tử", 
            "Kỹ thuật điều khiển và tự động hóa", "Kỹ thuật điện", "Kỹ thuật điện tử - viễn thông", 
            "Kỹ thuật điện tử - Viễn thông", "Robot và Trí tuệ nhân tạo", "Kỹ thuật hóa học", "Kỹ thuật phần mềm"
        ],
        "Nông nghiệp & Môi trường": [
            "Nông nghiệp", "Khoa học cây trồng", "Công nghệ sau thu hoạch", "Công nghệ thực phẩm",
            "Công nghệ sinh học", "Khoa học môi trường", "Nuôi trồng thủy sản", "Thú y", "Lâm nghiệp đô thị", "Kỹ thuật môi trường"
        ],
        "Xây dựng & Quy hoạch": [
            "Kỹ thuật xây dựng", "Quản lý xây dựng", "Kinh tế xây dựng", "Kỹ thuật cấp thoát nước",
            "Địa kỹ thuật xây dựng", "Công nghệ kỹ thuật công trình xây dựng"
        ],
        "Du lịch & Dịch vụ": [
            "Du lịch", "Quản trị dịch vụ du lịch và lữ hành", "Quản trị khách sạn", 
            "Quản trị nhà hàng và dịch vụ ăn uống", "Quản lý thể dục thể thao"
        ]
    }
    for g, m_list in major_groups.items():
        if major in m_list:
            return g
    return "Khác"

def main():
    np.random.seed(42)
    
    # 1. Load data
    f1 = 'data/rawdata/Career Path Recommendation Dataset for Senior High School Student in Indonesia.csv'
    f2 = 'data/rawdata/VN Student Performance.xlsx'
    f3 = 'data/rawdata/student_dataset_vi_AI_create.csv'
    
    df1 = pd.read_csv(f1, header=1)
    df2 = pd.read_excel(f2)
    df3 = pd.read_csv(f3)
    
    # 2. Extract MBTI mapping from Indonesia dataset (df1)
    df1_clean = df1[['Math', 'English', 'Physics', 'Chemistry', 'Biology', 'Unnamed: 4']].dropna()
    df1_clean.columns = ['math', 'english', 'physics', 'chemistry', 'biology', 'mbti']
    
    X_mbti = df1_clean[['math', 'english', 'physics', 'chemistry', 'biology']]
    y_mbti = df1_clean['mbti']
    knn_mbti = KNeighborsClassifier(n_neighbors=5)
    knn_mbti.fit(X_mbti, y_mbti)
    
    # 3. Create the resultant dataframe based on df3 individuals
    result_records = []
    
    def score_df2(row, major_group):
        val = 0
        if "Công nghệ" in major_group or "Kỹ thuật Máy tính" in major_group:
            val = row['MATH'] + row['PHYSICS'] + row['ENGLISH'] * 0.5
        elif "Y tế" in major_group:
            val = row['CHEMISTRY'] + row['BIOLOGY'] + row['MATH'] * 0.5
        elif "Kinh tế" in major_group:
            val = row['MATH'] + row['ENGLISH'] + row['LITERATURE'] * 0.5
        elif "Sư phạm" in major_group:
            val = row['LITERATURE'] + row['HISTORY'] + row['MATH'] * 0.5
        elif "Ngôn ngữ" in major_group:
            val = row['ENGLISH'] + row['LITERATURE'] + row['HISTORY'] * 0.5
        elif "Truyền thông" in major_group:
            val = row['LITERATURE'] + row['ENGLISH']
        elif "Nghệ thuật" in major_group:
            val = row['LITERATURE'] + row['HISTORY']
        elif "Luật" in major_group:
            val = row['LITERATURE'] + row['HISTORY'] + row['ENGLISH']
        elif "Cơ khí" in major_group or "Ô tô" in major_group or "Xây dựng" in major_group:
            val = row['PHYSICS'] + row['MATH'] + row['CHEMISTRY'] * 0.5
        elif "Nông nghiệp" in major_group:
            val = row['BIOLOGY'] + row['CHEMISTRY']
        elif "Du lịch" in major_group:
            val = row['ENGLISH'] + row['LITERATURE'] + row['HISTORY'] * 0.5
        else:
            val = row['MATH'] + row['LITERATURE'] + row['ENGLISH']
        return val

    for idx, row in df3.iterrows():
        student_id = row['student_id']
        specific_major = row['major']
        major_group = map_major_to_group(specific_major)
        gpa = row['gpa']
        
        major_rating = np.clip(gpa / 2.0, 1.0, 5.0)
        
        weights = df2.apply(lambda x: score_df2(x, major_group), axis=1)
        weights = weights ** 2 
        probs = weights / weights.sum()
        
        selected_idx = np.random.choice(df2.index, p=probs)
        base_scores = df2.loc[selected_idx]
        
        def add_noise(val):
            return np.clip(round(val + np.random.normal(0, 0.4), 1), 0, 10)
        
        math_score = add_noise(base_scores['MATH'])
        literature_score = add_noise(base_scores['LITERATURE'])
        english_score = add_noise(base_scores['ENGLISH'])
        physics_score = add_noise(base_scores['PHYSICS'])
        chemistry_score = add_noise(base_scores['CHEMISTRY'])
        biology_score = add_noise(base_scores['BIOLOGY'])
        history_score = add_noise(base_scores['HISTORY'])
        
        X_curr = pd.DataFrame([{
            'math': math_score * 10,
            'english': english_score * 10,
            'physics': physics_score * 10,
            'chemistry': chemistry_score * 10,
            'biology': biology_score * 10
        }])
        
        mbti_type = knn_mbti.predict(X_curr)[0]
        
        result_records.append({
            "student_id": student_id,
            "math_score": math_score,
            "literature_score": literature_score,
            "english_score": english_score,
            "physics_score": physics_score,
            "chemistry_score": chemistry_score,
            "biology_score": biology_score,
            "history_score": history_score,
            "mbti_type": mbti_type,
            "major_group": major_group,
            "specific_major": specific_major,
            "major_rating": round(major_rating, 2)
        })
        
    final_df = pd.DataFrame(result_records)
    
    output_path = 'data/student_data.csv'
    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Successfully generated {len(final_df)} records representing realistic Vietnamese students.")
    print("Saved to:", output_path)
    
    if len(final_df[final_df['major_group'] == 'Khác']) > 0:
        print("Warning: some majors were not mapped properly. Please update minor mappings:")
        print(final_df[final_df['major_group'] == 'Khác']['specific_major'].unique())


if __name__ == '__main__':
    main()
