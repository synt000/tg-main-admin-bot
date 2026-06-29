import sys
import os
import telebot
import json
from flask import Flask, request
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Startup မတိုင်မီ Database Table များကို ဆောက်ခြင်း
try:
    from core.database import init_ecommerce_db
    init_ecommerce_db()
    print("🛒 Database tables initialized successfully!")
except Exception as e:
    print(f"⚠️ Database initialization failed: {e}")

load_dotenv()

MAIN_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_TOKEN = os.getenv('ADMIN_BOT_TOKEN')

from main_bot.main import bot as main_bot
from admin_bot.main import bot as admin_bot

app = Flask(__name__)

@app.route("/")
def home():
    return "E-Commerce Multi-Bot System Server is Running ✅", 200

# --- 🛒 ၁။ MAIN BOT WEBHOOK ROUTE ---
@app.route("/webhook", methods=['POST'])
def main_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        
        # 🔍 Debug Log: Main Bot ဆီ Update ဝင်လာသမျှကို ကြည့်ရန်
        update_dict = json.loads(json_string)
        print(f"🔥 MAIN UPDATE: {json.dumps(update_dict, indent=2)}")
        
        update = telebot.types.Update.de_json(json_string)
        main_bot.process_new_updates([update])
        return "!", 200
    else:
        return "Invalid Content-Type", 400

# --- ⚙️ ၂။ ADMIN BOT WEBHOOK ROUTE ---
@app.route("/admin-webhook", methods=['POST'])
def admin_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        
        # 🔍 Debug Log: Admin Bot ဆီ Update ဝင်လာသမျှကို ကြည့်ရန်
        update_dict = json.loads(json_string)
        print(f"🔥 ADMIN UPDATE: {json.dumps(update_dict, indent=2)}")
        
        update = telebot.types.Update.de_json(json_string)
        admin_bot.process_new_updates([update])
        return "!", 200
    else:
        return "Invalid Content-Type", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
