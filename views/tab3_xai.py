import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def render_tab(active_model, model_choice):
    # Đã loại bỏ phần tab-hero cũ vì app.py đã render banner phía trên
    
    xai_col1, xai_col2 = st.columns(2, gap="large")
    
    with xai_col1:
        st.markdown(f"###  Trọng số Đặc trưng ({model_choice})")
        if model_choice.startswith("SVM"):
            st.info("Thuật toán SVM (RBF Kernel) chiếu dữ liệu lên không gian phi tuyến tính, làm giới hạn khả năng trích xuất trọng số tuyến tính trực quan.")
        else:
            # Danh sách nhãn đặc trưng (Cần khớp với số lượng đặc trưng đầu vào của mô hình)
            ALL_FEATURE_LABELS = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lý', 'Hóa học', 'Sinh học', 'Lịch sử', 'MBTI']
            
            try:
                importances = active_model.feature_importances_
                feature_names = ALL_FEATURE_LABELS[:len(importances)]
                
                fi_df = pd.DataFrame({
                    'Yếu tố': feature_names, 
                    'Đóng góp (%)': importances * 100
                }).sort_values(by='Đóng góp (%)', ascending=False)
                
                fig, ax = plt.subplots(figsize=(7, max(4, len(importances)*0.6)))
                sns.barplot(x='Đóng góp (%)', y='Yếu tố', data=fi_df, palette='viridis', hue='Yếu tố', legend=False, ax=ax)
                ax.set_xlabel("Tỉ trọng ảnh hưởng (%)")
                ax.set_ylabel("")
                sns.despine()
                
                # Đồng bộ màu sắc biểu đồ với Giao diện (Dark Mode support)
                if st.session_state.get('theme_mode', 'Light') == 'Dark':
                    fig.patch.set_facecolor('#0e1117')
                    ax.set_facecolor('#0e1117')
                    ax.xaxis.label.set_color('white')
                    ax.tick_params(colors='white')
                    for spine in ax.spines.values(): spine.set_edgecolor('white')
                
                st.pyplot(fig)
            except Exception:
                st.warning("Không thể trích xuất trọng số từ mô hình hiện tại.")

    with xai_col2:
        st.markdown("### Phân phối Dữ liệu Gốc")
        try:
            # Đảm bảo đường dẫn file csv chính xác
            df_data = pd.read_csv("data/student_data.csv")
            major_counts = df_data['major_group'].value_counts()
            
            fig_pie, ax_pie = plt.subplots(figsize=(5, 5))
            colors = sns.color_palette('Set2')[0:len(major_counts)]
            
            # Chỉnh màu chữ trong biểu đồ tròn theo Theme
            text_color = 'white' if st.session_state.get('theme_mode', 'Light') == 'Dark' else '#333333'
            
            ax_pie.pie(major_counts, labels=major_counts.index, autopct='%1.1f%%', 
                       startangle=140, colors=colors, textprops={'color': text_color})
            ax_pie.axis('equal') 
            
            if st.session_state.get('theme_mode', 'Light') == 'Dark': 
                fig_pie.patch.set_facecolor('#0e1117')
            
            st.pyplot(fig_pie)
        except Exception:
            st.info("Hệ thống đang sử dụng dữ liệu mô phỏng hoặc chưa tìm thấy file student_data.csv.")
            
    st.divider()
    st.markdown("###  Mô phỏng Dữ liệu Láng giềng (KNN Filter)")
    
    # Hiển thị các trường hợp tương đồng từ KNN được lưu trong session_state sau khi nhấn 'Xử lý' ở Tab 1
    if 'matching_students' in st.session_state and st.session_state['matching_students'] is not None:
        st.write("Dưới đây là 5 cá nhân có hồ sơ năng lực và tính cách tương đồng nhất với bạn trong tập dữ liệu:")
        cols = st.columns(5)
        for i, (_, student) in enumerate(st.session_state['matching_students'].head(5).iterrows()):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"🎯 **Hồ sơ {i+1}**")
                    st.caption(f"ID: {student.get('student_id', f'OBJ_0{i+1}')}")
                    st.write(f"**MBTI:** {student['mbti_type']}")
                    st.write(f"**Đánh giá:** {student['major_rating']:.1f}/5.0")
                    st.info(f"Ngành: {student['major_group']}")
    else:
        st.info(" Mẹo: Hãy thực hiện 'Khảo sát Phân tích' ở Tab 1 để xem các hồ sơ tương đồng tại đây.")