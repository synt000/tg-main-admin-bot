def update_order_status(order_id, status):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE orders SET status = ?
    WHERE id = ?
    """, (status, order_id))

    conn.commit()
    conn.close()
