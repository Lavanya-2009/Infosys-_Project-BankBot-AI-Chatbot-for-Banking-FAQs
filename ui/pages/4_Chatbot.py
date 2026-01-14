import sys
import os

# ---------- PATH FIX ----------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import streamlit as st
from core.chatbot import chatbot_response


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="BankBot AI",
    page_icon="🤖",
    layout="centered"
)

# ---------- HIDE STREAMLIT UI ----------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- THEME TOGGLE & CSS ----------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

with st.sidebar:
    st.markdown("### Appearance")
    dark_default = st.session_state.theme == "dark"
    dark_mode = st.toggle("Dark mode", value=dark_default)
    st.session_state.theme = "dark" if dark_mode else "light"
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        # Clear relevant session keys
        for key in ["user_name", "role", "messages"]:
            if key in st.session_state:
                del st.session_state[key]
        # Navigate back to login page
        st.switch_page("pages/3_Login.py")


def _chat_css(theme: str) -> str:
    if theme == "light":
        return """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* App background with soft gradient (light) + banking AI image */
        .stApp {
            background-image:
                linear-gradient(to bottom right, rgba(226,232,240,0.9), rgba(248,250,252,0.9)),
                url("https://www.teloz.com/wp-content/uploads/2023/12/dall%C2%B7e-2023-12-30-140151-a-feature-image-depicting-a-banking-ai-chatbot-concept-the-image-should-include-a-modern-sleek-digital-interface-labeled-banking-ai-chatbot-with-a.webp");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* Center the chat card nicely */
        .main > div {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        /* Chat wrapper with lighter glassmorphism (light) */
        .chat-wrapper {
            max-width: 440px;
            width: 100%;
            margin: 32px auto;
            background: radial-gradient(circle at top left, rgba(255,255,255,0.82), rgba(248,250,252,0.78));
            border-radius: 24px;
            box-shadow: 0 24px 60px rgba(15,23,42,0.18);
            overflow: hidden;
            border: 2px solid rgba(148,163,184,0.9);
            backdrop-filter: blur(26px) saturate(1.2);
        }

        /* Header with gradient accent */
        .chat-header {
            background: linear-gradient(135deg, #22c55e, #0ea5e9, #6366f1);
            padding: 14px 18px;
            color: white;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .chat-header img {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            box-shadow: 0 0 0 3px rgba(248,250,252,0.8);
        }

        .header-title {
            font-weight: 600;
            font-size: 16px;
        }

        .header-status {
            font-size: 12px;
            opacity: 0.96;
        }

        /* Online dot */
        .online-dot {
            width: 10px;
            height: 10px;
            background: #22c55e;
            border-radius: 50%;
            margin-left: auto;
            box-shadow: 0 0 10px rgba(34,197,94,0.8);
        }

        /* Small badges under title */
        .badge-row {
            display: flex;
            gap: 6px;
            margin-top: 6px;
            flex-wrap: wrap;
        }

        .badge-chip {
            font-size: 10px;
            padding: 4px 8px;
            border-radius: 999px;
            background: rgba(15,23,42,0.03);
            color: #0f172a;
            border: 1px solid rgba(148,163,184,0.7);
        }

        /* Chat body */
        .chat-body {
            padding: 18px 16px 12px 16px;
            height: 420px;
            overflow-y: auto;
            background: linear-gradient(180deg, rgba(248,250,252,0.75), rgba(226,232,240,0.78));
        }

        /* Custom scrollbar */
        .chat-body::-webkit-scrollbar {
            width: 6px;
        }

        .chat-body::-webkit-scrollbar-track {
            background: transparent;
        }

        .chat-body::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #0ea5e9, #6366f1);
            border-radius: 999px;
        }

        /* Message animation */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(6px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Messages */
        .bot-msg {
            background: linear-gradient(135deg, #eef2ff, #e0f2fe);
            color: #0f172a;
            padding: 12px 14px;
            border-radius: 16px 16px 16px 6px;
            margin-bottom: 12px;
            max-width: 85%;
            font-size: 14px;
            box-shadow: 0 10px 25px rgba(15,23,42,0.06);
            border: 1px solid rgba(148,163,184,0.7);
            animation: fadeInUp 0.22s ease-out;
        }

        .user-msg {
            background: linear-gradient(135deg, #0ea5e9, #6366f1);
            color: white;
            padding: 12px 14px;
            border-radius: 16px 16px 6px 16px;
            margin-bottom: 12px;
            max-width: 85%;
            margin-left: auto;
            font-size: 14px;
            box-shadow: 0 10px 25px rgba(15,23,42,0.15);
            border: 1px solid rgba(129,140,248,0.7);
            animation: fadeInUp 0.22s ease-out;
        }

        /* Input bar */
        .chat-input {
            padding: 12px 14px;
            background: linear-gradient(135deg, #f1f5f9, #e5e7eb);
            border-top: 1px solid rgba(148,163,184,0.7);
        }

        .stChatInput {
            background: #ffffff !important;
            border-radius: 999px !important;
            padding-left: 16px !important;
            border: 1px solid rgba(148,163,184,0.65) !important;
            box-shadow: 0 0 0 1px rgba(226,232,240,1), 0 14px 35px rgba(148,163,184,0.35) !important;
        }

        .stChatInput > div > div textarea {
            color: #0f172a !important;
        }

        .stChatInput:focus-within {
            border-color: #0ea5e9 !important;
            box-shadow: 0 0 0 1px #0ea5e9, 0 18px 45px rgba(59,130,246,0.35) !important;
        }

        </style>
        """

    # dark theme (original)
    return """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* App background with soft gradient + banking AI image */
    .stApp {
        background-image:
            radial-gradient(circle at top left, rgba(15,23,42,0.96), rgba(2,6,23,0.98)),
            url("https://www.teloz.com/wp-content/uploads/2023/12/dall%C2%B7e-2023-12-30-140151-a-feature-image-depicting-a-banking-ai-chatbot-concept-the-image-should-include-a-modern-sleek-digital-interface-labeled-banking-ai-chatbot-with-a.webp");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Center the chat card nicely */
    .main > div {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }

    /* Chat wrapper with lighter glassmorphism effect (dark) */
    .chat-wrapper {
        max-width: 440px;
        width: 100%;
        margin: 32px auto;
        background: radial-gradient(circle at top left, rgba(15,23,42,0.78), rgba(15,23,42,0.74));
        border-radius: 24px;
        box-shadow: 0 28px 80px rgba(15,23,42,0.85);
        overflow: hidden;
        border: 2px solid rgba(129,140,248,0.95);
        backdrop-filter: blur(30px) saturate(1.25);
    }

    /* Header with gradient accent */
    .chat-header {
        background: linear-gradient(135deg, #22c55e, #0ea5e9, #6366f1);
        padding: 14px 18px;
        color: white;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .chat-header img {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        box-shadow: 0 0 0 3px rgba(15,23,42,0.3);
    }

    .header-title {
        font-weight: 600;
        font-size: 16px;
    }

    .header-status {
        font-size: 12px;
        opacity: 0.96;
    }

    /* Online dot */
    .online-dot {
        width: 10px;
        height: 10px;
        background: #22c55e;
        border-radius: 50%;
        margin-left: auto;
        box-shadow: 0 0 10px rgba(34,197,94,0.8);
    }

    /* Small badges under title */
    .badge-row {
        display: flex;
        gap: 6px;
        margin-top: 6px;
        flex-wrap: wrap;
    }

    .badge-chip {
        font-size: 10px;
        padding: 4px 8px;
        border-radius: 999px;
        background: rgba(15,23,42,0.45);
        color: #e5e7eb;
        border: 1px solid rgba(129,140,248,0.9);
    }

    /* Chat body */
    .chat-body {
        padding: 18px 16px 12px 16px;
        height: 420px;
        overflow-y: auto;
        background: linear-gradient(180deg, rgba(15,23,42,0.8), rgba(15,23,42,0.9));
    }

    /* Custom scrollbar */
    .chat-body::-webkit-scrollbar {
        width: 6px;
    }

    .chat-body::-webkit-scrollbar-track {
        background: transparent;
    }

    .chat-body::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #0ea5e9, #6366f1);
        border-radius: 999px;
    }

    /* Message animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(6px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Messages */
    .bot-msg {
        background: linear-gradient(135deg, rgba(15,23,42,1), rgba(30,64,175,1));
        color: #e5e7eb;
        padding: 12px 14px;
        border-radius: 16px 16px 16px 6px;
        margin-bottom: 12px;
        max-width: 85%;
        font-size: 14px;
        box-shadow: 0 10px 25px rgba(15,23,42,0.9);
        border: 1px solid rgba(148,163,184,0.5);
        animation: fadeInUp 0.22s ease-out;
    }

    .user-msg {
        background: linear-gradient(135deg, #0ea5e9, #6366f1);
        color: white;
        padding: 12px 14px;
        border-radius: 16px 16px 6px 16px;
        margin-bottom: 12px;
        max-width: 85%;
        margin-left: auto;
        font-size: 14px;
        box-shadow: 0 10px 25px rgba(15,23,42,0.85);
        border: 1px solid rgba(129,140,248,0.7);
        animation: fadeInUp 0.22s ease-out;
    }

    /* Input bar */
    .chat-input {
        padding: 12px 14px;
        background: linear-gradient(135deg, rgba(15,23,42,0.98), rgba(15,23,42,0.98));
        border-top: 1px solid rgba(30,64,175,0.8);
    }

    .stChatInput {
        background: rgba(15,23,42,0.95) !important;
        border-radius: 999px !important;
        padding-left: 16px !important;
        border: 1px solid rgba(148,163,184,0.65) !important;
        box-shadow: 0 0 0 1px rgba(15,23,42,1), 0 14px 35px rgba(15,23,42,0.7) !important;
    }

    .stChatInput > div > div textarea {
        color: #e5e7eb !important;
    }

    .stChatInput:focus-within {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 1px #0ea5e9, 0 18px 45px rgba(14,165,233,0.45) !important;
    }

    </style>
    """


st.markdown(_chat_css(st.session_state.theme), unsafe_allow_html=True)

# ---------- AUTH CHECK ----------
if "user_name" not in st.session_state:
    st.warning("🔐 Please login first")
    st.stop()

# ---------- SESSION INIT ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        ("bot", "👋 Hi! Welcome to BankBot AI. How can I help you today?")
    ]

# ---------- UI START ----------
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

# ---------- HEADER ----------
display_name = st.session_state.get("user_name", "you")

st.markdown(f"""
<div class="chat-header">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png">
    <div>
        <div class="header-title">BankBot AI</div>
        <div class="header-status">Assisting {display_name.title()} securely</div>
        <div class="badge-row">
            <span class="badge-chip">24×7 Support</span>
            <span class="badge-chip">Bank-grade Security</span>
            <span class="badge-chip">AI Powered</span>
        </div>
    </div>
    <div class="online-dot"></div>
</div>
""", unsafe_allow_html=True)

# ---------- CHAT BODY ----------
# st.markdown("<div class='chat-body'>", unsafe_allow_html=True)

for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div class='user-msg'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- INPUT ----------
user_input = st.chat_input("Type a message...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    with st.spinner("BankBot AI is thinking..."):
        response = chatbot_response(user_input, st.session_state)
    st.session_state.messages.append(("bot", response))
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
