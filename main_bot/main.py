@bot.message_handler(content_types=['photo'])
def payment_proof(m):
    try:
        file_id = m.photo[-1].file_id
        caption = m.caption or ""

        parts = caption.split()

        # format: /pay ORDER_ID
        if len(parts) < 2:
            bot.reply_to(m, "❌ Use caption: /pay ORDER_ID")
            return

        order_id = parts[1]

        # SAVE PAYMENT
        from database.database import add_payment
        add_payment(m.from_user.id, order_id, file_id)

        bot.reply_to(
            m,
            "✅ Payment received\n⏳ Waiting admin approval"
        )

    except:
        bot.reply_to(m, "❌ Payment error")
