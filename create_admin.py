from database.bank_crud import create_user, get_all_users
from database.db import get_conn
from database.security import hash_password

def reset_admin():
    conn = get_conn()
    cur = conn.cursor()

    # Delete old admin (case-insensitive)
    cur.execute("DELETE FROM users WHERE LOWER(name) = 'admin'")
    conn.commit()

    # Create new admin
    admin_username = "admin"
    admin_password = "admin123"
    password_hash = hash_password(admin_password)

    cur.execute("INSERT INTO users (name, password_hash) VALUES (?, ?)",
                (admin_username, password_hash))
    conn.commit()
    conn.close()

    print("✅ Admin reset successfully! Use admin/admin123 to login.")

# Run the reset
reset_admin()
