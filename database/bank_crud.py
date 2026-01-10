from database.db import get_conn
from database.security import hash_password, verify_password
from datetime import datetime
import hashlib
from database.security import verify_password

# =========================================================
# INTENT MODEL MANAGEMENT
# =========================================================
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_PATH = "models/intent_model.pkl"  # Path to save trained model

def retrain_intent_model():
    """
    Retrain the intent classification model using FAQs and chat logs.
    Saves the model to disk.
    """
    # 1️⃣ Fetch data for training: FAQs (question -> answer can be used for intents)
    faqs = get_all_faqs()
    if not faqs:
        raise ValueError("No FAQs available to train the model.")

    X = []
    y = []

    for faq_id, question, answer in faqs:
        X.append(question)
        y.append(answer)  # Here, answer acts as intent label
        # Optionally, you could map each question to a specific intent tag

    # 2️⃣ Create training pipeline: TF-IDF + Logistic Regression
    clf = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('lr', LogisticRegression(max_iter=500))
    ])

    # 3️⃣ Train model
    clf.fit(X, y)

    # 4️⃣ Save the trained model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(clf, MODEL_PATH)

def authenticate_account(acc_no, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT password_hash FROM accounts WHERE account_number=?",
        (acc_no,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return False

    return verify_password(password, row[0])


# =========================================================
# USER MANAGEMENT (LOGIN)
# =========================================================
def get_account_password_hash(account_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT password_hash FROM accounts WHERE account_number = ?",
        (account_number,)
    )

    row = cur.fetchone()
    conn.close()

    if row:
        return row[0]
    return None

def create_user(name, password):
    conn = get_conn()
    cur = conn.cursor()

    password_hash = hash_password(password)

    cur.execute("""
        INSERT INTO users (name, password_hash)
        VALUES (?, ?)
    """, (name, password_hash))

    conn.commit()
    conn.close()



def get_user(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name, password_hash FROM users WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()
    return row

def authenticate_user(name, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT password_hash
        FROM users
        WHERE name = ?
    """, (name,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return False

    return verify_password(password, row[0])


def get_all_users():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT name FROM users")
    users = [row[0] for row in cur.fetchall()]

    conn.close()
    return users


# =========================================================
# ACCOUNT MANAGEMENT (ACCOUNT PASSWORD)
# =========================================================

from database.security import hash_password

def create_account(user_name, account_number, acc_type, balance, password):
    conn = get_conn()
    cur = conn.cursor()

    password_hash = hash_password(password)

    cur.execute("""
        INSERT INTO accounts (
            account_number, user_name, account_type, balance, password_hash
        ) VALUES (?, ?, ?, ?, ?)
    """, (account_number, user_name, acc_type, balance, password_hash))

    conn.commit()
    conn.close()

def get_account(account_number):
    """
    Fetch single account details (used by chatbot).
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT account_number, user_name, account_type, balance, password_hash
        FROM accounts
        WHERE account_number = ?
    """, (account_number,))

    row = cur.fetchone()
    conn.close()
    return row


def get_accounts_by_user(user_name):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT account_number, account_type, balance
        FROM accounts
        WHERE user_name = ?
    """, (user_name,))

    rows = cur.fetchall()
    conn.close()
    return rows
def get_all_users_with_accounts():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_name, account_number
        FROM accounts
        ORDER BY user_name
    """)

    data = cur.fetchall()
    conn.close()
    return data


def verify_account_password(acc_no, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT password_hash
        FROM accounts
        WHERE account_number = ?
    """, (acc_no,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return False

    return verify_password(password, row[0])


# =========================================================
# BALANCE CHECK (PASSWORD REQUIRED)
# =========================================================


def check_balance(acc_no, password):
    if not verify_account_password(acc_no, password):
        return False, "❌ Incorrect account password"

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT balance
        FROM accounts
        WHERE account_number = ?
    """, (acc_no,))

    balance = cur.fetchone()[0]
    conn.close()

    return True, balance


# =========================================================
# MONEY TRANSFER (PASSWORD REQUIRED)
# =========================================================

def transfer_money(from_acc, to_acc, amount, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT balance, password_hash
        FROM accounts
        WHERE account_number = ?
    """, (from_acc,))
    sender = cur.fetchone()

    if not sender:
        conn.close()
        return False, "❌ Sender account not found"

    balance, pwd_hash = sender

    if not verify_password(password, pwd_hash):
        conn.close()
        return False, "❌ Incorrect account password"

    if balance < amount:
        conn.close()
        return False, "❌ Insufficient balance"

    cur.execute("""
        SELECT account_number
        FROM accounts
        WHERE account_number = ?
    """, (to_acc,))
    receiver = cur.fetchone()

    if not receiver:
        conn.close()
        return False, "❌ Receiver account not found"

    cur.execute(
        "UPDATE accounts SET balance = balance - ? WHERE account_number = ?",
        (amount, from_acc)
    )

    cur.execute(
        "UPDATE accounts SET balance = balance + ? WHERE account_number = ?",
        (amount, to_acc)
    )

    cur.execute("""
        INSERT INTO transactions
        (from_account, to_account, amount, timestamp)
        VALUES (?, ?, ?, ?)
    """, (from_acc, to_acc, amount, datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return True, f"✅ ₹{amount} transferred successfully"


# =========================================================
# CARD MANAGEMENT (PASSWORD REQUIRED)
# =========================================================

def block_card(card_no, acc_no, password):
    if not verify_account_password(acc_no, password):
        return False, "❌ Incorrect account password"

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE cards
        SET status = 'BLOCKED'
        WHERE card_number = ? AND account_number = ?
    """, (card_no, acc_no))

    conn.commit()
    conn.close()

    return True, "✅ Card blocked successfully"


def unblock_card(card_no, acc_no, password):
    if not verify_account_password(acc_no, password):
        return False, "❌ Incorrect account password"

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE cards
        SET status = 'ACTIVE'
        WHERE card_number = ? AND account_number = ?
    """, (card_no, acc_no))

    conn.commit()
    conn.close()

    return True, "✅ Card unblocked successfully"
# =========================================================
# CHAT LOGS (ADMIN ANALYTICS)
# =========================================================

def log_chat(username, query, intent, confidence):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO chat_logs (username, query, intent, confidence)
        VALUES (?, ?, ?, ?)
    """, (username, query, intent, confidence))

    conn.commit()
    conn.close()


def get_chat_logs(limit=100):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT username, query, intent, confidence, timestamp
        FROM chat_logs
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()
    return rows
def get_intent_distribution():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT intent, COUNT(*)
        FROM chat_logs
        GROUP BY intent
    """)

    data = cur.fetchall()
    conn.close()
    return data


def get_top_queries(limit=5):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT query, COUNT(*) as cnt
        FROM chat_logs
        GROUP BY query
        ORDER BY cnt DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()
    return rows
# =========================================================
# FAQ / KNOWLEDGE BASE
# =========================================================

def add_faq(question, answer):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO faqs (question, answer)
        VALUES (?, ?)
    """, (question, answer))

    conn.commit()
    conn.close()


def get_all_faqs():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, question, answer FROM faqs")
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_faq(faq_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM faqs WHERE id = ?", (faq_id,))
    conn.commit()
    conn.close()
