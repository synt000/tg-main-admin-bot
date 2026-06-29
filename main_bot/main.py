import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from flask import Flask, request
import telebot
from telebot import types

from core.config import MAIN_BOT_TOKEN
from database.database import add_user, add_order, add_payment
from database.init_db import init_db

# INIT DB
init_db()

bot = telebot.TeleBot(MAIN_BOT_TOKEN)
app = Flask(__name__)

# =====================
# MENU
# =====================
def menu():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.row("🛍 Services", "📦 Products")
    m.row("📋 Orders", "💳 Payments")
    return m

# =====================
# START
# =====================
@bot.message_handler(commands=['start'])
def start(m):
    u = m.from_user
    add_user(u.id, u.username, u.first_name)

    bot.send_message(
        m.chat.id,
        "👋 Welcome to SaaS Bot 🚀",
        reply_markup=menu()
    )

# =====================
# PRODUCTS
# =====================
@bot.message_handler(func=lambda m: m.text == "📦 Products")
def products(m):
    bot.send_message(
        m.chat.id,
        "📦 Order format:\n/order Product 1000"
    )

# =====================
# ORDER SYSTEM
# =====================
@bot.message_handler(commands=['order'])
def order(m):
    try:
        parts = m.text.split()

        if len(parts) < 3:
            bot.reply_to(m, "❌ Format: /order Product 1000")
            return

        product = parts[1]
        amount = parts[2]

        add_order(m.from_user.id, product, amount)

        bot.reply_to(
            m,
            f"✅ Order Created\n📦 {product}\n💰 {amount}\n📌 Status: Pending\n\n💳 Send payment proof with caption:\n/pay ORDER_ID"
        )

    except:
        bot.reply_to(m, "❌ Error occurred")

# =====================
# PAYMENT PROOF
# =====================
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

        add_payment(m.from_user.id, order_id, file_id)

        bot.reply_to(
            m,
            "✅ Payment received\n⏳ Waiting for admin approval"
        )

    except:
        bot.reply_to(m, "❌ Payment error")

# =====================
# WEBHOOK
# =====================
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# =====================
# HEALTH CHECK
# =====================
@app.route("/")
def home():
    return "🚀 SaaS Bot Running"

# =====================
# RUN SERVER
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
