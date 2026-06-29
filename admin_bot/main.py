import os
import telebot
from flask import Flask, request
from dotenv import load_dotenv
from core.database import get_db_connection

load_dotenv()

ADMIN_TOKEN = os.getenv('ADMIN_BOT_TOKEN') # အက်ဒမင်ဘော့အတွက် သီးသန့်တိုကင်
RENDER_URL = os.getenv('RENDER_EXTERNAL_URL')

bot = telebot.TeleBot(ADMIN_TOKEN, threaded=False)
app = Flask(__name__)

# အက်ဒမင်ဖြစ်ကြောင်း စစ်ဆေးရန် (မိုင်ခရိုဆော့ဖ် သို့မဟုတ် env ထဲက ID စစ်နိုင်သည်)
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x]

# စာရိုက်ဆင့်ကဲစနစ် (FSM) အတွက် ယာယီဒေတာသိမ်းရန်
admin_states = {}

def is_admin(user_id):
    return user_id in ADMIN_IDS

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def admin_welcome(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        bot.reply_to(message, "❌ သင်သည် ဤစနစ်၏ Admin မဟုတ်ပါသဖြင့် အသုံးပြုခွင့်မရှိပါခင်ဗျာ။")
        return
        
    markup = telebot.types.InlineKeyboardMarkup()
    btn_add_prod = telebot.types.InlineKeyboardButton("📦 ပစ္စည်းအသစ်တင်ရန်", callback_data="admin_add_product")
    btn_orders = telebot.types.InlineKeyboardButton("📋 အော်ဒါများ စစ်ဆေးရန်", callback_data="admin_view_orders")
    
    markup.add(btn_add_prod)
    markup.add(btn_orders)
    
    bot.reply_to(message, "⚙️ **အက်ဒမင် စီမံခန့်ခွဲရေးစနစ်မှ ကြိုဆိုပါသည်**\n\nလုပ်ဆောင်လိုသော အလုပ်ကို အောက်ပါခလုတ်တွင် ရွေးချယ်ပေးပါဗျာ။", reply_markup=markup, parse_mode="Markdown")

# --- CALLBACK QUERY HANDLERS ---
@bot.callback_query_handler(func=lambda call: True)
def admin_callbacks(call):
    user_id = call.from_user.id
    if not is_admin(user_id): return
    
    if call.data == "admin_add_product":
        # အဆင့် (၁) - Category ရွေးခိုင်းခြင်း
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("📱 Digital Accounts", callback_data="setcat_Digital"))
        markup.add(telebot.types.InlineKeyboardButton("👕 အဝတ်အထည်နှင့် ဖက်ရှင်", callback_data="setcat_Clothes"))
        markup.add(telebot.types.InlineKeyboardButton("📦 အထွေထွေသုံး လူသုံးကုန်", callback_data="setcat_General"))
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="🏷️ **ပစ္စည်းတင်မည့် အမျိုးအစားကို ရွေးချယ်ပါ:**", reply_markup=markup)
                              
    elif call.data.startswith("setcat_"):
        category = call.data.split("_")[1]
        admin_states[user_id] = {'category': category, 'step': 'name'}
        
        bot.send_message(user_id, f"📝 အမျိုးအစား: {category}\n\n**ပစ္စည်းအမည် (Product Name)** ကို ရိုက်ပို့ပေးပါဗျာ:")

# --- TEXT MESSAGE HANDLERS FOR ADDING PRODUCT ---
@bot.message_handler(func=lambda message: message.from_user.id in admin_states)
def process_product_adding(message):
    user_id = message.from_user.id
    state = admin_states[user_id]
    
    if state['step'] == 'name':
        state['name'] = message.text
        state['step'] = 'desc'
        bot.reply_to(message, "📝 **ပစ္စည်းအကြောင်းအရာ အကျဉ်း (Description)** ကို ရိုက်ပို့ပေးပါဗျာ:")
        
    elif state['step'] == 'desc':
        state['desc'] = message.text
        state['step'] = 'price'
        bot.reply_to(message, "💰 **ပစ္စည်းစျေးနှုန်း (Price in MMK)** ကို နံပါတ်သက်သက်ပဲ ရိုက်ပို့ပေးပါဗျာ:")
        
    elif state['step'] == 'price':
        try:
            price = float(message.text)
            state['price'] = price
            state['step'] = 'image'
            bot.reply_to(message, "🖼️ နောက်ဆုံးအဆင့်အနေနဲ့ **ပစ္စည်းဓာတ်ပုံ (Product Image)** ကို ပို့ပေးပါဗျာ:")
        except ValueError:
            bot.reply_to(message, "❌ ကျေးဇူးပြု၍ စျေးနှုန်းကို ဂဏန်းနံပါတ် သီးသန့်သာ ရိုက်ပေးပါဗျာ:")

# --- PHOTO HANDLER FOR PRODUCT IMAGE ---
@bot.message_handler(content_types=['photo'], func=lambda message: message.from_user.id in admin_states and admin_states[message.from_user.id]['step'] == 'image')
def process_product_image(message):
    user_id = message.from_user.id
    state = admin_states[user_id]
    
    # Telegram ပေါ်က အကြည်ဆုံးပုံ ID ကို ယူခြင်း
    file_id = message.photo[-1].file_id
    
    # Database ထဲသို့ ပစ္စည်းအချက်အလက်များ သိမ်းဆည်းခြင်း
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, description, price, image_file_id, category)
        VALUES (%s, %s, %s, %s, %s);
    ''', (state['name'], state['desc'], state['price'], file_id, state['category']))
    conn.commit()
    cursor.close()
    conn.close()
    
    # State ကို ပိတ်သိမ်းခြင်း
    del admin_states[user_id]
    
    bot.reply_to(message, f"✅ **ပစ္စည်းအသစ် တင်ပြီးမြောက်ပါပြီ။**\n\nဝယ်သူများဘက်ခြမ်း Bot တွင် ယခုပစ္စည်းကို ချက်ချင်း ဝယ်ယူနိုင်ပါပြီခင်ဗျာ။")

# --- WEBHOOK SERVER ROUTING ---
@app.route('/' + ADMIN_TOKEN, methods=['POST'])
def getAdminMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def admin_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + '/' + ADMIN_TOKEN)
    return "Admin Bot Webhook Status: ACTIVE", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001)) # ကွဲပြားသော Port တစ်ခုခုဖြင့် Run မည်
    app.run(host="0.0.0.0", port=port)
