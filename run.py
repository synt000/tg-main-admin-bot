import sys
import os
import telebot
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

# Token များကို သီးသန့်စီ ခွဲထုတ်ခြင်း
MAIN_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_TOKEN = os.getenv('ADMIN_BOT_TOKEN')

# ဘော့တ် Instance များကို သီးသန့်စီ ချိတ်ဆက်ခြင်း
from main_bot.main import bot as main_bot
from admin_bot.main import bot as admin_bot

app = Flask(__name__)

# --- HOME ROUTE ---
@app.route("/")
def home():
    return "E-Commerce Multi-Bot System Server is Running ✅", 200

# --- 🛒 ၁။ MAIN BOT WEBHOOK ROUTE ---
@app.route("/webhook", methods=['POST'])
def main_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
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
        update = telebot.types.Update.de_json(json_string)
        admin_bot.process_new_updates([update])
        return "!", 200
    else:
        return "Invalid Content-Type", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Render / Gunicorn က လှမ်းခေါ်ရန်အတွက် app အား ကြေညာပေးခြင်း
# Start Command: gunicorn run:app
