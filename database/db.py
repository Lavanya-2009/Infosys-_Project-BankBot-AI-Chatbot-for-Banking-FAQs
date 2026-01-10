import sqlite3
import os

# Always point to ONE fixed DB location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "bankbot.db")

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        name TEXT PRIMARY KEY
    )
    """)

    # ACCOUNTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_number TEXT PRIMARY KEY,
        user_name TEXT,
        account_type TEXT,
        balance INTEGER,
        password_hash TEXT
    )
    """)

    # TRANSACTIONS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_account TEXT,
        to_account TEXT,
        amount INTEGER,
        timestamp TEXT
    )
    """)

    # 🔥 CARDS (THIS WAS MISSING)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        card_number TEXT PRIMARY KEY,
        account_number TEXT,
        status TEXT
    )
    """)
        # 🧠 CHAT LOGS (FOR ANALYTICS)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        query TEXT,
        intent TEXT,
        confidence REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 📚 KNOWLEDGE BASE (FAQ)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
    """)

    # 🔐 ADMINS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

