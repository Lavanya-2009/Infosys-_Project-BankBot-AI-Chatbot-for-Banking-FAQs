from database.db import get_conn
from database.security import hash_password

DEFAULT_PASSWORD = "1234"
hashed_pwd = hash_password(DEFAULT_PASSWORD)

conn = get_conn()
cur = conn.cursor()

cur.execute("""
    UPDATE users
    SET password_hash = ?
    WHERE password_hash IS NULL
""", (hashed_pwd,))

conn.commit()
conn.close()

print("✅ Default password set for all users (1234)")
