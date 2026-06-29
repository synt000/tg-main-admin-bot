def add_payment(user_id, order_id, proof):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO payments (user_id, order_id, proof)
    VALUES (?, ?, ?)
    """, (user_id, order_id, proof))

    conn.commit()
    conn.close()


def update_payment_status(payment_id, status):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE payments SET status = ?
    WHERE id = ?
    """, (status, payment_id))

    conn.commit()
    conn.close()
