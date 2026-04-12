import streamlit as st

def inject_custom_css():
    custom_css = """
    <style>
        /* 1. HIỆU ỨNG CHUNG */
        * { transition: all 0.3s ease; }
    
        /* 2. TÙY CHỈNH PHẦN CHỌN TAB (KIỂU VIÊN THUỐC - PILL TABS) */
        /* Loại bỏ triệt để đường kẻ ngang màu xám mặc định của hệ thống */
        div[data-testid="stTabs"] > div:first-child,
        div[data-testid="stTabs"] [data-baseweb="tab-list"],
        div[data-testid="stTabs"] [data-baseweb="tab-border"] {
            border-bottom: none !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        /* Cấu trúc Flexbox giúp Tab nằm giữa và tự động rơi dòng trên Mobile */
        div[data-testid="stTabs"] > div:first-child {
            flex-wrap: wrap !important; 
            gap: 10px !important;
            justify-content: center !important; 
        }
        
        /* Ẩn thanh cuộn ẩn nếu Streamlit cố tình tràn ngang */
        div[data-testid="stTabs"] > div:first-child::-webkit-scrollbar {
            display: none;
        }

        /* Loại bỏ gạch chân highlight màu đỏ/cam mặc định (Hỗ trợ đa phiên bản Streamlit) */
        div[data-baseweb="tab-highlight"],
        div[data-testid="stTabIndicator"],
        div[data-testid="stTabHighlight"] {
            display: none !important; 
            visibility: hidden !important;
            opacity: 0 !important;
            background-color: transparent !important;
            height: 0 !important;
            width: 0 !important;
        }

        /* Định dạng các nút Tab */
        button[data-baseweb="tab"] {
            font-size: 1rem !important;
            font-weight: 600 !important;
            border-radius: 30px !important;       /* Bo tròn dạng viên thuốc */
            padding: 10px 25px !important;
            margin-right: 0 !important;           /* Reset margin vì đã có gap */
            background-color: #f1f5f9 !important; /* Màu nền cho tab chưa chọn */
            border: 1px solid #e2e8f0 !important;
            color: #475569 !important;
            height: 46px !important;
            flex: 0 1 auto !important;            /* Chiều rộng tuỳ nội dung trên PC */
            transition: all 0.2s ease !important;
        }

        /* Hiệu ứng khi di chuột qua tab */
        button[data-baseweb="tab"]:hover {
            border-color: #0ea5e9 !important; /* Xanh biển lam nhạt (sky-500) */
            color: #0284c7 !important;        /* Xanh dương (sky-600) */
            background-color: #f0f9ff !important;
        }

        /* Tab khi được chọn (Active) */
        button[data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #0369a1 0%, #0ea5e9 100%) !important; /* Xanh biển gradient */
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3) !important;
        }

        /* 3. CÁC THÀNH PHẦN CONTAINER & FORM */
        div[data-testid="stForm"], div[data-testid="stExpander"], div[data-testid="stMetric"] {
            border-radius: 16px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(200, 200, 200, 0.2);
        }
        
        /* Nút bấm mặc định */
        .stButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0369a1 0%, #0ea5e9 100%) !important;
            border: none !important;
            color: white !important;
        }
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px -3px rgba(14, 165, 233, 0.4) !important;
        }
    
        /* 4. GIAO DIỆN BANNER CHÍNH (HERO) */
        .main-hero {
            background: linear-gradient(135deg, #0c4a6e 0%, #0284c7 100%); /* Nền xanh biển sâu cực đẹp */
            padding: 40px 25px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
            margin-top: 10px;
            box-shadow: 0 10px 20px -5px rgba(0,0,0,0.2);
        }
        .main-hero h1 {
            font-size: 2.3rem;
            font-weight: 800;
            margin-bottom: 10px;
            color: #ffffff !important;
            letter-spacing: -0.5px;
        }
        .main-hero p {
            font-size: 1.15rem;
            color: #cbd5e1 !important;
            margin: 0;
        }
        
        /* 5. MBTI CARDS & INTERACTIVE ELEMENTS */
        .mbti-card-display {
            padding: 2.2rem 1.5rem;
            border-radius: 20px;
            height: 220px;
            color: #1e293b;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            border: 1px solid rgba(255,255,255,0.3);
            display: flex;
            flex-direction: column;
            position: relative;
        }
        .mbti-card-display h4 {
            font-size: 1.35rem;
            font-weight: 800;
            margin-bottom: 10px;
        }
        .mbti-card-container [data-testid="column"]:hover .mbti-card-display {
            transform: translateY(-8px);
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
        }

        /* 6. RESPONSIVE ĐIỆN THOẠI (MOBILE QUERIES) */
        @media screen and (max-width: 768px) {
            /* Tùy chỉnh Tabs trên điện thoại */
            button[data-baseweb="tab"] {
                font-size: 0.9rem !important;
                padding: 8px 16px !important;
                height: 42px !important;
                flex: 1 1 100% !important; /* Mở rộng toàn bộ chiều rộng hoặc co giãn tự do */
                max-width: 100% !important; 
                margin-bottom: 5px !important; /* Vì ráp dòng nên cần margin dưới */
            }

            /* Thu gọn Banner Hero */
            .main-hero {
                padding: 25px 15px;
                border-radius: 15px;
                margin-bottom: 20px;
            }
            .main-hero h1 {
                font-size: 1.6rem;
            }
            .main-hero p {
                font-size: 0.95rem;
            }
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_hero(title, subtitle):
    st.markdown(f"""
        <div class="main-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)