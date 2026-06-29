import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 🚨 အရေးကြီးဆုံးအချက်: အခြား Bot Instance များ Import မလုပ်မီ .env ကို အရင်ဆုံး အပြတ်ဖတ်ခိုင်းခြင်း
load_dotenv()

# Startup မတိုင်မီ Database Table များကို ဆောက်ခြင်း
try:
    from core.database import init_saas_database
    init_saas_database()
    print("🛒 Central Database Synchronized!")
except Exception as e:
    print(f"⚠️ Database Auto-Sync Warning: {e}")

from flask import Flask, request, jsonify
import telebot
import json

# .env ဖတ်ပြီးမှသာ ဘော့တ် Instance များကို Import လုပ်ခြင်း
from main_bot.main import bot as main_bot
from admin_bot.main import bot as admin_bot

app = Flask(__name__)

@app.route("/")
def index():
    return "SaaS Multi-Tenant Omnichannel Platform Layer: ACTIVE ✅", 200

# --- 🚀 BEST PRACTICE: SMART FILTER UNIFIED WEBHOOK WITH DEBUG LOGS ---
@app.route("/webhook", methods=['POST'])
def unified_webhook():
    content_type = request.headers.get("content-type", "")
    
    if "application/json" in content_type:
        json_string = request.get_data().decode('utf-8')
        
        # 🔍 Debug Log: Telegram ကနေ Request ဝင်လာသမျှကို ကြည့်ရန်
        update_dict = json.loads(json_string)
        print(f"🔥 INCOMING SaaS UPDATE: {json.dumps(update_dict, indent=2)}")
        
        update = telebot.types.Update.de_json(json_string)
        
        # Smart Filtering စနစ်အတွက် Chat ID ရှာဖွေခြင်း
        chat_id = None
        if update.message: chat_id = update.message.chat.id
        elif update.callback_query and update.callback_query.message:
            chat_id = update.callback_query.message.chat.id
            
        # Super Admin IDs စာရင်းဝင် ဟုတ်မဟုတ် စစ်ဆေးခြင်း
        admin_env = os.getenv('ADMIN_IDS', '')
        SUPER_ADMIN_IDS = [int(x) for x in admin_env.split(',') if x.strip().isdigit()]
        
        if chat_id and chat_id in SUPER_ADMIN_IDS:
            try:
                print(f"⚙️ Dispatching update to Admin Bot for Admin User ID: {chat_id}")
                admin_bot.process_new_updates([update])
            except Exception as e:
                print(f"⚠️ Admin Bot Dispatcher Error: {e}")
        else:
            try:
                print(f"🛒 Dispatching update to Main Bot for User ID: {chat_id}")
                main_bot.process_new_updates([update])
            except Exception as e:
                print(f"⚠️ Main Bot Dispatcher Error: {e}")
                
        return "!", 200
    else:
        return "Invalid Content-Type", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
