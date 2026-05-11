import streamlit as st
import html
import base64
import os
from google import genai
from google.genai import types


def init_chatbot():
    try:
        api_key = st.secrets.get("gemini", {}).get("api_key")
        if not api_key:
            return None
        client = genai.Client(api_key=api_key)
        return client
    except Exception:
        return None

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def _scroll_chat_js():
    """Inject JS to auto-scroll the chat container to the bottom."""
    st.components.v1.html(
        '<script>setTimeout(function(){var p=window.parent.document.querySelector(\'div[data-testid="stPopoverBody"]\');'
        'if(p){p.querySelectorAll("div").forEach(function(d){var s=window.getComputedStyle(d);'
        'if((s.overflowY==="auto"||s.overflowY==="scroll")&&d.scrollHeight>d.clientHeight)'
        '{d.scrollTop=d.scrollHeight}})}},100);</script>',
        height=0
    )

def render_floating_chat():
    button_b64 = get_base64_image("assets/chat_button_icon.png")
    
    # ===== CSS =====
    st.markdown("""
    <style>
    /* ===== NÚT LƠ LỬNG (Fixed bottom-right) ===== */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 28px !important;
        right: 28px !important;
        z-index: 999999 !important;
    }
    button[data-testid="stPopoverButton"] {
        border-radius: 50% !important;
        width: 65px !important;
        height: 65px !important;
        padding: 0 !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(14,165,233,0.3) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    button[data-testid="stPopoverButton"]:hover {
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 0 12px 28px rgba(14,165,233,0.5) !important;
    }
    button[data-testid="stPopoverButton"] p,
    button[data-testid="stPopoverButton"] span {
        display: none !important;
    }

    /* ===== KHUNG POPOVER (cửa sổ chat) ===== */
    div[data-testid="stPopoverBody"] {
        width: 400px !important;
        max-width: 92vw !important;
        height: auto !important;
        min-height: 400px !important;
        max-height: 80vh !important;
        border-radius: 18px !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.18) !important;
        padding: 16px 14px 14px 14px !important;
        border: 1px solid rgba(148,163,184,0.25) !important;
        background: var(--background-color) !important;
        overflow: hidden !important;  /* Chặn cuộn toàn khung */
        display: flex !important;
        flex-direction: column !important;
    }

    /* ===== KHUNG TIN NHẮN (container có border) ===== */
    div[data-testid="stPopoverBody"] div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        border: 0px solid rgba(148,163,184,0.2) !important;
        background: var(--secondary-background-color) !important;
    }

    /* ===== CÁC NÚT CÂU HỎI MẪU ===== */
    div[data-testid="stPopoverBody"] div.row-widget button[kind="secondary"],
    div[data-testid="stPopoverBody"] div[data-testid="stButton"] > button {
        border-radius: 10px !important;
        border: 1px solid rgba(14,165,233,0.35) !important;
        background: rgba(14,165,233,0.06) !important;
        color: var(--text-color) !important;
        padding: 6px 10px !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        height: auto !important;
        min-height: 36px !important;
        white-space: normal !important;
        line-height: 1.25 !important;
        transition: background 0.15s, border-color 0.15s !important;
    }
    div[data-testid="stPopoverBody"] div[data-testid="stButton"] > button:hover {
        background: rgba(14,165,233,0.15) !important;
        border-color: #0ea5e9 !important;
    }

    /* ===== Ô NHẬP LIỆU ===== */
    div[data-testid="stPopoverBody"] div[data-testid="stChatInput"] textarea {
        border-radius: 12px !important;
    }
    
    /* Căn lề cho các message */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 15px !important;
    }
    
    /* Xóa mọi viền đen thô bao quanh */
    div[data-testid="stChatMessage"] * {
        border: none !important;
        outline: none !important;
    }

    /* Ẩn viền quanh Avatar của AI */
    div[data-testid="stChatMessage"] > div:first-child {
        background-color: transparent !important;
        box-shadow: none !important;
    }

    /* Bo góc và tạo nền xám nhạt cho nội dung chat của AI */
    div[data-testid="stChatMessageContent"] {
        background-color: #f1f5f9 !important;
        border-radius: 4px 18px 18px 18px !important;
        padding: 12px 18px !important;
        color: #1e293b !important;
        box-shadow: none !important; /* Xóa bóng đổ nếu có để tránh lỗi viền mờ */
    }
    
    /* Đồng bộ cỡ chữ bên trong AI Bubble */
    div[data-testid="stChatMessageContent"] h1,
    div[data-testid="stChatMessageContent"] h2,
    div[data-testid="stChatMessageContent"] h3,
    div[data-testid="stChatMessageContent"] h4,
    div[data-testid="stChatMessageContent"] h5,
    div[data-testid="stChatMessageContent"] h6 {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        margin-top: 12px !important;
        margin-bottom: 6px !important;
        line-height: 1.4 !important;
        color: #1e293b !important;
    }
    
    div[data-testid="stChatMessageContent"] p,
    div[data-testid="stChatMessageContent"] li,
    div[data-testid="stChatMessageContent"] span {
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        color: #1e293b !important;
        margin-bottom: 8px !important;
    }
    div[data-testid="stChatMessageContent"] p:last-child {
        margin-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if button_b64:
        st.markdown(f"""
        <style>
        button[data-testid="stPopoverButton"] {{
            background-image: url('data:image/png;base64,{button_b64}') !important;
            background-color: transparent !important;
            background-size: cover !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    # ===== POPOVER =====
    with st.popover("Chatbot"):
        system_icon_b64 = get_base64_image("assets/system_icon.png")
        icon_html = f'<img src="data:image/png;base64,{system_icon_b64}" style="width: 45px; height: 45px; border-radius: 50%; box-shadow: 0 2px 6px rgba(14,165,233,0.2);">' if system_icon_b64 else '<span style="font-size:1.5rem;">✨</span>'
        
        # Tiêu đề
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 0 0 12px 0;">
            <div style="margin-bottom: 6px;">{icon_html}</div>
            <div style="text-align: center; line-height: 1.3;">
                <span style="font-size:1.15rem; font-weight:800; color:#0ea5e9;">Tư Vấn Học Đường AI</span><br>
                <span style="font-size:0.75rem; color:gray;">Hỏi đáp tuyển sinh · Điểm chuẩn · MBTI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


        from utils.firebase_client import fb_get_chatbot_config
        chatbot_config = fb_get_chatbot_config()
        if not chatbot_config:
            chatbot_config = {
                "system_instruction": "Bạn là Tư Vấn Viên Học Đường AI.",
                "preset_questions": []
            }


        client = init_chatbot()
        if not client:
            st.error("⚠️ Chưa cấu hình API Key. Thêm `[gemini] api_key` vào `.streamlit/secrets.toml`.")
            return

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # Chuẩn bị history cho SDK
        history_for_sdk = []
        for msg in st.session_state["chat_history"]:
            history_for_sdk.append({
                "role": msg["role"],
                "parts": [{"text": msg["parts"][0]}]
            })

        chat = client.chats.create(
            model="gemini-2.5-flash",
            history=history_for_sdk,
            config=types.GenerateContentConfig(
                system_instruction=chatbot_config.get("system_instruction", "")
            )
        )

        preset_prompt = None
        
        # ===== KHUNG TIN NHẮN (scrollable, có border) =====
        chat_container = st.container(height=340, border=True)

        with chat_container:
            student_b64 = get_base64_image("assets/student_avatar.png")
            user_avatar_html = f'<img src="data:image/png;base64,{student_b64}" style="width: 32px; height: 32px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">' if student_b64 else '🧑‍🎓'
            
            if not st.session_state["chat_history"]:
                with st.chat_message("assistant", avatar="assets/ai_bot_avatar.png"):
                    st.markdown("Chào bạn! Mình là trợ lý AI chuyên tư vấn **tuyển sinh** và **hướng nghiệp**. Bạn cần hỏi gì nào?")
                
                presets = [p for p in chatbot_config.get("preset_questions", []) if p.get("is_active", True)]
                if presets:
                    st.markdown("<div style='margin-top: 10px; margin-bottom: 5px; font-size: 0.85rem; color: gray; text-align: center;'>Gợi ý câu hỏi:</div>", unsafe_allow_html=True)
                    for i, p in enumerate(presets):
                        if st.button(p.get("label", ""), use_container_width=True, key=f"preset_btn_{i}"):
                            preset_prompt = p.get("prompt", "")

            for message in st.session_state["chat_history"]:
                role = message["role"]
                text = message["parts"][0]
                if role == "user":
                    safe_text = html.escape(text)
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 15px; align-items: flex-start;">
                        <div style="background-color: #0ea5e9; color: white; padding: 10px 15px; border-radius: 18px 18px 4px 18px; max-width: 85%; font-size: 0.95rem; line-height: 1.5; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                            {safe_text}
                        </div>
                        <div style="margin-left: 10px; display: flex; align-items: flex-start;">{user_avatar_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    with st.chat_message("assistant", avatar="assets/ai_bot_avatar.png"):
                        st.markdown(text)

            # Auto-scroll xuống cuối khung chat
            _scroll_chat_js()
        # ===== Ô NHẬP LIỆU =====
        prompt = st.chat_input("Nhập câu hỏi của bạn...") or preset_prompt

        if prompt:
            with chat_container:
                safe_prompt = html.escape(prompt)
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 15px; align-items: flex-start;">
                    <div style="background-color: #0ea5e9; color: white; padding: 10px 15px; border-radius: 18px 18px 4px 18px; max-width: 85%; font-size: 0.95rem; line-height: 1.5; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        {safe_prompt}
                    </div>
                    <div style="margin-left: 10px; display: flex; align-items: flex-start;">{user_avatar_html}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Scroll xuống ngay khi gửi tin nhắn
                _scroll_chat_js()
                
                with st.chat_message("assistant", avatar="assets/ai_bot_avatar.png"):
                    placeholder = st.empty()
                    with st.spinner("Đang trả lời..."):
                        try:
                            response = chat.send_message(prompt)
                            placeholder.markdown(response.text)
                            st.session_state["chat_history"].append({"role": "user", "parts": [prompt]})
                            st.session_state["chat_history"].append({"role": "model", "parts": [response.text]})
                        except Exception as e:
                            placeholder.error(f"Lỗi: {e}")
                
                # Scroll xuống sau khi AI trả lời xong
                _scroll_chat_js()
            st.rerun()
