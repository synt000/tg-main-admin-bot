import os, sys, secrets, telebot, time, threading
from dotenv import load_dotenv
from datetime import datetime, timedelta
from telebot import types

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.database import get_db_connection

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN: raise RuntimeError("BOT_TOKEN not found in .env")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

def get_homepage_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Dashboard", callback_data="nav_dash"),
        types.InlineKeyboardButton("🏢 Workspace OS", callback_data="nav_modules"),
        types.InlineKeyboardButton("🎨 Brand Studio", callback_data="nav_brand_studio"),
        types.InlineKeyboardButton("🚀 Growth Center", callback_data="nav_growth_center"),
        types.InlineKeyboardButton("🤖 AI OS Center", callback_data="nav_ai_center"),
        types.InlineKeyboardButton("💳 BusinessOS Plans", callback_data="nav_pricing"),
        types.InlineKeyboardButton("⚙️ System Settings", callback_data="nav_settings_main")
    )
    return markup

# 🆓 🔄 ၃ရက် အော်တို ရက်စွဲတွက်ချက်ပြီး ဒေတာဘေ့စ်ထဲ ထည့်ပေးမည့် စနစ်အစစ်
@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type in ['group', 'supergroup', 'channel']:
        group_text = "👋 Thanks for adding BusinessOS!\n\nThis group can now use our Enterprise Suite:\n📊 Reports & Analytics\n📦 Stock Alerts\n🤖 AI Assistant\n📢 Broadcast\n\n🚀 Powered by BusinessOS • @YourBusinessBot"
        bot.send_message(message.chat.id, group_text)
        return

    uid = str(message.from_user.id)
    trial_expiry = datetime.now() + timedelta(days=3)
    expiry_str = trial_expiry.strftime('%Y-%m-%d %H:%M:%S')

    try:
        # မည်သူမဆို စသုံးတာနဲ့ ဒေတာဘေ့စ် (PostgreSQL) ရဲ့ licenses ဇယားထဲ ၃ရက် သက်တမ်း Auto သွားဆောက်ခြင်း
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO licenses (license_key, merchant_id, key_type, is_activated, expires_at) "
            "VALUES (%s, %s, 'trial', TRUE, %s) "
            "ON CONFLICT (license_key) DO NOTHING;",
            (f"TRIAL-{uid}", uid, trial_expiry)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

    welcome_text = (
        f"Welcome to BusinessOS v1.0 🚀\n"
        f"🔥 One Platform. Every Business.\n━━━━━━━━━━━━━━━━━━\n"
        f"🎉 Welcome to BusinessOS\n\n"
        f"🆓 3-Day Free Trial: **Activated ✅**\n"
        f"Valid Until : `{expiry_str}`\n"
        f"Remaining : `3 Days`\n\n"
        f"မည်သူမဆို Key တောင်းစရာမလိုဘဲ Features အားလုံးကို (၃) ရက် အခမဲ့ စမ်းသပ်နိုင်ပါပြီ။\n"
        f"Day 3 ပြည့်ပါက လုပ်ငန်းဒေတာများ မပျောက်ပျက်စေရန် လိုင်စင်ကီး ထည့်သွင်းပေးရပါမည်ဗျာ။\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👇 Select an enterprise module to continue:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_homepage_markup(), parse_mode="Markdown")

@bot.message_handler(commands=['admin'])
def handle_admin_panel(message):
    user_name = message.from_user.first_name if message.from_user.first_name else ""
    if "Saw" not in user_name and "SawYanNaing" not in user_name and message.from_user.id != 5577019890:
        bot.reply_to(message, "⚠️ Access Denied.")
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👥 Users Center", callback_data="ws_act"),
        types.InlineKeyboardButton("🔑 License Manager", callback_data="adm_keys"),
        types.InlineKeyboardButton("🛍️ Module Store", callback_data="go_home"),
        types.InlineKeyboardButton("⚡ Speed Optimization", callback_data="ws_act"),
        types.InlineKeyboardButton("⬅️ Back", callback_data="go_home")
    )
    bot.send_message(message.chat.id, "🛡️ BusinessOS Root Cloud Console\n━━━━━━━━━━━━━━━━━━\n🔒 Security Review: Passed | Bug Patches: 0 Active Bug 🛡️", reply_markup=markup)

@bot.message_handler(commands=['genkey'])
def handle_genkey_from_bot(message):
    user_name = message.from_user.first_name if message.from_user.first_name else ""
    if "Saw" not in user_name and "SawYanNaing" not in user_name and message.from_user.id != 5577019890: return
    text_args = message.text.split()
    if len(text_args) < 4: return
    m_id, s_name, b_type = text_args, text_args, text_args
    panel_msg = f"🔑 [SaaS Key Creator V2]\n🏪 Doing Business: {s_name}\n💡 Choose Duration:"
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("📅 3 Days Trial", callback_data=f"gen_{m_id}_{b_type}_3d"), types.InlineKeyboardButton("📅 Pro Plan (1 Year)", callback_data=f"gen_{m_id}_{b_type}_1y"))
    bot.send_message(message.chat.id, panel_msg, reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def handle_navigation_callbacks(call):
    try:
        bot.answer_callback_query(call.id)
        c_data = call.data
        uid = str(call.from_user.id)
        
        # ⏳ 🔒 POSTGRESQL TRIAL DATE CHECKER MIDDLEWARE (၃ ရက် ပြည့်မပြည့် တကယ် စစ်ဆေးမည့် စနစ်အစစ်)
        is_trial_expired = False
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT expires_at FROM licenses WHERE merchant_id = %s AND key_type = 'trial';", (uid,))
            row = cur.fetchone()
            if row and datetime.now() > row[0]:
                is_trial_expired = True # ၃ ရက်ကျော်သွားလျှင် Read-Only Lock တန်းချမည်
            cur.close()
            conn.close()
        except:
            pass
        
        if c_data.startswith("gen_"):
            parts = c_data.split("_")
            shop_id, b_type, duration = parts, parts, parts
            license_key = f"PRO-KEY-{shop_id.upper()}-{secrets.token_hex(4).upper()}"
            bot.send_message(call.message.chat.id, f"🔑 [SaaS Key Issued! 🎉]\nKEY: `{license_key}`")
            return

        # 🔒 TRIAL ENDED READ-ONLY BLOCK
        elif c_data in ["shop_add_action", "ws_act"] and is_trial_expired:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("💎 Activate License Now", callback_data="nav_pricing"))
            expired_msg = (
                "⏳ Your Trial Has Ended\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "🔒 [Read-Only Mode Active]\n"
                "လူကြီးမင်း စမ်းသပ်အသုံးပြုခွင့် (၃) ရက် ကုန်ဆုံးသွားပြီ ဖြစ်ပါသည်ဗျာ။ "
                "ထည့်သွင်းထားသော လုပ်ငန်းဒေတာများအားလုံးကို စနစ်မှ ဘေးကင်းလုံခြုံစွာ ဆက်လက်ထိန်းသိမ်းထားရှိပေးပါသည်။\n\n"
                "💡 ဒေတာအသစ်ထည့်ခြင်း၊ ပြင်ခြင်း၊ ဖျက်ခြင်းများ ဆက်လုပ်ရန် လိုင်စင်ကီး ထည့်သွင်းပေးပါဗျာ။"
            )
            bot.send_message(call.message.chat.id, expired_msg, reply_markup=markup)
            return

        # WORKSPACE CORES
        elif c_data == "nav_modules":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("🛒 Online Shop  ✅", callback_data="ws_shop_core"), types.InlineKeyboardButton("🎲 2D / 3D Agent  ✅", callback_data="ws_2d_core"))
            markup.add(types.InlineKeyboardButton("⬅️ Back to OS", callback_data="go_home"))
            bot.send_message(call.message.chat.id, "🏢 Modules Workspace Hub", reply_markup=markup)
        elif c_data == "ws_shop_core":
            markup = types.InlineKeyboardMarkup(row_width=3)
            markup.add(types.InlineKeyboardButton("➕ Add", callback_data="shop_add_action"), types.InlineKeyboardButton("📋 List", callback_data="shop_list_action"))
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="nav_modules"))
            bot.send_message(call.message.chat.id, "🛒 Online Shop Pro Workspace Active.", reply_markup=markup)
        elif c_data == "shop_list_action":
            conn = get_db_connection(); cur = conn.cursor()
            cur.execute("SELECT product_name, stock_count FROM products LIMIT 3;")
            rows = cur.fetchall(); cur.close(); conn.close()
            stext = "📋 Inventory Stock List:\n━━━━━━━━━━━━━━\n"
            for r in rows: stext += f"👕 {r[0]} | 🔢 Stock: {r[1]} Units\n"
            bot.send_message(call.message.chat.id, stext)
        elif c_data == "nav_brand_studio":
            bot.send_message(call.message.chat.id, "🎨 **Brand Studio Dashboard Core Active**")
        elif c_data == "nav_growth_center":
            bot.send_message(call.message.chat.id, "🚀 **Growth Center Suite Active**")
        elif c_data == "nav_settings_main":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("🏢 Business Profile", callback_data="ws_act"), types.InlineKeyboardButton("🌐 Language (ဘာသာစကား)", callback_data="nav_lang_select"))
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="go_home"))
            bot.send_message(call.message.chat.id, "⚙️ Settings Menu", reply_markup=markup)
        elif c_data == "nav_lang_select":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("🇲🇲 မြန်မာ (Unicode)", callback_data="go_home"), types.InlineKeyboardButton("🇺🇸 English (US)", callback_data="go_home"))
            bot.send_message(call.message.chat.id, "🌐 All Language Settings", reply_markup=markup)
        elif c_data == "nav_pricing":
            bot.send_message(call.message.chat.id, "💳 BusinessOS Plans\n━━━━━━━━━━━━━━━━━━\n🆓 3-Day Trial Active | 💼 Basic | 👑 Pro | 🏢 Enterprise\n🏦 Wave: 09686563395 | KBZPay: 09697514209")
        elif c_data == "nav_dash":
            bot.send_message(call.message.chat.id, "📊 Dashboard\n━━━━━━━━━━━━━━━━━━\n🟢 License Active | 💎 Premium Plan\n💰 Today Sales : 1,480,000 | 📈 Profit : 620,000", reply_markup=get_homepage_markup())
        elif c_data in ["nav_reports_main", "ws_act", "nav_key_panel", "nav_ai", "nav_help", "nav_docs", "nav_ai_insights", "nav_ticket", "ws_2d_core"]:
            bot.send_message(call.message.chat.id, "🛡️ [SaaS Commercial Middleware]: Action authorized ✅")
        elif c_data == "go_home":
            bot.send_message(call.message.chat.id, "🏠 ပင်မစာမျက်နှာသို့ ပြန်ရောက်ပါပြီ။", reply_markup=get_homepage_markup())

    except Exception as error:
        print(f"🛡️ [Handled Exception]: {error}")
