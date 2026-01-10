# import sys
# import os

# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# if BASE_DIR not in sys.path:
#     sys.path.insert(0, BASE_DIR)

# import streamlit as st
# from core.chatbot import chatbot_response

# st.set_page_config(
#     page_title="BankBot AI",
#     page_icon="🏦",
#     layout="centered"
# )

# st.title("🏦 BankBot AI Assistant")
# st.caption("Secure • Intelligent • Fast")

# if "session" not in st.session_state:
#     st.session_state.session = {}

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ---------- LOGIN ----------
# with st.sidebar:
#     st.header("🔐 Login")
#     acc_no = st.text_input("Account Number")
#     if st.button("Login"):
#         st.session_state.session["account_no"] = acc_no
#         st.success("Login successful")

# # ---------- CHAT ----------
# user_input = st.chat_input("Ask banking queries...")

# if user_input:
#     st.session_state.messages.append(("user", user_input))
#     reply = chatbot_response(user_input, st.session_state.session)
#     st.session_state.messages.append(("bot", reply))

# for role, msg in st.session_state.messages:
#     if role == "user":
#         st.chat_message("user").write(msg)
#     else:
#         st.chat_message("assistant").write(msg)
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.db import init_db
from database.seed_data import seed_data

init_db()
seed_data()
