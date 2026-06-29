from database.database import add_vip
from datetime import datetime, timedelta

@bot.message_handler(commands=['givevip'])
def givevip(m):
    if not is_owner(m.from_user.id):
        return

    try:
        parts = m.text.split()

        if len(parts) < 4:
            bot.reply_to(m, "❌ Usage: /givevip user_id days plan")
            return

        user_id = int(parts[1])
        days = int(parts[2])
        plan = parts[3]

        expires = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

        add_vip(user_id, plan, expires)

        bot.reply_to(
            m,
            f"✅ VIP Granted\n👤 User: {user_id}\n📦 Plan: {plan}\n📅 Days: {days}"
        )

    except:
        bot.reply_to(m, "❌ Usage: /givevip user_id days plan")

