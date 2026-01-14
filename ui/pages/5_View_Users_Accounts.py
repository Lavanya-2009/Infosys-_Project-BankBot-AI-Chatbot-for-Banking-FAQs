import sys
import os
import streamlit as st
import pandas as pd

# ---------- PATH FIX ----------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.bank_crud import get_all_users_with_accounts

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="User & Account Database",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- THEME STATE ----------
st.session_state.setdefault("ua_theme", "dark")

top_spacer, toggle_col = st.columns([6, 1.6])
with toggle_col:
    use_light = st.toggle(
        "☀️ Light theme",
        value=(st.session_state["ua_theme"] == "light"),
        key="ua_theme_toggle",
    )

st.session_state["ua_theme"] = "light" if use_light else "dark"
THEME = st.session_state["ua_theme"]

if THEME == "light":
    BG = "#e0f2fe"          # soft blue background
    BG_END = "#ffffff"      # smooth fade to white
    CARD_BG = "#f9fafb"     # light card surface
    CARD_GRAD_END = "#e5e7eb"
    TITLE = "#0f172a"
    SUB = "#64748b"
    BORDER = "rgba(148,163,184,0.7)"
    BADGE_BG = "rgba(15,23,42,0.04)"
    TABLE_SHADOW = "0 18px 40px rgba(15,23,42,0.18)"
else:
    BG = "#020617"
    BG_END = "#020617"
    CARD_BG = "#020617"
    CARD_GRAD_END = "rgba(15,23,42,0.96)"
    TITLE = "#e5e7eb"
    SUB = "#9ca3af"
    BORDER = "rgba(30,64,175,0.9)"
    BADGE_BG = "rgba(15,23,42,0.3)"
    TABLE_SHADOW = "0 18px 45px rgba(15,23,42,0.65)"

# ---------- CSS (DARK & LIGHT) ----------
st.markdown(
    f"""
<style>
header, footer {{ visibility: hidden; }}

.stApp {{
    /* banking dashboard background image + soft dark tint */
    background-image:
        linear-gradient(120deg, rgba(15,23,42,0.45), rgba(15,23,42,0.70)),
        url("https://tse1.mm.bing.net/th/id/OIP.dgU8FVAiJd-UHESWodzvbwHaGE?pid=Api&P=0&h=180");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: {TITLE};
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

.ua-card {{
    max-width: 780px;
    margin: 2.6rem auto 3.0rem auto;
    padding: 2.2rem 2.1rem 2.5rem 2.1rem;
    border-radius: 24px;
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.20), transparent 60%),
        radial-gradient(circle at bottom right, rgba(45,212,191,0.18), transparent 55%),
        linear-gradient(145deg, {CARD_BG}, {CARD_GRAD_END});
    border: 1px solid {BORDER};
    box-shadow:
        0 28px 70px rgba(15,23,42,0.85),
        0 0 0 1px rgba(15,23,42,0.9);
    backdrop-filter: blur(22px) saturate(150%);
    -webkit-backdrop-filter: blur(22px) saturate(150%);
    position: relative;
    overflow: hidden;
    animation: card-in 0.7s ease-out;
}}

.ua-card::before {{
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(135deg, rgba(59,130,246,0.85), rgba(96,165,250,0.85), rgba(45,212,191,0.85));
    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    opacity: 0.9;
    pointer-events: none;
}}

@keyframes card-in {{
    from {{ opacity: 0; transform: translateY(24px) scale(0.98); }}
    to   {{ opacity: 1; transform: translateY(0)    scale(1); }}
}}

.ua-title {{
    font-size: 2.1rem;
    font-weight: 850;
    text-align: center;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
    background: linear-gradient(120deg, #e5e7eb, #38bdf8, #a5b4fc, #facc15, #e5e7eb);
    background-size: 260% 260%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: titleGlow 9s ease-in-out infinite;
}}

@keyframes titleGlow {{
    0%   {{ filter: drop-shadow(0 0 0px rgba(56,189,248,0.0)); }}
    50%  {{ filter: drop-shadow(0 0 18px rgba(56,189,248,0.8)); }}
    100% {{ filter: drop-shadow(0 0 0px rgba(56,189,248,0.0)); }}
}}

.ua-subtitle {{
    text-align: center;
    color: {SUB};
    margin-bottom: 1.7rem;
    font-size: 0.96rem;
}}

.ua-badge-row {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 1.2rem;
}}

.ua-badge {{
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    border: 1px solid rgba(148,163,184,0.7);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {SUB};
    background: {BADGE_BG};
}}

/* DataFrame wrapper for subtle animation */
[data-testid="stDataFrame"] {{
    border-radius: 16px;
    box-shadow: {TABLE_SHADOW};
    border: 1px solid rgba(148,163,184,0.7);
    overflow: hidden;
    animation: table-rise 0.6s ease-out;
}}

@keyframes table-rise {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to   {{ opacity: 1; transform: translateY(0px); }}
}}

/* Subtle scrollbar */
::-webkit-scrollbar {{ width: 8px; height: 8px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: linear-gradient(180deg, #38bdf8, #6366f1);
    border-radius: 999px;
}}

</style>
""",
    unsafe_allow_html=True,
)

# ---------- UI ----------
# st.markdown("<div class='ua-card'>", unsafe_allow_html=True)
st.markdown("<div class='ua-title'>📊 User & Account Database</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='ua-subtitle'>Live, read-only view of all customer accounts currently stored in BankBot.</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class='ua-badge-row'>
        <span class='ua-badge'>Real-time snapshot</span>
        <span class='ua-badge'>Secure read-only access</span>
        <span class='ua-badge'>Filtered by user & account</span>
    </div>
    """,
    unsafe_allow_html=True,
)

data = get_all_users_with_accounts()

if not data:
    st.warning("⚠️ No accounts found in database.")
else:
    df = pd.DataFrame(data, columns=["User Name", "Account Number"])
    st.dataframe(df, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
