import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from flask import Flask, request
import telebot
from telebot import types

from core.config import MAIN_BOT_TOKEN
from database.database import add_user, add_order
from database.init_db import init_db

# =====================
# INIT DB
# =====================
init_db()

# =====================
# BOT + FLASK
# =====================
bot = telebot.TeleBot(MAIN_BOT_TOKEN)
app = Flask(__name__)

# =====================
# MENU
# =====================
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛍 Services", "📦 Products")
    markup.row("💳 Payments", "📋 Orders")
    markup.row("🎫 Support", "👤 Profile")
    return markup

# =====================
# START
# =====================
@bot.message_handler(commands=['start'])
def start(message):
    u = message.from_user
    add_user(u.id, u.username, u.first_name)

    bot.send_message(
        message.chat.id,
        "👋 Welcome to Business Bot 🚀",
        reply_markup=main_menu()
    )

# =====================
# PRODUCTS
# =====================
@bot.message_handler(func=lambda m: m.text == "📦 Products")
def products(message):
    bot.send_message(
        message.chat.id,
        "📦 Order format:\n/order ProductName 1000"
    )

# =====================
# WEBHOOK (FIXED)
# =====================
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_str = request.get_data().decode("UTF-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "OK", 200
    return "INVALID", 400

# =====================
# HEALTH CHECK
# =====================
@app.route("/")
def home():
    return "Bot is running 🚀"

# =====================
# RUN (RENDER SAFE)
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    print("🚀 Bot running on port:", port)

    app.run(host="0.0.0.0", port=port)
