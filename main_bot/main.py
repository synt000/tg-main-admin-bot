import os
import sys
import telebot
from flask import Flask, request
from dotenv import load_dotenv

# Parent Directory (ပင်မ Folder) ကို လမ်းကြောင်းထဲ ထည့်သွင်းခြင်း
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.database import get_db_connection

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
RENDER_URL = os.getenv('RENDER_EXTERNAL_URL')
BOT_USERNAME = os.getenv('BOT_USERNAME')

bot = telebot.TeleBot(API_TOKEN, threaded=False)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    
    referred_by = None
    command_args = message.text.split()
    if len(command_args) > 1:
        try:
            possible_referrer = int(command_args[1])
            if possible_referrer != user_id:
                referred_by = possible_referrer
        except ValueError:
            pass

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, username, full_name) 
        VALUES (%s, %s, %s) 
        ON CONFLICT (user_id) DO NOTHING;
    ''', (user_id, username, full_name))
    conn.commit()
    cursor.close()
    conn.close()
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn_shop = telebot.types.InlineKeyboardButton("🛒 ပစ္စည်းများကြည့်ရန်", callback_data="view_shop")
    btn_agent = telebot.types.InlineKeyboardButton("💰 ကူရောင်းပြီး ပိုက်ဆံရှာရန်", callback_data="agent_panel")
    btn_wallet = telebot.types.InlineKeyboardButton("💳 ကျွန်ုပ်၏ Wallet", callback_data="my_wallet")
    
    markup.add(btn_shop)
    markup.add(btn_agent, btn_wallet)
    
    bot.reply_to(message, f"👋 မင်္ဂလာပါ {full_name}!\nဘက်စုံသုံး Online Store မှ ကြိုဆိုပါတယ်။\n\nပစ္စည်းများကို စျေးနှုန်းချိုသာစွာဖြင့် ဝယ်ယူနိုင်သလို၊ သူငယ်ချင်းများကို လင့်ခ်မျှဝေပြီး ကော်မရှင်ခ (Affiliate Bonus) ရှာဖွေနိုင်ပါတယ်ဗျာ။", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.from_user.id
    
    if call.data == "view_shop":
        markup = telebot.types.InlineKeyboardMarkup()
        btn_digital = telebot.types.InlineKeyboardButton("📱 Digital Accounts / Software", callback_data="cat_Digital")
        btn_clothes = telebot.types.InlineKeyboardButton("👕 အဝတ်အထည်နှင့် ဖက်ရှင်", callback_data="cat_Clothes")
        btn_general = telebot.types.InlineKeyboardButton("📦 အထွေထွေသုံး လူသုံးကုန်", callback_data="cat_General")
        btn_back = telebot.types.InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
        markup.add(btn_digital)
        markup.add(btn_clothes)
        markup.add(btn_general)
        markup.add(btn_back)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="🛍️ **ပစ္စည်းအမျိုးအစားများ**\n\nသင်ကြည့်ရှုလိုသော အမျိုးအစားကို အောက်ပါခလုတ်များတွင် ရွေးချယ်ပေးပါဗျာ။", 
                              parse_mode="Markdown", reply_markup=markup)
                              
    elif call.data.startswith("cat_"):
        category_name = call.data.split("_")[1]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE category = %s AND stock > 0;", (category_name,))
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not products:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton("🔙 နောက်သို့", callback_data="view_shop"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"❌ လက်ရှိတွင် *{category_name}* အမျိုးအစားထဲ၌ ရောင်းရန်ပစ္စည်း မရှိသေးပါခင်ဗျာ။", 
                                  parse_mode="Markdown", reply_markup=markup)
            return
            
        bot.answer_callback_query(call.id, text=f"{category_name} ပစ္စည်းစာရင်းကို ရှာဖွေနေပါသည်...")

    elif call.data == "agent_panel":
        referral_link = f"https://t.me{BOT_USERNAME}?start={user_id}"
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT commission_earned FROM users WHERE user_id = %s;", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        commission = user_data['commission_earned'] if user_data else 0.0
        
        markup = telebot.types.InlineKeyboardMarkup()
        btn_back = telebot.types.InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
        markup.add(btn_back)
        
        agent_text = (
            f"💰 **Agent ကူရောင်းရေး ပန်နယ်လ်**\n\n"
            f"လူကြီးမင်းအနေဖြင့် အောက်ပါ ကိုယ်ပိုင် Referral Link ကို အသုံးပြုပြီး "
            f"ဒီမိတ်ဆွေတိုးပွားရေးလင့်ခ်မှတစ်ဆင့် လူသစ်များကို ဖိတ်ခေါ်ကာ ကော်မရှင်ခများ ရယူနိုင်ပါတယ်ဗျာ။\n\n"
            f"🔗 **သင်၏ ဖိတ်ခေါ်စာလင့်ခ်:**\n`{referral_link}`\n\n"
            f"💵 **စုစုပေါင်းရရှိပြီးသော ကော်မရှင်ခ:** {commission} MMK\n\n"
            f"*(လင့်ခ်ကို တစ်ချက်နှိပ်ရုံဖြင့် အလွယ်တကူ Copy ကူးယူနိုင်ပါသည်)*"
        )
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=agent_text, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "my_wallet":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = %s;", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        balance = user_data['balance'] if user_data else 0.0
        
        markup = telebot.types.InlineKeyboardMarkup()
        btn_deposit = telebot.types.InlineKeyboardButton("💳 Ngwe Phyi Yan", callback_data="deposit_money")
        btn_back = telebot.types.InlineKeyboardButton("🔙 ပင်မမီနူးသို့", callback_data="back_to_main")
        markup.add(btn_deposit)
        markup.add(btn_back)
        
        wallet_text = (
            f"💳 **ကျွန်ုပ်၏ Wallet စာမျက်နှာ**\n\n"
            f"💵 **လက်ရှိ လက်ကျန်ငွေ:** {balance} MMK\n\n"
            f"ပစ္စည်းများ ဝယ်ယူရန်အတွက် Wallet ထဲသို့ ကြိုတင်ငွေ ဖြည့်သွင်းထားနိုင်ပါတယ်ခင်ဗျာ။"
        )
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=wallet_text, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "deposit_money":
        bot.answer_callback_query(call.id, text="ငွေဖြည့်စနစ်ကို Admin Control ဆောက်ပြီးလျှင် ထည့်သွင်းပေးပါမည်။")

    elif call.data == "back_to_main":
        markup = telebot.types.InlineKeyboardMarkup()
        btn_shop = telebot.types.InlineKeyboardButton("🛒 ပစ္စည်းများကြည့်ရန်", callback_data="view_shop")
        btn_agent = telebot.types.InlineKeyboardButton("💰 ကူရောင်းပြီး ပိုက်ဆံရှာရန်", callback_data="agent_panel")
        btn_wallet = telebot.types.InlineKeyboardButton("💳 ကျွန်ုပ်၏ Wallet", callback_data="my_wallet")
        markup.add(btn_shop)
        markup.add(btn_agent, btn_wallet)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=f"👋 ပင်မစာမျက်နှာသို့ ပြန်ရောက်ပါပြီ။\n\nပစ္စည်းများကို စျေးနှုန်းချိုသာစွာဖြင့် ဝယ်ယူနိုင်သလို၊ သူငယ်ချင်းများကို လင့်ခ်မျှဝေပြီး ကော်မရှင်ခ ရှာဖွေနိုင်ပါတယ်ဗျာ။", 
                              reply_markup=markup)

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + '/' + API_TOKEN)
    return "Bot Webhook Status: ACTIVE", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
