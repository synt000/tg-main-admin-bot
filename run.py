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

# ဘော့တ် Instance များကို Import လုပ်ခြင်း
from main_bot.main import bot as main_bot
from admin_bot.main import bot as admin_bot

app = Flask(__name__)

@app.route("/")
def home():
    return "E-Commerce Multi-Bot System Server is Running ✅", 200

# --- 🚀 RECOMMENDED CLEAN SETUP: SINGLE WEBHOOK ROUTE ---
# လမ်းကြောင်း တစ်ခုတည်းဖြင့် Main Bot ရော Admin Bot ကိုပါ အတူတူ ကိုင်တွယ်ခြင်း
@app.route("/webhook", methods=['POST'])
def unified_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update_dict = json.loads(json_string)
        
        # စစ်ဆေးရန် Debug Log
        print(f"🔥 UNIFIED UPDATE INCOMING: {json.dumps(update_dict, indent=2)}")
        update = telebot.types.Update.de_json(json_string)
        
        # 🔍 Token/Path ခွဲစရာမလိုဘဲ Bot နှစ်ခုလုံးဆီသို့ Update များ တစ်ပြိုင်နက် ပို့ပေးခြင်း
        # Library က ၎င်းနှင့်ဆိုင်သော Update ကိုသာ ဖတ်ပြီး အလုပ်လုပ်သွားပါမည်။ Conflict လုံးဝမဖြစ်ပါ။
        try:
            main_bot.process_new_updates([update])
            admin_bot.process_new_updates([update])
        except Exception as e:
            print(f"⚠️ Bot Process Update Error: {e}")
            
        return "!", 200
    else:
        return "Invalid Content-Type", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
