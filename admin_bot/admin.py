import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import telebot
from core.config import ADMIN_BOT_TOKEN, OWNER_ID
from database.database import connect

# =====================
# BOT INIT
# =====================
bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

# =====================
# SECURITY CHECK
# =====================
def is_owner(uid):
    return uid == OWNER_ID

# =====================
# START
# =====================
@bot.message_handler(commands=['start'])
def start(m):
    if not is_owner(m.from_user.id):
        return bot.reply_to(m, "⛔ Access Denied")

    bot.reply_to(m, "👑 Admin Panel Ready 🚀")

# =====================
# USERS LIST
# =====================
@bot.message_handler(commands=['users'])
def users(m):
    if not is_owner(m.from_user.id):
        return bot.reply_to(m, "⛔ Access Denied")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT user_id, first_name FROM users ORDER BY id DESC LIMIT 20")
    data = cur.fetchall()

    conn.close()

    text = "👥 Latest Users:\n\n"
    for u in data:
        text += f"{u[0]} | {u[1]}\n"

    bot.send_message(m.chat.id, text)

# =====================
# ORDERS LIST
# =====================
@bot.message_handler(commands=['orders'])
def orders(m):
    if not is_owner(m.from_user.id):
        return bot.reply_to(m, "⛔ Access Denied")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT user_id, product, amount, status FROM orders ORDER BY id DESC LIMIT 20")
    data = cur.fetchall()

    conn.close()

    text = "📦 Latest Orders:\n\n"
    for o in data:
        text += f"{o[0]} | {o[1]} | {o[2]} | {o[3]}\n"

    bot.send_message(m.chat.id, text)

# =====================
# BROADCAST
# =====================
@bot.message_handler(commands=['broadcast'])
def broadcast(m):
    if not is_owner(m.from_user.id):
        return bot.reply_to(m, "⛔ Access Denied")

    msg = m.text.replace("/broadcast", "").strip()

    if not msg:
        return bot.reply_to(m, "❌ Usage: /broadcast message")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM users")
    users = cur.fetchall()

    conn.close()

    for u in users:
        try:
            bot.send_message(u[0], f"📢 {msg}")
        except:
            pass

    bot.reply_to(m, "✅ Broadcast Sent")

# =====================
# RUN BOT
# =====================
print("👑 Admin Bot Running...")

bot.polling(non_stop=True)
