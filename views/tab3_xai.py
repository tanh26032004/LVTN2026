import streamlit as st
import pandas as pd
import plotly.express as px

def render_tab(active_model, model_choice):
    st.markdown("<h3 style='font-weight: 800; margin-bottom: 20px;'>Phân tích Mô hình & Dữ liệu</h3>", unsafe_allow_html=True)
    
    xai_col1, xai_col2 = st.columns(2, gap="large")
    
    with xai_col1:
        st.markdown(f"<h4 style='font-weight: 700; font-size: 1.1rem; margin-bottom: 15px;'>Trọng số Đặc trưng ({model_choice})</h4>", unsafe_allow_html=True)
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
                }).sort_values(by='Đóng góp (%)', ascending=True)
                
                fig = px.bar(fi_df, x='Đóng góp (%)', y='Yếu tố', orientation='h', 
                             color='Đóng góp (%)', color_continuous_scale='Viridis',
                             text_auto='.1f')
                
                fig.update_layout(
                    margin=dict(l=0, r=0, t=10, b=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis_title="Tỉ trọng ảnh hưởng (%)",
                    yaxis_title="",
                    coloraxis_showscale=False,
                    height=max(300, len(importances)*40)
                )
                
                st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            except Exception:
                st.warning("Không thể trích xuất trọng số từ mô hình hiện tại.")

    with xai_col2:
        st.markdown("<h4 style='font-weight: 700; font-size: 1.1rem; margin-bottom: 15px;'>Phân phối Dữ liệu Gốc</h4>", unsafe_allow_html=True)
        try:
            # Đảm bảo đường dẫn file csv chính xác
            df_data = pd.read_csv("data/student_data.csv")
            major_counts = df_data['major_group'].value_counts().reset_index()
            major_counts.columns = ['major_group', 'count']
            
            fig_pie = px.pie(major_counts, values='count', names='major_group', hole=0.45,
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            
            fig_pie.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                height=350
            )
            
            fig_pie.update_traces(textposition='inside', textinfo='percent+label', 
                                  hovertemplate='<b>%{label}</b><br>Số lượng: %{value}<br>Tỉ lệ: %{percent}')
            
            st.plotly_chart(fig_pie, use_container_width=True, theme="streamlit")
        except Exception:
            st.info("Hệ thống đang sử dụng dữ liệu mô phỏng hoặc chưa tìm thấy file student_data.csv.")
            
    st.markdown("<hr style='margin-top: 20px; margin-bottom: 30px; border: 0; border-top: 1px solid rgba(128, 128, 128, 0.2);'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight: 800; margin-bottom: 20px;'>Mô phỏng Dữ liệu Láng giềng (KNN Filter)</h3>", unsafe_allow_html=True)
    
    # Hiển thị các trường hợp tương đồng từ KNN được lưu trong session_state sau khi nhấn 'Xử lý' ở Tab 1
    if 'matching_students' in st.session_state and st.session_state['matching_students'] is not None:
        st.markdown("<p style='font-size: 0.95rem; margin-bottom: 20px; color: gray;'>Dưới đây là 5 cá nhân có hồ sơ năng lực và tính cách tương đồng nhất với bạn trong tập dữ liệu:</p>", unsafe_allow_html=True)
        cols = st.columns(5)
        for i, (_, student) in enumerate(st.session_state['matching_students'].head(5).iterrows()):
            with cols[i]:
                with st.container(border=True):
                    # Dùng thẻ div linh hoạt để render UI Card
                    st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 10px;">
                        <span style="font-size: 1.5rem;">👤</span><br>
                        <b style="font-size: 1rem; color: #0284c7;">Hồ sơ {i+1}</b>
                    </div>
                    <div style="font-size: 0.8rem; color: gray; text-align: center; margin-bottom: 12px; border-bottom: 1px solid rgba(128, 128, 128, 0.2); padding-bottom: 8px;">
                        ID: {student.get('student_id', f'OBJ_0{i+1}')}
                    </div>
                    <div style="margin-bottom: 6px; display: flex; justify-content: space-between;">
                        <span style="font-size: 0.85rem; color: gray;">MBTI:</span> 
                        <b style="font-size: 0.9rem;">{student['mbti_type']}</b>
                    </div>
                    <div style="margin-bottom: 12px; display: flex; justify-content: space-between;">
                        <span style="font-size: 0.85rem; color: gray;">Đánh giá:</span> 
                        <b style="font-size: 0.9rem; color: #f59e0b;">{student['major_rating']:.1f} ★</b>
                    </div>
                    <div style="background-color: rgba(16, 185, 129, 0.1); color: #10b981; padding: 6px 4px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; text-align: center; border: 1px solid rgba(16, 185, 129, 0.2);">
                        {student['major_group']}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background-color: rgba(128, 128, 128, 0.05); padding: 40px 20px; border-radius: 15px; border: 2px dashed rgba(128, 128, 128, 0.3); text-align: center;'>
            <h4 style="margin-top: 0; color: gray;">Hệ thống đang chờ dữ liệu</h4>
            <p style='font-size: 0.95rem; margin: 0; color: gray;'>
                💡 <b>Mẹo:</b> Hãy hoàn thành <b>Thông tin của bạn</b> và nhấn nút <b>Khám phá Ngành phù hợp</b> ở Tab 1 để xem các hồ sơ tương đồng tại đây.
            </p>
        </div>
        """, unsafe_allow_html=True)