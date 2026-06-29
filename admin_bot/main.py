import os
import sys
import telebot
from dotenv import load_dotenv

# လမ်းကြောင်း ပြင်ဆင်ခြင်း
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.database import get_db_connection

load_dotenv()

# Token ကို စာသားထဲက အကြံပြုချက်အတိုင်း သေသေချာချာ ခေါ်ယူခြင်း
ADMIN_TOKEN = os.getenv('ADMIN_BOT_TOKEN')

# Threaded=False ပေးမှ Webhook နှင့် စနစ်တကျ အလုပ်လုပ်မည်ဖြစ်သည်
bot = telebot.TeleBot(ADMIN_TOKEN, threaded=False)

# အက်ဒမင် ID စစ်ဆေးခြင်းစနစ်
admin_env = os.getenv('ADMIN_IDS')
if admin_env:
    ADMIN_IDS = [int(x) for x in admin_env.split(',') if x.strip().isdigit()]
else:
    ADMIN_IDS = []

admin_states = {}

def is_admin(user_id):
    return user_id in ADMIN_IDS

# --- 🧪 TEST & DEBUG HANDLER (ဘယ်သူစာပို့ပို့ အလုပ်လုပ်၊ မလုပ် အရင်ဆုံး သိရမည့် Safe Handler) ---
@bot.message_handler(commands=['test'])
def handle_test(message):
    bot.reply_to(message, "⚙️ Admin Bot Response Test: WORKING PERFECTLY ✅")

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def admin_welcome(message):
    user_id = message.from_user.id
    
    # 🔍 Debug Print: အက်ဒမင် ID စစ်ဆေးမှုကို Log ထဲထုတ်ကြည့်ရန်
    print(f"👉 ADMIN BOT START CALLED BY USER: {user_id} (Is Admin? {is_admin(user_id)})")
    
    if not is_admin(user_id):
        bot.reply_to(message, f"❌ သင်သည် ဤစနစ်၏ Admin မဟုတ်ပါသဖြင့် အသုံးပြုခွင့်မရှိပါခင်ဗျာ။\n*(သင်၏ ID: `{user_id}` အား Admin IDs တွင် ထည့်သွင်းပေးရန် လိုအပ်ပါသည်)*", parse_mode="Markdown")
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

# --- PHOTO HANDLER ---
@bot.message_handler(content_types=['photo'], func=lambda message: message.from_user.id in admin_states and admin_states[message.from_user.id]['step'] == 'image')
def process_product_image(message):
    user_id = message.from_user.id
    state = admin_states[user_id]
    file_id = message.photo[-1].file_id
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, description, price, image_file_id, category)
        VALUES (%s, %s, %s, %s, %s);
    ''', (state['name'], state['desc'], state['price'], file_id, state['category']))
    conn.commit()
    cursor.close()
    conn.close()
    
    del admin_states[user_id]
    bot.reply_to(message, f"✅ **ပစ္စည်းအသစ် တင်ပြီးမြောက်ပါပြီ။**\n\nဝယ်သူများဘက်ခြမ်း Bot တွင် ယခုပစ္စည်းကို ချက်ချင်း ဝယ်ယူနိုင်ပါပြီခင်ဗျာ။")
