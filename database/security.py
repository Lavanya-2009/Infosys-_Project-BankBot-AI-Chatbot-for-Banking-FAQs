import bcrypt

# ---------------- HASH PASSWORD ----------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


# ---------------- VERIFY PASSWORD ----------------
def verify_password(password: str, stored_hash) -> bool:
    if not stored_hash:
        return False

    # SQLite may return bytes OR string
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode("utf-8")

    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored_hash
    )
