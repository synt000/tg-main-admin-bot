import sys
import os
import telebot
import json
from flask import Flask, request
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Database initialized
try:
    from core.database import init_ecommerce_db
    init_ecommerce_db()
    print("🛒 Database tables initialized successfully!")
except Exception as e:
    print(f"⚠️ Database initialization failed: {e}")

load_dotenv()

# Admin IDs ကို စာရင်းအဖြစ် ပြောင်းလဲထားခြင်း
admin_env = os.getenv('ADMIN_IDS', '')
ADMIN_IDS = [int(x) for x in admin_env.split(',') if x.strip().isdigit()]

# ဘော့တ် Instance များကို Import လုပ်ခြင်း
from main_bot.main import bot as main_bot
from admin_bot.main import bot as admin_bot

app = Flask(__name__)

@app.route("/")
def home():
    return "E-Commerce Multi-Bot System Server is Running ✅", 200

# --- 🚀 BEST PRACTICE: SMART FILTER UNIFIED WEBHOOK ---
@app.route("/webhook", methods=['POST'])
def unified_webhook():
    content_type = request.headers.get("content-type", "")
    
    # ⚠️ Content-Type check fix: Telegram format အားလုံးကို လက်ခံနိုင်ရန်
    if "application/json" in content_type:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        
        # 🔍 စာသားထဲက အကြံပြုချက်အတိုင်း Chat ID ကို ရှာဖွေစစ်ထုတ်ခြင်း (Message ရော Callback Query ပါ အလုပ်လုပ်ရန်)
        chat_id = None
        if update.message:
            chat_id = update.message.chat.id
        elif update.callback_query and update.callback_query.message:
            chat_id = update.callback_query.message.chat.id
            
        # 🛒 ဝယ်သူ/အေးဂျင့် Flow အတွက် Main Bot ဆီသို့ Update အမြဲမပြတ်ပို့ခြင်း
        try:
            main_bot.process_new_updates([update])
        except Exception as e:
            print(f"⚠️ Main Bot Process Error: {e}")
            
        # ⚙️ Smart Filter: အချက်အလက်ပို့သူသည် Admin စာရင်းဝင်မှသာ Admin Bot ဆီသို့ ပို့ဆောင်ခြင်း
        if chat_id and chat_id in ADMIN_IDS:
            try:
                print(f"⚙️ Routing update to Admin Bot for Admin User ID: {chat_id}")
                admin_bot.process_new_updates([update])
            except Exception as e:
                print(f"⚠️ Admin Bot Process Error: {e}")
                
        return "!", 200
    else:
        return "Invalid Content-Type", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
