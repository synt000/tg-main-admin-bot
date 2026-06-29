import os
import sys
import telebot
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.database import get_db_connection

load_dotenv()

# WebApp ပွင့်မည့် သတ်မှတ်ချက် URL (SaaS Engine Frontend Link)
TMA_FRONTEND_URL = os.getenv('TMA_FRONTEND_URL', 'https://onrender.com')

# ⚠️ Whitelabel Engine ဖြစ်သောကြောင့် Token အား Router မှ Dynamic ဖြည့်ပေးမည်ဖြစ်သော်လည်း
# Handler ကြေညာချက်များ အဆင်ပြေစေရန် အခြေခံ Instance ဆောက်ထားခြင်းဖြစ်သည်
bot = telebot.TeleBot(os.getenv('BOT_TOKEN', 'DUMMY_TOKEN'), threaded=False)

# --- 🛍️ CHATBOT INLINE BUTTONS (ဝယ်သူများ ဆိုင်ထဲသို့ဝင်မည့် ပင်မစာမျက်နှာ) ---
@bot.message_handler(commands=['start'])
def customer_start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    
    # ဝယ်သူအား ဗဟို Database ထဲသို့ သိမ်းဆည်းခြင်း (Checkout Memory အတွက်)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (telegram_id, username, full_name)
        VALUES (%s, %s, %s)
        ON CONFLICT (telegram_id) DO NOTHING;
    ''', (user_id, username, full_name))
    conn.commit()
    cursor.close()
    conn.close()
    
    # Prompt ထဲမှ တောင်းဆိုထားသည့်အတိုင်း လှပသော Inline ခလုတ်များ ဖန်တီးခြင်း
    markup = telebot.types.InlineKeyboardMarkup()
    
    # Telegram Mini App (TMA) သို့ တိုက်ရိုက်ဝင်မည့် WebApp Button
    web_app_info = telebot.types.WebAppInfo(url=TMA_FRONTEND_URL)
    btn_shop = telebot.types.InlineKeyboardButton("🛍️ ဆိုင်သို့ဝင်ရန် (Web App)", web_app_info=web_app_info)
    
    btn_history = telebot.types.InlineKeyboardButton("📦 မှာယူမှုမှတ်တမ်း", callback_data="cust_order_history")
    btn_support = telebot.types.InlineKeyboardButton("📞 ဆိုင်ရှင်နှင့်စကားပြောရန်", callback_data="cust_contact_owner")
    
    markup.add(btn_shop)
    markup.add(btn_history, btn_support)
    
    bot.reply_to(message, f"👋 မင်္ဂလာပါ {full_name}!\nကျွန်ုပ်တို့၏ ဘက်စုံသုံး Whitelabel စတိုးဆိုင်မှ ကြိုဆိုပါတယ်ဗျာ။\n\nအောက်ပါခလုတ်ကိုနှိပ်ပြီး ဈေးဝယ်ခြင်း၊ ရက်ချိန်း Booking တင်ခြင်းများကို Telegram ထဲမှာတင် Website တစ်ခုလိုမျိုး ခေတ်မီစွာ ပြုလုပ်နိုင်ပါပြီခင်ဗျာ။", reply_markup=markup)

# --- 📦 SMOOTH TRANSITION FLOW (ဝယ်သူ TMA ထဲတွင် ငွေချေပြီးလျှင် Bot ထဲသို့ ဒေတာဝင်လာမည့်စနစ်) ---
@bot.message_handler(content_types=['web_app_data'])
def handle_tma_checkout_data(message):
    user_id = message.from_user.id
    # Mini App ဘက်မှ tg.sendData() ဖြင့် ပို့လိုက်သော ဒေတာအား ဖတ်ခြင်း
    try:
        tma_data = json.loads(message.web_app_data.data)
        
        if tma_data.get("event") == "checkout_success":
            total_amount = tma_data.get("total_amount", 0)
            
            # ဒစ်ဂျစ်တယ် ဗောက်ချာအတွက် QR Code အား အလိုအလျောက် ထုတ်ပေးခြင်း (Digital Voucher Generator)
            voucher_code = f"VOUCHER-{user_id}-{message.message_id}"
            
            # စာသားချက်ချင်း ဝင်လာစေခြင်း
            bot.send_message(user_id, f"🎉 **မှာယူမှု အောင်မြင်ပါသည်ခင်ဗျာ!**\n\n💵 **စုစုပေါင်း ကျသင့်ငွေ:** {total_amount:,} MMK\n🎫 **သင်၏ ဒစ်ဂျစ်တယ် ပြေစာကုဒ်:** `{voucher_code}`\n\nလူကြီးမင်း မှာယူလိုက်သော ပစ္စည်းများကို ဆိုင်ရှင်မှ စစ်ဆေးပြီးပါက ပစ္စည်းများအား ချက်ချင်း ပို့ဆောင်ပေးသွားမည် ဖြစ်ပါသည်ဗျာ။")
    except Exception as e:
        print(f"⚠️ WebApp Data Parse Error: {e}")
