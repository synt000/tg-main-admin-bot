import os
import sys
import telebot
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.database import get_db_connection

load_dotenv()

# Super Admin အတွက် သီးသန့် တိုကင်
ADMIN_TOKEN = os.getenv('ADMIN_BOT_TOKEN')
bot = telebot.TeleBot(ADMIN_TOKEN, threaded=False)

# Env ထဲမှ Super Admin ID များကို စာရင်းအဖြစ် ဖတ်ယူခြင်း
admin_env = os.getenv('ADMIN_IDS', '')
SUPER_ADMIN_IDS = [int(x) for x in admin_env.split(',') if x.strip().isdigit()]

def is_super_admin(user_id):
    return user_id in SUPER_ADMIN_IDS

# --- 👑 SUPER ADMIN START MENU ---
@bot.message_handler(commands=['start'])
def super_admin_start(message):
    user_id = message.from_user.id
    if not is_super_admin(user_id):
        bot.reply_to(message, "❌ သင်သည် စနစ်တစ်ခုလုံး၏ Super Admin မဟုတ်ပါသဖြင့် အသုံးပြုခွင့်မရှိပါ။")
        return
        
    markup = telebot.types.InlineKeyboardMarkup()
    btn_tenants = telebot.types.InlineKeyboardButton("🏬 ဆိုင်ရှင်များအား စီမံရန်", callback_data="sa_manage_tenants")
    btn_broadcast = telebot.types.InlineKeyboardButton("📢 ဆိုင်ရှင်အားလုံးဆီ စာပို့ရန်", callback_data="sa_broadcast")
    
    markup.add(btn_tenants)
    markup.add(btn_broadcast)
    
    bot.send_message(user_id, "⚙️ **SaaS Super Admin Control Center**\n\nစနစ်တစ်ခုလုံးရှိ ဆိုင်ရှင်များအား ထိန်းချုပ်ရန်နှင့် သတင်းထုတ်ပြန်ရန် ရွေးချယ်ပါဗျာ။", reply_markup=markup, parse_mode="Markdown")

# --- 📈 /report COMMAND (စာရင်းဇယားနှင့် လစဉ်ကြေးစာရင်းများ ထုတ်ပေးခြင်း) ---
@bot.message_handler(commands=['report'])
def generate_saas_report(message):
    user_id = message.from_user.id
    if not is_super_admin(user_id): return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # ဆိုင်အားလုံး၏ စုစုပေါင်း ရောင်းရငွေ (TMA Orders) နှင့် လစဉ်ကြေးရရှိမှု စုစုပေါင်းအား တွက်ချက်ခြင်း
    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total_sales FROM orders WHERE payment_status = 'verified';")
    total_sales = cursor.fetchone()['total_sales']
    
    cursor.execute("SELECT COALESCE(SUM(amount_paid), 0) as total_subs FROM subscription_logs;")
    total_subs = cursor.fetchone()['total_subs']
    
    cursor.execute("SELECT COUNT(*) as active_shops FROM tenants WHERE subscription_status = 'active';")
    active_shops = cursor.fetchone()['active_shops']
    
    cursor.close()
    conn.close()
    
    report_text = (
        f"📊 **SaaS System Platform Report**\n\n"
        f"🏬 လက်ရှိလည်ပတ်နေသော ဆိုင်စုစုပေါင်း: {active_shops} ဆိုင်\n"
        f"💳 စနစ်တစ်ခုလုံး၏ စုစုပေါင်းရောင်းရငွေ: {total_sales:,} MMK\n"
        f"💵 Super Admin ရရှိထားသော လစဉ်ကြေးစုစုပေါင်း: {total_subs:,} MMK\n\n"
        f"*(ဒေတာများကို ဗဟို PostgreSQL Database မှ Real-time တွက်ချက်ထားခြင်းဖြစ်သည်)*"
    )
    bot.send_message(user_id, report_text, parse_mode="Markdown")

# --- 🎯 INLINE BUTTONS ACTIONS (ခလုတ်များ နှိပ်လျှင် အလုပ်လုပ်မည့်စနစ်) ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("sa_"))
def super_admin_callbacks(call):
    user_id = call.from_user.id
    if not is_super_admin(user_id): return
    
    if call.data == "sa_manage_tenants":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tenant_id, shop_name, subscription_status FROM tenants LIMIT 10;")
        tenants = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not tenants:
            bot.answer_callback_query(call.id, text="လက်ရှိတွင် ငှားရမ်းထားသော ဆိုင်ရှင်မရှိသေးပါ။")
            return
            
        markup = telebot.types.InlineKeyboardMarkup()
        for t in tenants:
            status_icon = "✅" if t['subscription_status'] == 'active' else "❌"
            # ခလုတ်နှိပ်လျှင် သက်ဆိုင်ရာဆိုင်ကို Suspend သို့မဟုတ် Activate လုပ်ရန် စီစဉ်ခြင်း
            action_data = f"sa_toggle_{t['tenant_id']}"
            markup.add(telebot.types.InlineKeyboardButton(f"{status_icon} {t['shop_name']}", callback_data=action_data))
            
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, 
                              text="🏬 **ငှားရမ်းထားသော ဆိုင်များစာရင်း**\n\nဆိုင်အား ခေတ္တပိတ်သိမ်းရန် (Suspend) သို့မဟုတ် ပြန်ဖွင့်ရန် သက်ဆိုင်ရာဆိုင်ခလုတ်ကို နှိပ်ပါဗျာ။", 
                              reply_markup=markup)
                              
    elif call.data.startswith("sa_toggle_"):
        tenant_id = int(call.data.split("_")[2])
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # ဆိုင်၏ လက်ရှိအခြေအနေကို စစ်ပြီး ပြောင်းပြန်လှန်ခြင်း (Active <-> Suspended)
        cursor.execute("SELECT subscription_status FROM tenants WHERE tenant_id = %s;", (tenant_id,))
        current_status = cursor.fetchone()['subscription_status']
        new_status = 'suspended' if current_status == 'active' else 'active'
        
        cursor.execute("UPDATE tenants SET subscription_status = %s WHERE tenant_id = %s;", (new_status, tenant_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        bot.answer_callback_query(call.id, text=f"ဆိုင်အခြေအနေအား {new_status.upper()} သို့ ပြောင်းလဲလိုက်ပါပြီ။")
        # မီနူးအား Refresh ပြန်လုပ်ခြင်း
        super_admin_start(call.message)

    elif call.data == "sa_broadcast":
        # Global Broadcast စနစ်အတွက် စာရိုက်ရန် အချက်ပေးခြင်း
        msg = bot.send_message(user_id, "📢 **Global Broadcast System**\n\nဆိုင်ရှင်အားလုံးဆီ တစ်ပြိုင်နက် ပို့ချင်တဲ့ 'စနစ် Update သတင်းစကား' ကို ရိုက်ပို့ပေးပါဗျာ:")
        bot.register_next_step_handler(msg, process_global_broadcast)

def process_global_broadcast(message):
    user_id = message.from_user.id
    broadcast_text = message.text
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT owner_id FROM tenants;")
    owners = cursor.fetchall()
    cursor.close()
    conn.close()
    
    success_count = 0
    for owner in owners:
        try:
            # ဆိုင်ရှင်တစ်ဦးချင်းစီ၏ Telegram ဆီသို့ Message လှမ်းပို့ခြင်း
            bot.send_message(owner['owner_id'], f"🚨 **SaaS Platform Update Notification**\n\n{broadcast_text}")
            success_count += 1
        except Exception:
            pass
            
    bot.send_message(user_id, f"✅ Broadcast ပြီးမြောက်ပါပြီ။ ဆိုင်ရှင်စုစုပေါင်း {success_count} ဦးထံသို့ အောင်မြင်စွာ ပို့ဆောင်ပြီးပါပြီ။")
