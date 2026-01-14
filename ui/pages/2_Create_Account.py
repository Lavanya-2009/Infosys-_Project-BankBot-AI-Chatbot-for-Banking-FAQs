import sys
import os
import sqlite3
import streamlit as st

# ---------- ADD PROJECT ROOT ----------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.bank_crud import (
    create_account,
    get_all_users,
    create_user,
    get_account,
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Create Account", page_icon="🏦", layout="centered")

# ---------------- CSS ----------------
st.markdown("""
<style>
/* ---------- GLOBAL LAYOUT & BACKGROUND ---------- */
.stApp {
    /* dark overlay + banking image background (matches login aesthetic) */
    background-image:
        linear-gradient(115deg, rgba(15,23,42,0.9), rgba(30,64,175,0.78), rgba(124,58,237,0.85)),
        url("https://tse3.mm.bing.net/th/id/OIP.azxAV4lUf-_ThFxk5b1S3QHaH6?pid=Api&P=0&h=180");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #0f172a;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Smooth scrolling and font rendering */
html, body {
    scroll-behavior: smooth;
    -webkit-font-smoothing: antialiased;
}

/* ---------- CARD / CONTAINER ---------- */
.bank-card {
    max-width: 820px;
    margin: 2.6rem auto 2.8rem auto;
    padding: 2.35rem 2.2rem 2.6rem 2.2rem;
    border-radius: 26px;
    background:
        radial-gradient(circle at top left, rgba(59, 130, 246, 0.16), transparent 60%),
        radial-gradient(circle at bottom right, rgba(45, 212, 191, 0.16), transparent 60%),
        linear-gradient(145deg, #ffffff, #f9fafb);
    border: 1px solid rgba(148, 163, 184, 0.55);
    box-shadow:
        0 26px 60px rgba(15, 23, 42, 0.16),
        0 0 0 1px rgba(226, 232, 240, 0.9);
    backdrop-filter: blur(20px) saturate(145%);
    -webkit-backdrop-filter: blur(20px) saturate(145%);
    animation: floatIn 0.85s ease-out 0.1s both;
    position: relative;
    overflow: hidden;
}

/* Gradient border halo around card */
.bank-card::before {
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(135deg, rgba(59,130,246,0.65), rgba(139,92,246,0.6), rgba(34,197,94,0.6));
    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    opacity: 0.0;
    pointer-events: none;
    transition: opacity 0.5s ease;
}

/* Light sheen effect */
.bank-card::after {
    content: "";
    position: absolute;
    inset: -80%;
    background: conic-gradient(
        from 220deg,
        rgba(129, 140, 248, 0.0),
        rgba(129, 140, 248, 0.25),
        rgba(56, 189, 248, 0.0),
        rgba(45, 212, 191, 0.26),
        rgba(129, 140, 248, 0.0)
    );
    opacity: 0;
    transform: translate3d(0, 0, 0) rotate(0deg);
    transition: opacity 0.8s ease, transform 1.6s ease-out;
    pointer-events: none;
}

.bank-card:hover::before {
    opacity: 0.9;
}

.bank-card:hover::after {
    opacity: 0.45;
    transform: translate3d(0, 0, 0) rotate(18deg);
}

/* ---------- SECTION WRAPPERS (BOUNDARIES) ---------- */
.section-wrapper {
    margin-top: 1.5rem;
    padding: 1.35rem 1.4rem 1.6rem 1.4rem;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    background:
        linear-gradient(145deg, #ffffff, #f9fafb);
    box-shadow:
        0 12px 28px rgba(15, 23, 42, 0.07),
        0 0 0 1px rgba(248, 250, 252, 0.95);
    position: relative;
    overflow: hidden;
}

/* colorful left accent bar */
.section-wrapper::before {
    content: "";
    position: absolute;
    left: -1px;
    top: 14px;
    bottom: 14px;
    width: 4px;
    border-radius: 999px;
    background: linear-gradient(180deg, #38bdf8, #6366f1, #22c55e);
    box-shadow: 0 0 18px rgba(59, 130, 246, 0.45);
}

/* soft highlight on hover */
.section-wrapper:hover {
    border-color: #bfdbfe;
    box-shadow:
        0 18px 36px rgba(15, 23, 42, 0.12),
        0 0 0 1px rgba(191, 219, 254, 0.95);
}

/* faint gradient tint inside when hovered */
.section-wrapper:hover::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at top right, rgba(191,219,254,0.35), transparent 55%);
    opacity: 0.9;
    pointer-events: none;
}

/* ---------- INNER FIELD GROUP BOUNDARIES ---------- */
.field-group {
    margin-top: 0.6rem;
    padding: 1.0rem 1.0rem 1.05rem 1.0rem;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    background: radial-gradient(circle at top left, rgba(191, 219, 254, 0.35), transparent 65%),
                #ffffff;
    box-shadow:
        0 8px 20px rgba(15, 23, 42, 0.05),
        0 0 0 1px rgba(248, 250, 252, 0.9);
}

.field-group + .field-group {
    margin-top: 0.9rem;
}

.field-group:hover {
    border-color: #93c5fd;
    box-shadow:
        0 12px 26px rgba(15, 23, 42, 0.09),
        0 0 0 1px rgba(191, 219, 254, 0.95);
}

/* ---------- SUBMIT / CREATE ACCOUNT CONTAINER ---------- */
.submit-wrapper {
    margin-top: 1.2rem;
    padding: 1.0rem 1.1rem 1.2rem 1.1rem;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    background:
        radial-gradient(circle at top left, rgba(191, 219, 254, 0.5), transparent 70%),
        #ffffff;
    box-shadow:
        0 10px 24px rgba(15, 23, 42, 0.07),
        0 0 0 1px rgba(248, 250, 252, 0.95);
}

.submit-wrapper:hover {
    border-color: #93c5fd;
    box-shadow:
        0 16px 32px rgba(15, 23, 42, 0.12),
        0 0 0 1px rgba(191, 219, 254, 0.98);
}

/* ---------- TITLES & HEADERS ---------- */
.page-title {
    font-size: 2.4rem;
    font-weight: 850;
    text-align: center;
    margin-bottom: 0.3rem;
    letter-spacing: 0.03em;
    background: linear-gradient(120deg, #0f172a, #2563eb, #7c3aed, #22c55e, #0f172a);
    background-size: 260% 260%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: titleGlow 7s ease-in-out infinite;
}

.page-subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 2.1rem;
    font-size: 0.98rem;
    opacity: 0.95;
}

/* Section headers with underline accent */
.section-title {
    font-size: 1.1rem;
    font-weight: 750;
    color: #0f172a;
    margin-top: 0.1rem;
    margin-bottom: 0.55rem;
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}

.section-title::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: -0.38rem;
    width: 60%;
    height: 2px;
    border-radius: 999px;
    background: linear-gradient(90deg, #38bdf8, #6366f1, transparent);
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.6);
}

/* small pill behind emoji/icon */
.section-title::before {
    content: "";
    position: absolute;
    left: -0.35rem;
    top: -0.15rem;
    width: 2.1rem;
    height: 2.1rem;
    border-radius: 999px;
    background: radial-gradient(circle at 30% 30%, rgba(59,130,246,0.25), transparent 70%);
    z-index: -1;
}

/* Labels */
label {
    color: #0f172a !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
}

/* ---------- INPUTS & SELECTS ---------- */
.stTextInput input,
.stNumberInput input,
.stSelectbox select {
    background: #f9fafb !important;
    color: #0f172a !important;
    border-radius: 12px;
    border: 1px solid #cbd5e1 !important;
    padding: 0.48rem 0.7rem;
    transition:
        border-color 0.22s ease,
        box-shadow 0.22s ease,
        background-color 0.25s ease,
        transform 0.15s ease;
    font-size: 0.92rem;
}

.stTextInput input::placeholder,
.stNumberInput input::placeholder {
    color: #94a3b8;
}

/* Focus states */
.stTextInput input:focus,
.stNumberInput input:focus,
.stSelectbox select:focus {
    outline: none !important;
    border-color: #2563eb !important;
    box-shadow:
        0 0 0 1px rgba(37, 99, 235, 0.9),
        0 0 18px rgba(59, 130, 246, 0.6);
    background-color: #ffffff !important;
    transform: translateY(-1px);
}

/* ---------- RADIO BUTTONS (User Type) ---------- */
div[role="radiogroup"] {
    gap: 0.75rem !important;
}

div[role="radiogroup"] label {
    color: #0f172a !important;
    font-weight: 700 !important;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    border: 1px solid #cbd5e1;
    background: #f8fafc;
    transition:
        background-color 0.22s ease,
        border-color 0.22s ease,
        box-shadow 0.22s ease,
        transform 0.12s ease;
}

div[role="radiogroup"] label:hover {
    background: #eff6ff;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.35);
    transform: translateY(-1px);
}

div[role="radiogroup"] input[type="radio"] {
    accent-color: #2563eb;
}

/* Make selected radio stand out */
@supports selector(label:has(input[type="radio"]:checked)) {
    div[role="radiogroup"] label:has(input[type="radio"]:checked) {
        background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.18), #ffffff);
        border-color: #2563eb;
        box-shadow:
            0 0 0 1px rgba(37, 99, 235, 0.8),
            0 0 16px rgba(59, 130, 246, 0.55);
        transform: translateY(-1px);
    }
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    width: 100%;
    background-image: linear-gradient(120deg, #0ea5e9, #6366f1, #22c55e);
    background-size: 220% 220%;
    color: #f9fafb;
    font-weight: 750;
    border-radius: 999px;
    padding: 0.78rem 1.6rem;
    border: 1px solid rgba(15, 23, 42, 0.05);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    box-shadow:
        0 12px 30px rgba(37, 99, 235, 0.40),
        0 0 18px rgba(56, 189, 248, 0.65);
    transition:
        transform 0.18s ease-out,
        box-shadow 0.2s ease-out,
        background-position 0.25s ease-out,
        filter 0.2s ease-out;
    cursor: pointer;
}

.stButton > button:hover {
    background-position: 100% 0%;
    transform: translateY(-2px) scale(1.01);
    box-shadow:
        0 20px 42px rgba(37, 99, 235, 0.5),
        0 0 28px rgba(56, 189, 248, 0.9);
    filter: saturate(125%);
}

.stButton > button:active {
    transform: translateY(0px) scale(0.995);
    box-shadow:
        0 8px 18px rgba(37, 99, 235, 0.35),
        0 0 16px rgba(56, 189, 248, 0.6);
}

/* Disabled */
.stButton > button:disabled {
    cursor: not-allowed;
    opacity: 0.7;
    box-shadow: none;
}

/* ---------- FEEDBACK MESSAGES ---------- */
div.stAlert {
    border-radius: 14px !important;
    border-width: 1px !important;
    border-color: #cbd5e1 !important;
    background: #eff6ff !important;
    color: #0f172a !important;
    backdrop-filter: blur(12px);
}

div.stAlert[data-baseweb="notification"] {
    animation: slideUp 0.4s ease-out both;
}

/* ---------- SCROLLBAR ---------- */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #e5e7eb;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #38bdf8, #6366f1);
    border-radius: 999px;
}

/* ---------- ANIMATIONS ---------- */
@keyframes gradientShift {
    0% { background-position: 0% 20%; }
    50% { background-position: 100% 80%; }
    100% { background-position: 0% 20%; }
}

@keyframes floatIn {
    0% {
        opacity: 0;
        transform: translate3d(0, 18px, 0) scale(0.98);
    }
    60% {
        opacity: 1;
        transform: translate3d(0, -4px, 0) scale(1.01);
    }
    100% {
        transform: translate3d(0, 0, 0) scale(1);
    }
}

@keyframes titleGlow {
    0% {
        text-shadow:
            0 0 12px rgba(129, 140, 248, 0.65),
            0 0 26px rgba(59, 130, 246, 0.8);
        filter: drop-shadow(0 0 3px rgba(56, 189, 248, 0.4));
    }
    50% {
        text-shadow:
            0 0 6px rgba(129, 140, 248, 0.7),
            0 0 18px rgba(59, 130, 246, 0.9);
        filter: drop-shadow(0 0 2px rgba(129, 140, 248, 0.6));
    }
    100% {
        text-shadow:
            0 0 12px rgba(129, 140, 248, 0.65),
            0 0 26px rgba(59, 130, 246, 0.8);
        filter: drop-shadow(0 0 3px rgba(56, 189, 248, 0.4));
    }
}

@keyframes slideUp {
    0% {
        opacity: 0;
        transform: translate3d(0, 12px, 0);
    }
    100% {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------

# st.markdown("<div class='bank-card'>", unsafe_allow_html=True)
st.markdown("<div class='page-title'>🏦 Create Bank Account</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Create user and bank account</div>", unsafe_allow_html=True)

# ================= USER SETUP =================
# st.markdown("<div class='section-wrapper'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>👤 User Setup</div>", unsafe_allow_html=True)
# st.markdown("<div class='field-group'>", unsafe_allow_html=True)

user_mode = st.radio(
    "User Type",
    ["Existing User", "New User"],
    horizontal=True
)

users = get_all_users()

selected_user = None
new_username = None
user_password = None

if user_mode == "Existing User":
    selected_user = st.selectbox("Select User", users)
else:
    new_username = st.text_input("New Username")
    user_password = st.text_input("User Login Password", type="password")

st.markdown("</div>", unsafe_allow_html=True)  # close user field-group
st.markdown("</div>", unsafe_allow_html=True)  # close user section-wrapper

# ================= ACCOUNT DETAILS =================
# st.markdown("<div class='section-wrapper'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>💳 Account Details</div>", unsafe_allow_html=True)
# st.markdown("<div class='field-group'>", unsafe_allow_html=True)

acc_no = st.text_input("Account Number")
acc_type = st.selectbox("Account Type", ["Savings", "Current"])
balance = st.number_input("Initial Balance", min_value=0.0, step=500.0)
account_password = st.text_input("Account Password", type="password")

st.markdown("</div>", unsafe_allow_html=True)  # close account field-group
st.markdown("</div>", unsafe_allow_html=True)  # close account section-wrapper

st.markdown("<br>", unsafe_allow_html=True)

# ================= SUBMIT =================
# st.markdown("<div class='submit-wrapper'>", unsafe_allow_html=True)
if st.button("Create Account", use_container_width=True):
    # ----- USER VALIDATION -----
    if user_mode == "Existing User":
        if not selected_user:
            st.error("❌ Please select a user")
            st.stop()
        final_user = selected_user
    else:
        if not new_username:
            st.error("❌ Please enter new username")
            st.stop()
        if not user_password:
            st.error("❌ Please enter user login password")
            st.stop()
        final_user = new_username.strip()

    # ----- ACCOUNT VALIDATION -----
    if not acc_no:
        st.error("❌ Please enter account number")
        st.stop()
    if not account_password:
        st.error("❌ Please enter account password")
        st.stop()

    # ----- PREVENT DUPLICATE ACCOUNT NUMBERS -----
    existing_account = get_account(acc_no)
    if existing_account is not None:
        st.error("❌ This account number already exists. Please use a different account number.")
        st.stop()

    # ----- CREATE USER FIRST -----
    if user_mode == "New User":
        try:
            create_user(final_user, user_password)
        except sqlite3.IntegrityError:
            st.error("❌ This username already exists. Please choose 'Existing User' or use a different name.")
            st.stop()

    # ----- CREATE ACCOUNT -----
    try:
        create_account(
            final_user,
            acc_no,
            acc_type,
            balance,
            account_password,
        )
    except sqlite3.IntegrityError:
        st.error("❌ This account number already exists. Please use a different account number.")
        st.stop()

    st.success("✅ User & Account created successfully")
    # Navigate to login page after successful creation
    st.switch_page("pages/3_Login.py")
st.markdown("</div>", unsafe_allow_html=True)  # close submit-wrapper

st.markdown("</div>", unsafe_allow_html=True)  # close bank-card
