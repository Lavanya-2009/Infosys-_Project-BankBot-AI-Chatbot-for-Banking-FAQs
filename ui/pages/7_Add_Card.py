import sys
import os
import random
import streamlit as st

# ---------- PATH FIX ----------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.bank_crud import get_all_users_with_accounts
from database.card_crud import add_card, get_card, list_cards

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Issue Card | BankBot",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- ADMIN CHECK (must come after set_page_config) ----------
if "user_name" not in st.session_state or st.session_state.get("role") != "admin":
    st.error("🚫 Access Denied: Admins only")
    st.stop()

# ---------- THEME TOGGLE & CSS ----------
if "card_dark_mode" not in st.session_state:
    st.session_state["card_dark_mode"] = False

st.toggle("🌙 Dark mode", key="card_dark_mode")

light_css = """
<style>
header, footer { visibility: hidden; }

.stApp {
    /* Banking image with a very light dark overlay so content pops */
    background-image:
        linear-gradient(120deg, rgba(15,23,42,0.35), rgba(15,23,42,0.55)),
        url("https://tse1.mm.bing.net/th/id/OIP.QedNCf1lEXNfyokLR_HXLQHaE8?pid=Api&P=0&h=180");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #111827;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.card-shell {
    max-width: 760px;
    margin: 2.5rem auto 3rem auto;
    padding: 2.1rem 2.0rem 2.4rem 2.0rem;
    border-radius: 26px;
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.16), transparent 65%),
        radial-gradient(circle at bottom right, rgba(34,197,94,0.16), transparent 60%),
        linear-gradient(145deg, #ffffff, #f9fafb);
    border: 1px solid rgba(148,163,184,0.6);
    box-shadow:
        0 18px 40px rgba(148,163,184,0.5),
        0 0 0 1px rgba(209,213,219,0.9);
    position: relative;
    overflow: hidden;
}

.card-shell::before {
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(135deg, rgba(59,130,246,0.85), rgba(129,140,248,0.85), rgba(34,197,94,0.85));
    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    opacity: 0.8;
    pointer-events: none;
}

.page-title {
    font-size: 2.1rem;
    font-weight: 850;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 0.35rem;
    background: linear-gradient(120deg, #0f172a, #2563eb, #7c3aed, #0f766e, #0f172a);
    background-size: 260% 260%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.page-subtitle {
    text-align: center;
    font-size: 0.95rem;
    color: #6b7280;
    margin-bottom: 1.9rem;
}

.section {
    margin-top: 1.2rem;
    padding: 1.1rem 1.1rem 1.3rem 1.1rem;
    border-radius: 18px;
    border: 1px solid rgba(209,213,219,0.9);
    background: linear-gradient(145deg, #ffffff, #f9fafb);
    box-shadow:
        0 16px 35px rgba(148,163,184,0.45),
        0 0 0 1px rgba(209,213,219,0.9);
}

.section-title {
    font-size: 1.0rem;
    font-weight: 750;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #0f172a;
    margin-bottom: 0.7rem;
}

/* Realistic card preview */
.physical-card {
    position: relative;
    width: 100%;
    max-width: 380px;
    aspect-ratio: 16 / 10;
    border-radius: 22px;
    padding: 1.15rem 1.4rem;
    background:
        radial-gradient(circle at 0% 0%, rgba(248,250,252,0.9), transparent 55%),
        radial-gradient(circle at 100% 100%, rgba(59,130,246,0.22), transparent 55%),
        linear-gradient(135deg, #e5e7eb, #f9fafb, #ffffff);
    box-shadow:
        0 22px 50px rgba(148,163,184,0.7),
        0 0 0 1px rgba(209,213,219,0.95);
    border: 1px solid rgba(148,163,184,0.55);
    color: #111827;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
}

.card-chip {
    width: 46px;
    height: 32px;
    border-radius: 8px;
    background: linear-gradient(135deg, #fbbf24, #f97316, #facc15);
    box-shadow: 0 0 0 1px rgba(15,23,42,0.1);
}

.card-brand {
    font-weight: 800;
    letter-spacing: 0.18em;
    font-size: 0.8rem;
    text-transform: uppercase;
    opacity: 0.9;
}

.card-number {
    font-size: 1.25rem;
    letter-spacing: 0.18em;
    margin-top: 0.8rem;
}

.card-row-bottom {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    font-size: 0.75rem;
}

.card-label {
    text-transform: uppercase;
    letter-spacing: 0.12em;
    opacity: 0.75;
    font-size: 0.7rem;
}

.card-holder {
    font-size: 0.9rem;
    font-weight: 600;
}

.card-meta {
    text-align: right;
}

/* Inputs / buttons */
.stTextInput input,
.stSelectbox select,
.stNumberInput input {
    background-color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid rgba(209,213,219,0.9) !important;
    color: #111827 !important;
}

.stTextInput input::placeholder,
.stNumberInput input::placeholder {
    color: #9ca3af !important;
}

.stButton > button {
    width: 100%;
    background-image: linear-gradient(120deg, #2563eb, #6366f1, #22c55e);
    background-size: 220% 220%;
    color: #f9fafb;
    font-weight: 750;
    border-radius: 999px;
    padding: 0.78rem 1.6rem;
    border: 1px solid rgba(30,64,175,0.8);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    box-shadow:
        0 14px 32px rgba(148,163,184,0.8),
        0 0 20px rgba(59,130,246,0.55);
    transition:
        transform 0.18s ease-out,
        box-shadow 0.22s ease-out,
        background-position 0.3s ease-out,
        filter 0.25s ease-out;
    cursor: pointer;
}

.stButton > button:hover {
    background-position: 100% 0%;
    transform: translateY(-2px) scale(1.01);
    box-shadow:
        0 22px 48px rgba(148,163,184,0.95),
        0 0 28px rgba(59,130,246,0.75);
    filter: saturate(115%);
}

.stButton > button:active {
    transform: translateY(0px) scale(0.995);
    box-shadow:
        0 10px 24px rgba(148,163,184,0.9),
        0 0 18px rgba(59,130,246,0.65);
}

</style>
"""

dark_css = """
<style>
header, footer { visibility: hidden; }

.stApp {
    /* Same image in dark mode with slightly stronger shade */
    background-image:
        linear-gradient(125deg, rgba(15,23,42,0.65), rgba(15,23,42,0.85)),
        url("https://tse1.mm.bing.net/th/id/OIP.QedNCf1lEXNfyokLR_HXLQHaE8?pid=Api&P=0&h=180");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #e5e7eb;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.card-shell {
    max-width: 760px;
    margin: 2.5rem auto 3rem auto;
    padding: 2.1rem 2.0rem 2.4rem 2.0rem;
    border-radius: 26px;
    background:
        radial-gradient(circle at top left, rgba(56,189,248,0.28), transparent 65%),
        radial-gradient(circle at bottom right, rgba(94,234,212,0.22), transparent 60%),
        linear-gradient(145deg, rgba(15,23,42,0.98), rgba(15,23,42,0.92));
    border: 1px solid rgba(148,163,184,0.6);
    box-shadow:
        0 30px 80px rgba(15,23,42,0.9),
        0 0 0 1px rgba(15,23,42,0.95);
    position: relative;
    overflow: hidden;
}

.card-shell::before {
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(135deg, rgba(56,189,248,0.9), rgba(129,140,248,0.9), rgba(34,197,94,0.9));
    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    opacity: 0.9;
    pointer-events: none;
}

.page-title {
    font-size: 2.1rem;
    font-weight: 850;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 0.35rem;
    background: linear-gradient(120deg, #e5e7eb, #38bdf8, #a5b4fc, #facc15, #e5e7eb);
    background-size: 260% 260%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.page-subtitle {
    text-align: center;
    font-size: 0.95rem;
    color: #9ca3af;
    margin-bottom: 1.9rem;
}

.section {
    margin-top: 1.2rem;
    padding: 1.1rem 1.1rem 1.3rem 1.1rem;
    border-radius: 18px;
    border: 1px solid rgba(55,65,81,0.8);
    background: radial-gradient(circle at top left, rgba(30,64,175,0.46), transparent 70%),
                rgba(15,23,42,0.96);
    box-shadow:
        0 18px 45px rgba(15,23,42,0.85),
        0 0 0 1px rgba(15,23,42,0.95);
}

.section-title {
    font-size: 1.0rem;
    font-weight: 750;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #e5e7eb;
    margin-bottom: 0.7rem;
}

/* Realistic card preview */
.physical-card {
    position: relative;
    width: 100%;
    max-width: 380px;
    aspect-ratio: 16 / 10;
    border-radius: 22px;
    padding: 1.15rem 1.4rem;
    background:
        radial-gradient(circle at 0% 0%, rgba(248,250,252,0.25), transparent 55%),
        radial-gradient(circle at 100% 100%, rgba(56,189,248,0.40), transparent 55%),
        linear-gradient(135deg, #020617, #0f172a, #1e293b);
    box-shadow:
        0 24px 60px rgba(15,23,42,0.95),
        0 0 0 1px rgba(15,23,42,0.9);
    border: 1px solid rgba(148,163,184,0.55);
    color: #f9fafb;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
}

.card-chip {
    width: 46px;
    height: 32px;
    border-radius: 8px;
    background: linear-gradient(135deg, #fbbf24, #f97316, #facc15);
    box-shadow: 0 0 0 1px rgba(15,23,42,0.8);
}

.card-brand {
    font-weight: 800;
    letter-spacing: 0.18em;
    font-size: 0.8rem;
    text-transform: uppercase;
    opacity: 0.9;
}

.card-number {
    font-size: 1.25rem;
    letter-spacing: 0.18em;
    margin-top: 0.8rem;
}

.card-row-bottom {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    font-size: 0.75rem;
}

.card-label {
    text-transform: uppercase;
    letter-spacing: 0.12em;
    opacity: 0.75;
    font-size: 0.7rem;
}

.card-holder {
    font-size: 0.9rem;
    font-weight: 600;
}

.card-meta {
    text-align: right;
}

/* Inputs / buttons */
.stTextInput input,
.stSelectbox select,
.stNumberInput input {
    background-color: rgba(15,23,42,0.95) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(55,65,81,0.9) !important;
    color: #e5e7eb !important;
}

.stTextInput input::placeholder,
.stNumberInput input::placeholder {
    color: #6b7280 !important;
}

.stButton > button {
    width: 100%;
    background-image: linear-gradient(120deg, #0ea5e9, #6366f1, #22c55e);
    background-size: 220% 220%;
    color: #f9fafb;
    font-weight: 750;
    border-radius: 999px;
    padding: 0.78rem 1.6rem;
    border: 1px solid rgba(15,23,42,0.9);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    box-shadow:
        0 14px 32px rgba(15,23,42,0.95),
        0 0 20px rgba(56,189,248,0.75);
    transition:
        transform 0.18s ease-out,
        box-shadow 0.22s ease-out,
        background-position 0.3s ease-out,
        filter 0.25s ease-out;
    cursor: pointer;
}

.stButton > button:hover {
    background-position: 100% 0%;
    transform: translateY(-2px) scale(1.01);
    box-shadow:
        0 22px 48px rgba(15,23,42,1),
        0 0 28px rgba(56,189,248,0.9);
    filter: saturate(125%);
}

.stButton > button:active {
    transform: translateY(0px) scale(0.995);
    box-shadow:
        0 10px 24px rgba(15,23,42,0.9),
        0 0 18px rgba(56,189,248,0.75);
}

</style>
"""

st.markdown(light_css if not st.session_state["card_dark_mode"] else dark_css, unsafe_allow_html=True)


# ---------- HELPERS ----------
def mask_card_number(number: str) -> str:
    """Return card number grouped in 4s for display."""
    number = number.replace(" ", "")
    return " ".join(number[i : i + 4] for i in range(0, len(number), 4))


def generate_card_number() -> str:
    """Generate a 16‑digit card number starting with 4 (Visa‑style)."""
    body = "".join(str(random.randint(0, 9)) for _ in range(15))
    return "4" + body[:15]


def generate_unique_card_number() -> str:
    for _ in range(20):
        candidate = generate_card_number()
        if not get_card(candidate):
            return candidate
    return ""


# ---------- LOAD ACCOUNTS ----------
accounts = get_all_users_with_accounts()

# st.markdown("<div class='card-shell'>", unsafe_allow_html=True)

st.markdown("<div class='page-title'>Issue New Card</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='page-subtitle'>Link a virtual bank card to an existing customer account and store it in the database.</div>",
    unsafe_allow_html=True,
)

if not accounts:
    st.warning("⚠️ No accounts found. Please create an account first.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Map user-friendly label -> (user_name, account_number)
options = {
    f"{user} • {acc}": (user, acc) for user, acc in accounts
}

left_col, right_col = st.columns([1.1, 1])

with left_col:
    # st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Account & Card Details</div>", unsafe_allow_html=True)

    selected_label = st.selectbox("Select user account", list(options.keys()))
    selected_user, selected_acc = options[selected_label]

    # Keep generated card number in session
    if "generated_card" not in st.session_state:
        st.session_state["generated_card"] = ""

    gen_col, _ = st.columns([1, 1])
    if gen_col.button("Generate card number"):
        new_no = generate_unique_card_number()
        if not new_no:
            st.error("Could not generate a unique card number. Please try again.")
        else:
            st.session_state["generated_card"] = new_no
            st.rerun()

    card_number = st.text_input(
        "Card number (16 digits)",
        value=st.session_state.get("generated_card", ""),
        max_chars=16,
    )

    cardholder = st.text_input(
        "Card holder name",
        value=selected_user.upper(),
    )

    exp_month = st.selectbox("Expiry month", [f"{i:02d}" for i in range(1, 13)], index=0)
    exp_year = st.selectbox("Expiry year", [str(y) for y in range(2026, 2036)], index=0)

    st.markdown("""<br>""", unsafe_allow_html=True)

    if st.button("Save card to database"):
        num = card_number.replace(" ", "")
        if len(num) != 16 or not num.isdigit():
            st.error("❌ Card number must be exactly 16 digits.")
        elif get_card(num):
            st.error("⚠️ This card number already exists.")
        else:
            msg = add_card(num, selected_acc)
            st.success(msg)
            st.session_state["generated_card"] = num

    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    # st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Card Preview</div>", unsafe_allow_html=True)

    display_number = st.session_state.get("generated_card") or card_number or "0000 0000 0000 0000"
    masked = mask_card_number(display_number)

    st.markdown(
        f"""
        <div class='physical-card'>
            <div>
                <div class='card-brand'>BANKBOT • PLATINUM</div>
                <div style='margin-top:0.75rem; display:flex; align-items:center; gap:0.6rem;'>
                    <div class='card-chip'></div>
                    <div style='font-size:0.80rem; opacity:0.8;'>VIRTUAL DEBIT</div>
                </div>
                <div class='card-number'>{masked}</div>
            </div>
            <div class='card-row-bottom'>
                <div>
                    <div class='card-label'>Card holder</div>
                    <div class='card-holder'>{cardholder or selected_user.upper()}</div>
                </div>
                <div class='card-meta'>
                    <div class='card-label'>Valid thru</div>
                    <div>{exp_month}/{exp_year[-2:]}</div>
                    <div style='margin-top:0.35rem; font-size:0.7rem; opacity:0.8;'>ACC {selected_acc}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""<br>""", unsafe_allow_html=True)

    # Show existing cards for this account
    cards = list_cards(selected_acc)
    if cards:
        st.caption("Existing cards for this account:")
        for cn, status in cards:
            st.write(f"• {mask_card_number(cn)} — {status}")
    else:
        st.caption("No cards found for this account yet.")

st.markdown("</div>", unsafe_allow_html=True)
