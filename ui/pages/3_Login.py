# import sys
# import os
# import streamlit as st

# # --------------------------------------------------
# # PATH FIX
# # --------------------------------------------------
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# if BASE_DIR not in sys.path:
#     sys.path.insert(0, BASE_DIR)

# from database.bank_crud import get_all_users, get_user
# from database.security import verify_password

# # --------------------------------------------------
# # PAGE CONFIG
# # --------------------------------------------------
# st.set_page_config(
#     page_title="User Login",
#     page_icon="🔐",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # --------------------------------------------------
# # CSS
# # --------------------------------------------------
# st.markdown("""
# <style>
# header {visibility: hidden;}
# footer {visibility: hidden;}

# .stApp {
#     margin-top: -60px;
#     background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
# }

# .login-title {
#     color: #ffffff;
#     font-size: 2.1rem;
#     font-weight: 800;
#     text-align: center;
# }

# .login-subtitle {
#     color: #d1d5db;
#     text-align: center;
#     margin-bottom: 2rem;
# }

# .login-card {
#     background: rgba(255,255,255,0.12);
#     backdrop-filter: blur(12px);
#     padding: 2.2rem;
#     border-radius: 18px;
#     max-width: 420px;
#     margin: auto;
#     box-shadow: 0 20px 40px rgba(0,0,0,0.35);
# }

# label {
#     color: white !important;
#     font-weight: 600;
# }

# .stTextInput > div > div,
# .stSelectbox > div {
#     background-color: white;
#     border-radius: 12px;
# }

# .stButton button {
#     background: linear-gradient(90deg, #0072ff, #00c6ff);
#     color: white;
#     font-weight: 700;
#     border-radius: 30px;
#     padding: 0.7rem;
#     font-size: 1rem;
# }
# </style>
# """, unsafe_allow_html=True)

# # --------------------------------------------------
# # AUTO REDIRECT IF ALREADY LOGGED IN
# # --------------------------------------------------
# if "user_name" in st.session_state:
#     role = st.session_state.get("role", "user")

#     if role == "admin":
#         st.switch_page("pages/6_Admin.py")
#     else:
#         st.switch_page("pages/4_Chatbot.py")

# # --------------------------------------------------
# # UI
# # --------------------------------------------------
# st.markdown("<div class='login-title'>🔐 User Login</div>", unsafe_allow_html=True)
# st.markdown("<div class='login-subtitle'>Login using your credentials</div>", unsafe_allow_html=True)

# users = get_all_users()

# if not users:
#     st.warning("⚠️ No users found. Please create a user first.")
#     st.stop()

# st.markdown("<div class='login-card'>", unsafe_allow_html=True)

# selected_user = st.selectbox("👤 Select User", users)
# password = st.text_input("🔑 Password", type="password")

# st.markdown("<br>", unsafe_allow_html=True)

# # --------------------------------------------------
# # LOGIN LOGIC (TUPLE SAFE)
# # --------------------------------------------------
# if st.button("Login", use_container_width=True):
#     user = get_user(selected_user)

#     if not user:
#         st.error("❌ User not found")

#     # user tuple structure: (username, password)
#     elif not verify_password(password, user[1]):
#         st.error("❌ Incorrect password")

#     else:
#         # SAVE SESSION
#         st.session_state["user_name"] = user[0]

#         # ADMIN CHECK
#         if user[0].lower() == "admin":
#             st.session_state["role"] = "admin"
#             st.success("✅ Admin login successful")
#             st.switch_page("pages/6_Admin.py")
#         else:
#             st.session_state["role"] = "user"
#             st.success("✅ Login successful")
#             st.switch_page("pages/4_Chatbot.py")

# st.markdown("</div>", unsafe_allow_html=True)
import sys
import os
import time
import streamlit as st

# --------------------------------------------------
# PATH FIX
# --------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.bank_crud import get_all_users, get_user
from database.security import verify_password

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Secure Login | BankBot",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# SESSION DEFAULTS
# --------------------------------------------------
st.session_state.setdefault("dark_mode", False)
st.session_state.setdefault("theme", "user")

# --------------------------------------------------
# THEME VARIABLES
# --------------------------------------------------
if st.session_state["theme"] == "admin":
    ACCENT_1 = "#7c3aed"
    ACCENT_2 = "#a855f7"
else:
    ACCENT_1 = "#4f46e5"
    ACCENT_2 = "#22d3ee"

BG = "#0b1220" if st.session_state["dark_mode"] else "#f4f7ff"
CARD = "#111827" if st.session_state["dark_mode"] else "#ffffff"
TEXT = "#e5e7eb" if st.session_state["dark_mode"] else "#0f172a"

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown(f"""
<style>
header, footer {{ visibility: hidden; }}

/* FULL-PAGE BACKGROUND WITH DARK OVERLAY (LIKE REFERENCE DASHBOARD) */
.stApp {{
    background-image:
        linear-gradient(115deg, rgba(15,23,42,0.95), rgba(30,64,175,0.75), rgba(124,58,237,0.8)),
        url("https://tse2.mm.bing.net/th/id/OIP.90qlAsgN-sKqOBFHh0RVKAHaEK?pid=Api&P=0&h=180");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    transition: background 0.4s ease, color 0.4s ease;
}}

/* TOP NAVBAR (GLASS, BLURRED) */
.top-nav {{
    position: fixed;
    inset: 0 0 auto 0;
    height: 64px;
    padding: 0 3.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(120deg, rgba(15,23,42,0.88), rgba(30,64,175,0.8));
    backdrop-filter: blur(18px);
    box-shadow: 0 18px 45px rgba(15,23,42,0.9);
    border-bottom: 1px solid rgba(148,163,184,0.55);
    z-index: 1000;
}}

.nav-left {{
    display: flex;
    align-items: center;
    gap: 10px;
    color: #e5e7eb;
    font-weight: 700;
}}

.nav-logo {{
    width: 34px;
    height: 34px;
    border-radius: 999px;
    background: radial-gradient(circle at 30% 0%, #fde68a, #f97316);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 0 3px rgba(15,23,42,0.6);
    font-size: 18px;
}}

.nav-links {{
    display: flex;
    gap: 28px;
    color: #e5e7eb;
    font-size: 0.95rem;
    opacity: 0.9;
}}

.nav-link-active {{
    padding: 6px 16px;
    border-radius: 999px;
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(129,140,248,0.8);
}}

.nav-cta {{
    padding: 7px 18px;
    border-radius: 999px;
    background: linear-gradient(135deg, {ACCENT_1}, {ACCENT_2});
    color: white;
    font-weight: 700;
    font-size: 0.9rem;
    box-shadow: 0 14px 30px rgba(15,23,42,0.7);
}}

/* PAGE CONTENT WRAPPER (PUSHED BELOW NAVBAR) */
.page-shell {{
    max-width: 1120px;
    margin: 0 auto;
    padding: 96px 1.75rem 56px 1.75rem;
}}

/* HERO SECTION – TITLE ABOVE CARD */
.hero {{
    text-align: center;
    color: #e5e7eb;
    margin-bottom: 32px;
}}

.hero-title {{
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    text-shadow: 0 18px 40px rgba(15,23,42,0.95);
}}

.hero-subtitle {{
    margin-top: 8px;
    font-size: 0.98rem;
    color: rgba(209,213,219,0.9);
}}

/* LOGIN CARD – GLASS PANEL LIKE DASHBOARD TILES */
.login-card {{
    background: radial-gradient(circle at 0 0, rgba(148,163,184,0.22), transparent 60%),
                radial-gradient(circle at 100% 100%, rgba(56,189,248,0.16), transparent 55%),
                rgba(15,23,42,0.86);
    backdrop-filter: blur(20px) saturate(1.1);
    padding: 2.4rem 2.6rem;
    border-radius: 24px;
    max-width: 480px;
    margin: 0 auto;
    box-shadow: 0 26px 70px rgba(15,23,42,0.95);
    border: 1.5px solid rgba(148,163,184,0.85);
    animation: card-in 0.7s ease-out;
    position: relative;
    overflow: hidden;
}}

.login-card::before {{
    content: "";
    position: absolute;
    inset: -40%;
    background:
        radial-gradient(circle at 0% 0%, rgba(255,255,255,0.16), transparent 60%),
        radial-gradient(circle at 100% 100%, rgba(129,140,248,0.16), transparent 60%);
    opacity: 0.8;
    pointer-events: none;
}}

@keyframes card-in {{
    from {{ opacity: 0; transform: translateY(30px) scale(0.98); }}
    to   {{ opacity: 1; transform: translateY(0)    scale(1); }}
}}

h2 {{
    color: {TEXT};
    text-align: center;
    margin-bottom: 0.4rem;
}}

.login-subtitle {{
    color: rgba(148,163,184,0.95);
    text-align: center;
    font-size: 0.9rem;
    margin-bottom: 1.6rem;
}}

/* INPUTS */
label {{
    color: {TEXT} !important;
    font-weight: 600;
}}

.stTextInput > div > div,
.stSelectbox > div {{
    background-color: rgba(255,255,255,0.96);
    border-radius: 14px;
    border: 1px solid rgba(209,213,219,0.9);
    box-shadow: 0 8px 22px rgba(15,23,42,0.4);
}}

.stTextInput > div > div:focus-within,
.stSelectbox > div:focus-within {{
    border-color: {ACCENT_1};
    box-shadow: 0 0 0 1px {ACCENT_1}, 0 10px 28px rgba(79,70,229,0.5);
}}

/* BUTTON */
.stButton button {{
    background: linear-gradient(120deg, {ACCENT_1}, {ACCENT_2});
    color: white;
    font-weight: 800;
    border-radius: 999px;
    padding: 0.9rem;
    font-size: 1.02rem;
    box-shadow: 0 18px 40px rgba(15,23,42,0.9);
    border: none;
    transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
}}

.stButton button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 24px 60px rgba(15,23,42,1);
    filter: brightness(1.05);
}}

.stButton button:active {{
    transform: translateY(0);
    box-shadow: 0 12px 30px rgba(15,23,42,0.9);
}}

/* INLINE LOADER */
.spinner {{
    width: 45px;
    height: 45px;
    border: 5px solid rgba(255,255,255,0.3);
    border-top: 5px solid {ACCENT_2};
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 18px auto 0 auto;
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# AUTO REDIRECT
# --------------------------------------------------
if "user_name" in st.session_state:
    if st.session_state["role"] == "admin":
        st.switch_page("pages/6_Admin.py")
    else:
        st.switch_page("pages/4_Chatbot.py")

# --------------------------------------------------
# DARK MODE TOGGLE
# --------------------------------------------------
st.toggle("🌙 Dark Mode", key="dark_mode")

# --------------------------------------------------
# TOP NAVBAR + HERO (MATCHING REFERENCE STYLE)
# --------------------------------------------------
# st.markdown(
#     """
#     <div class="top-nav">
#         <div class="nav-left">
#             <div class="nav-logo">🏦</div>
#             <div>BankBot AI</div>
#         </div>
#         <div class="nav-links">
#             <div class="nav-link-active">Login</div>
#             <div>Chatbot</div>
#             <div>Accounts</div>
#         </div>
#         <div class="nav-cta">Need Help?</div>
#     </div>
#     <div class="page-shell">
#         <div class="hero">
#             <div class="hero-title">Welcome to your BankBot</div>
#             <div class="hero-subtitle">Securely sign in to manage accounts, cards and your AI assistant.</div>
#         </div>
#     """,
#     unsafe_allow_html=True,
# )

# --------------------------------------------------
# LOGIN CARD
# --------------------------------------------------
# st.markdown('<div class="login-card">', unsafe_allow_html=True)

st.markdown("<h2>Secure Login</h2>", unsafe_allow_html=True)
st.markdown(
    "<div class='login-subtitle'>Sign in to access your personalized banking assistant</div>",
    unsafe_allow_html=True,
)

users = get_all_users()
selected_user = st.selectbox("👤 Username", users)
password = st.text_input("🔑 Password", type="password")

login = st.button("Login", use_container_width=True)

if login:
    with st.spinner("Authenticating..."):
        time.sleep(1.4)

    user = get_user(selected_user)

    if not user or not verify_password(password, user[1]):
        st.error("❌ Invalid credentials")
    else:
        st.session_state["user_name"] = user[0]

        if user[0].lower() == "admin":
            st.session_state["role"] = "admin"
            st.session_state["theme"] = "admin"
        else:
            st.session_state["role"] = "user"
            st.session_state["theme"] = "user"

        st.markdown('<div class="spinner"></div>', unsafe_allow_html=True)
        time.sleep(0.8)

        if st.session_state["role"] == "admin":
            st.switch_page("pages/6_Admin.py")
        else:
            st.switch_page("pages/4_Chatbot.py")

# Close wrappers opened for custom layout (login-card + page-shell)
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
