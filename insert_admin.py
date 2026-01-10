import sqlite3
from database.security import hash_password

conn = sqlite3.connect("bankbot.db")
cur = conn.cursor()

cur.execute(
    "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
    ("admin", hash_password("admin123"))
)

conn.commit()
conn.close()
