@bot.message_handler(commands=['payments'])
def payments(m):
    if not is_owner(m.from_user.id):
        return

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, user_id, order_id, status
    FROM payments
    ORDER BY id DESC
    LIMIT 10
    """)

    data = cur.fetchall()
    conn.close()

    for p in data:
        text = f"""
💳 Payment ID: {p[0]}
👤 User: {p[1]}
📦 Order: {p[2]}
📌 Status: {p[3]}
"""

        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{p[0]}"),
            types.InlineKeyboardButton("❌ Reject", callback_data=f"reject_{p[0]}")
        )

        bot.send_message(m.chat.id, text, reply_markup=markup)
