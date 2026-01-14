import re

from nlu_engine.predictor import predict_intent
from core.llm_groq import ask_groq_llm

from database.db import get_conn
from database.bank_crud import (
    get_accounts_by_user,
    get_account,
    transfer_money,
    get_account_password_hash
)
from database.card_crud import list_cards, block_card
from database.security import verify_password


INTENT_THRESHOLD = 0.6

TRANSFER_KEYWORDS = [
    "transfer", "ransfer", "tranfer",  # common spellings/typos
    "send", "pay", "give"
]
BALANCE_KEYWORDS = ["balance", "check balance", "account balance"]
BANKING_KEYWORDS = [
    "balance", "account", "transfer", "send", "pay", "money",
    "statement", "deposit", "withdraw", "withdrawal", "card",
    "block", "loan", "upi", "ifsc", "limit", "interest"
]


# ======================================================
# ADMIN LOGGING (SAFE)
# ======================================================
def log_chat(username, query, intent, confidence):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO chat_logs (username, query, intent, confidence)
            VALUES (?, ?, ?, ?)
        """, (username, query, intent, confidence))
        conn.commit()
        conn.close()
    except Exception as e:
        print("⚠️ Logging failed:", e)


# ======================================================
# FAQ LOOKUP (ADMIN KB)
# ======================================================
def get_faq_answer(text):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT answer
        FROM faqs
        WHERE LOWER(question) LIKE ?
    """, ('%' + text.lower() + '%',))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


# ======================================================
# MAIN CHATBOT
# ======================================================
def chatbot_response(user_text, session):
    text = user_text.strip().lower()

    if "flow" not in session:
        session.flow = {}

    flow = session.flow

    # ======================================================
    # ACTIVE FLOW (HIGHEST PRIORITY)
    # ======================================================

    if flow.get("waiting_transfer_details"):
        amt = re.search(r"\d+", text)
        accs = re.findall(r"\d{4,}", text)

        if not amt or not accs:
            return "❗ Please mention amount and receiver account number."

        flow.clear()
        flow.update({
            "action": "transfer",
            "amount": int(amt.group()),
            "to_acc": accs[-1],
            "need_account": True
        })
        return "🏦 From which account do you want to transfer?"

    if flow.get("need_account") and "account_no" not in flow:
        accounts = get_accounts_by_user(session.user_name)
        acc_numbers = [str(a[0]) for a in accounts]

        if text not in acc_numbers:
            return "🏦 Select account:\n" + "\n".join(acc_numbers)

        flow["account_no"] = text
        flow["need_password"] = True
        return "🔐 Please enter your account password"

    if flow.get("need_password") and "password" not in flow:
        flow["password"] = text
        stored_hash = get_account_password_hash(flow["account_no"])

        if not verify_password(flow["password"], stored_hash):
            session.flow = {}
            return "❌ Invalid password. Please try again."

        if flow["action"] == "check_balance":
            acc = get_account(flow["account_no"])
            session.flow = {}
            return f"💰 Your balance is ₹{acc[3]}"

        if flow["action"] == "transfer":
            success, msg = transfer_money(
                from_acc=flow["account_no"],
                to_acc=flow["to_acc"],
                amount=flow["amount"],
                password=flow["password"]
            )
            session.flow = {}
            return msg

        if flow["action"] == "card_block":
            cards = list_cards(flow["account_no"])
            if not cards:
                session.flow = {}
                return "❌ No card found."

            if len(cards) == 1:
                msg = block_card(cards[0][0], flow["account_no"])
                session.flow = {}
                return msg

            flow["cards"] = [c[0] for c in cards]
            return "💳 Select card:\n" + "\n".join(flow["cards"])

    if flow.get("action") == "card_block" and "cards" in flow:
        if text not in flow["cards"]:
            return "❗ Select valid card:\n" + "\n".join(flow["cards"])

        msg = block_card(text, flow["account_no"])
        session.flow = {}
        return msg

    # ======================================================
    # FAQ (ADMIN KNOWLEDGE BASE)
    # ======================================================
    faq_answer = get_faq_answer(text)
    if faq_answer:
        return faq_answer

    # ======================================================
    # NON-BANKING SMALL TALK → LLM DIRECTLY
    # ======================================================
    # If the message does not contain any banking-related keywords,
    # skip intent classification and let the LLM answer freely.
    if not any(k in text for k in BANKING_KEYWORDS):
        return ask_groq_llm(text)

    # ======================================================
    # INTENT DETECTION + LOGGING
    # ======================================================
    intent, confidence = predict_intent(text)
    log_chat(session.user_name, user_text, intent, confidence)

    print(f"🎯 INTENT: {intent} | CONFIDENCE: {confidence}")

    # If the model is not confident, try simple keyword-based
    # fallback for core banking intents before using the LLM.
    if confidence < INTENT_THRESHOLD:
        if any(k in text for k in TRANSFER_KEYWORDS):
            intent = "transfer_money"
        elif any(k in text for k in BALANCE_KEYWORDS):
            intent = "check_balance"
        else:
            return ask_groq_llm(text)

    if intent == "greeting":
        return "👋 Hello! How can I help you?"

    if intent == "check_balance":
        # Extra safety: only treat as balance query if relevant keywords appear
        if not any(k in text for k in BALANCE_KEYWORDS):
            return ask_groq_llm(text)

        flow.clear()
        flow.update({
            "action": "check_balance",
            "need_account": True
        })
        return "🏦 Which account do you want to check balance for?"

    if intent == "transfer_money":
        if not any(k in text for k in TRANSFER_KEYWORDS):
            return ask_groq_llm(text)

        amt = re.search(r"\d+", text)
        accs = re.findall(r"\d{4,}", text)

        if not amt or not accs:
            flow.clear()
            flow["waiting_transfer_details"] = True
            return "❗ Please mention amount and receiver account number."

        flow.clear()
        flow.update({
            "action": "transfer",
            "amount": int(amt.group()),
            "to_acc": accs[-1],
            "need_account": True
        })
        return "🏦 From which account do you want to transfer?"

    if intent == "card_block":
        flow.clear()
        flow.update({
            "action": "card_block",
            "need_account": True
        })
        return "🏦 From which account do you want to block the card?"

    return ask_groq_llm(text)
