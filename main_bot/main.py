import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import telebot
from telebot import types

from core.config import MAIN_BOT_TOKEN
from database.database import add_user, add_order

bot = telebot.TeleBot(MAIN_BOT_TOKEN)

# MENU
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛍 Services", "📦 Products")
    markup.row("💳 Payments", "📋 Orders")
    markup.row("🎫 Support", "👤 Profile")
    return markup

# START
@bot.message_handler(commands=['start'])
def start(message):
    u = message.from_user

    add_user(u.id, u.username, u.first_name)

    bot.send_message(
        message.chat.id,
        "👋 Welcome to Business Bot",
        reply_markup=main_menu()
    )

# PRODUCTS → ORDER INFO
@bot.message_handler(func=lambda m: m.text == "📦 Products")
def products(message):
    bot.send_message(
        message.chat.id,
        "📦 Order format:\n/order ProductName 1000"
    )

# ORDER COMMAND
@bot.message_handler(commands=['order'])
def order(message):
    try:
        parts = message.text.split()
        product = parts[1]
        amount = int(parts[2])

        add_order(message.from_user.id, product, amount)

        bot.send_message(message.chat.id, "✅ Order placed successfully")

    except:
        bot.send_message(message.chat.id, "❌ Use: /order ProductName 1000")

# OTHERS
@bot.message_handler(func=lambda m: m.text == "🛍 Services")
def services(m):
    bot.send_message(m.chat.id, "🛍 Services available")

@bot.message_handler(func=lambda m: m.text == "💳 Payments")
def payments(m):
    bot.send_message(m.chat.id, "💳 KBZ / Wave Pay")

@bot.message_handler(func=lambda m: m.text == "📋 Orders")
def orders(m):
    bot.send_message(m.chat.id, "📋 Use /order command")

@bot.message_handler(func=lambda m: m.text == "🎫 Support")
def support(m):
    bot.send_message(m.chat.id, "🎫 Contact admin")

@bot.message_handler(func=lambda m: m.text == "👤 Profile")
def profile(m):
    bot.send_message(m.chat.id, f"👤 ID: {m.from_user.id}")

print("Bot running...")
bot.infinity_polling()
