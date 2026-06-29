from database.database import 
check_vip

@bot.message_handler(commands=['vip'])
def vip_status(m):
    data = check_vip(m.from_user.id)

    if not data:
        bot.reply_to(m, "❌ You are not VIP")
        return

    plan, expires, status = data

    bot.reply_to(
        m,
        f"👑 VIP STATUS\n\n"
        f"📦 Plan: {plan}\n"
        f"📅 Expires: {expires}\n"
        f"📌 Status: {status}"
    )
