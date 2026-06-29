def add_vip(user_id, plan, expires_at):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO vip_users (user_id, plan, expires_at, status)
    VALUES (?, ?, ?, 'active')
    """, (user_id, plan, expires_at))

    conn.commit()
    conn.close()


def check_vip(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT plan, expires_at, status FROM vip_users
    WHERE user_id = ?
    """, (user_id,))

    data = cur.fetchone()
    conn.close()
    return data
