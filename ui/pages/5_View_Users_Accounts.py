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
    layout="centered"
)

# ---------- CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
}

.card {
    max-width: 700px;
    margin: auto;
    padding: 2rem;
}

.title {
    color: white;
    font-size: 2rem;
    font-weight: 800;
    text-align: center;
}

.subtitle {
    color: #94a3b8;
    text-align: center;
    margin-bottom: 1.5rem;
}

table {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------- UI ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='title'>📊 User & Account Database</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Read-only view</div>", unsafe_allow_html=True)

data = get_all_users_with_accounts()

if not data:
    st.warning("⚠️ No accounts found in database.")
else:
    df = pd.DataFrame(data, columns=["User Name", "Account Number"])
    st.dataframe(df, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
