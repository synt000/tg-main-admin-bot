import sys
import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import telebot

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

# Startup မတိုင်မီ Database Table များကို ဆောက်ခြင်း
try:
    from core.database import init_saas_database
    init_saas_database()
    print("🛒 Central Database Synchronized!")
except Exception as e:
    print(f"⚠️ Database Auto-Sync Warning: {e}")

# Core Bot Logics များကို Router ထဲသို့ ခေါ်ယူခြင်း
from main_bot.main import bot as main_bot
from admin_bot.main import bot as admin_bot
from integrations.omnichannel import sync_external_order

app = Flask(__name__)

# --- 👑 HOME ROUTE ---
@app.route("/")
def index():
    return "SaaS Multi-Tenant Omnichannel Platform Layer: ACTIVE ✅", 200

# --- 🛠️ 1. WHIELABEL SELF-ONBOARDING API ---
@app.route("/api/onboard", methods=['POST'])
def onboard_tenant():
    data = request.json
    from core.database import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO tenants (owner_id, shop_name, business_type, bot_token)
            VALUES (%s, %s, %s, %s) RETURNING tenant_id;
        ''', (data['telegram_id'], data['shop_name'], data['business_type'], data['bot_token']))
        tenant_id = cursor.fetchone()['tenant_id']
        
        # Webhook အလိုအလျောက် သွားရောက်ချိတ်ဆက်ပေးခြင်း
        bot = telebot.TeleBot(data['bot_token'])
        webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL')}/webhook"
        bot.set_webhook(url=webhook_url)
        
        conn.commit()
        return jsonify({"status": "success", "tenant_id": tenant_id, "message": "Whitelabel Engine Activated!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# --- 📱 2. FACEBOOK & TIKTOK OMNICHANNEL INTEGRATION ENDPOINT ---
@app.route("/api/integrations/sync-order", methods=['POST'])
def external_platform_webhook():
    """
    Facebook / TikTok Shop ကဲ့သို့သော ပြင်ပပလက်ဖောင်းများမှ Webhook API ဒေတာများကို 
    ဗဟိုဆာဗာမှ လက်ခံရယူပြီး Omnichannel စနစ်သို့ လွှဲပြောင်းပေးသည့် API လမ်းကြောင်း ဖြစ်သည်။
    """
    data = request.json
    # လိုအပ်ချက်ဒေတာ format: tenant_id, platform, platform_order_id, customer_name, items, total_price
    tenant_id = data.get("tenant_id")
    platform = data.get("platform")
    platform_order_id = data.get("platform_order_id")
    customer_name = data.get("customer_name")
    items = data.get("items", [])
    total_price = data.get("total_price", 0)
    
    if not tenant_id or not platform or not platform_order_id:
        return jsonify({"status": "error", "message": "Missing required data fields"}), 400
        
    result = sync_external_order(tenant_id, platform, platform_order_id, customer_name, items, total_price)
    
    if result.get("status") == "success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

# --- 🚀 3. BEST PRACTICE: SMART FILTER UNIFIED WEBHOOK ---
@app.route("/webhook", methods=['POST'])
def unified_webhook():
    content_type = request.headers.get("content-type", "")
    
    if "application/json" in content_type:
        json_string = request.get_data().decode('utf-8')
        update_dict = json.loads(json_string)
        update = telebot.types.Update.de_json(json_string)
        
        # 🔍 SMART CHAT ID FILTERING (ဒုတိယအကြိမ် ပြဿနာများကို ဖြေရှင်းရန် စစ်ထုတ်စနစ်)
        chat_id = None
        if update.message: chat_id = update.message.chat.id
        elif update.callback_query and update.callback_query.message:
            chat_id = update.callback_query.message.chat.id
            
        print(f"🔥 UNIFIED WEBHOOK UPDATE INCOMING FOR CHAT: {chat_id}")
        
        # 🛡️ RACE CONDITION & DOUBLE REPLIES ကာကွယ်ရေးစနစ်
        # ၎င်း Update သည် Super Admin IDs စာရင်းဝင် ဟုတ်မဟုတ် စစ်ဆေးခြင်း
        admin_env = os.getenv('ADMIN_IDS', '')
        SUPER_ADMIN_IDS = [int(x) for x in admin_env.split(',') if x.strip().isdigit()]
        
        if chat_id and chat_id in SUPER_ADMIN_IDS:
            try:
                # အကယ်၍ အက်ဒမင် ID ဖြစ်ပါက Admin Bot Handler ဆီသို့သာ သီးသန့် မောင်းနှင်ပေးခြင်း
                admin_bot.process_new_updates([update])
            except Exception as e:
                print(f"⚠️ Admin Bot Dispatcher Error: {e}")
        else:
            try:
                # သာမန် User သို့မဟုတ် ဝယ်သူများဖြစ်ပါက Main Bot Handler ဆီသို့သာ စနစ်တကျ ပို့ဆောင်ပေးခြင်း
                main_bot.process_new_updates([update])
            except Exception as e:
                print(f"⚠️ Main Bot Dispatcher Error: {e}")
                
        return "!", 200
    else:
        return "Invalid Content-Type", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
