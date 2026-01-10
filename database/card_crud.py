from database.db import get_conn

# ---------------- ADD CARD ----------------
def add_card(card_number, account_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO cards (card_number, account_number, status)
    VALUES (?, ?, 'ACTIVE')
    """, (card_number, account_number))

    conn.commit()
    conn.close()
    return "✅ Card added successfully."


# ---------------- GET CARD ----------------
def get_card(card_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT card_number, account_number, status
    FROM cards
    WHERE card_number=?
    """, (card_number,))

    card = cur.fetchone()
    conn.close()
    return card


# ---------------- BLOCK CARD ----------------
def block_card(card_number, account_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT status FROM cards
    WHERE card_number=? AND account_number=?
    """, (card_number, account_number))

    row = cur.fetchone()
    if not row:
        conn.close()
        return "❌ Card not found for this account."

    if row[0] == "BLOCKED":
        conn.close()
        return "⚠️ Card is already blocked."

    cur.execute("""
    UPDATE cards
    SET status='BLOCKED'
    WHERE card_number=? AND account_number=?
    """, (card_number, account_number))

    conn.commit()
    conn.close()
    return "✅ Your card has been successfully blocked."


# ---------------- UNBLOCK CARD ----------------
def unblock_card(card_number, account_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT status FROM cards
    WHERE card_number=? AND account_number=?
    """, (card_number, account_number))

    row = cur.fetchone()
    if not row:
        conn.close()
        return "❌ Card not found for this account."

    if row[0] == "ACTIVE":
        conn.close()
        return "⚠️ Card is already active."

    cur.execute("""
    UPDATE cards
    SET status='ACTIVE'
    WHERE card_number=? AND account_number=?
    """, (card_number, account_number))

    conn.commit()
    conn.close()
    return "✅ Your card has been unblocked."


# ---------------- LIST USER CARDS ----------------
def list_cards(account_number):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT card_number, status
    FROM cards
    WHERE account_number=?
    """, (account_number,))

    cards = cur.fetchall()
    conn.close()
    return cards
