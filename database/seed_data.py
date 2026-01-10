from database.db import get_conn
from database.security import hash_password

def seed_data():
    conn = get_conn()
    cur = conn.cursor()

    # Check if accounts already exist
    cur.execute("SELECT COUNT(*) FROM accounts")
    count = cur.fetchone()[0]

    if count > 0:
        conn.close()
        return  # Already seeded

    pwd = hash_password("1234")

    cur.execute("""
    INSERT INTO accounts(account_number, user_name, account_type, balance, password_hash)
    VALUES
    ('10001', 'Ravi', 'Savings', 50000, ?),
    ('10002', 'Sita', 'Current', 75000, ?),
    ('10003', 'Kiran', 'Savings', 32000, ?)
    """, (pwd, pwd, pwd))

    conn.commit()
    conn.close()
    print("✅ Sample data inserted")
