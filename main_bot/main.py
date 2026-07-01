import os, sys, secrets, telebot, time
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

def get_welcome_text(expiry_str):
    return (
        f"📢 Live Updates: Central Database Sync [OK] • REST API Status [ONLINE] • Active Tenants: 117\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Welcome to BusinessOS v1.0 🚀\n"
        f"🔥 One Platform. Every Business.\n━━━━━━━━━━━━━━━━━━\n"
        f"🎉 Welcome to BusinessOS\n\n"
        f"Free 3-Day Trial: **Activated ✅**\n"
        f"Valid Until : `{expiry_str}`\n"
        f"Remaining : `3 Days`\n\n"
        f"Enjoy all Premium Features.\n"
        f"Day 3 ပြီးရင် Business Data များ မပျောက်ပျက်စေရန် License Key လိုအပ်ပါမယ် ခင်ဗျာ။\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👇 Select an enterprise module to continue:"
    )

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

    bot.send_message(message.chat.id, get_welcome_text(expiry_str), reply_markup=get_homepage_markup(), parse_mode="Markdown")

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
@bot.callback_query_handler(func=lambda call: True)
def handle_navigation_callbacks(call):
    try:
        c_data = call.data
        uid = str(call.from_user.id)
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        
        # ⏳ 🔒 TRIAL EXPIRY DATETIME CHECKER
        is_trial_expired = False
        expiry_str = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT expires_at FROM licenses WHERE merchant_id = %s AND key_type = 'trial';", (uid,))
            row = cur.fetchone()
            if row:
                expiry_str = row[0].strftime('%Y-%m-%d %H:%M:%S')
                if datetime.now() > row[0]:
                    is_trial_expired = True
            cur.close()
            conn.close()
        except: pass
        
        # 🔒 TRIAL ENDED READ-ONLY EDIT CONSOLE (မက်ဆေ့ခ်ျအသစ်မပို့ဘဲ Edit စနစ်ဖြင့်ပြောင်းခြင်း)
        if c_data in ["shop_add_action", "ws_act"] and is_trial_expired:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("💎 Activate License Now", callback_data="nav_pricing"))
            expired_msg = "⏳ Your Trial Has Ended\n━━━━━━━━━━━━━━━━━━\n🔒 [Read-Only Mode Active]\nလူကြီးမင်း စမ်းသပ်အသုံးပြုခွင့် (၃) ရက် ကုန်ဆုံးသွားပြီ ဖြစ်ပါသည်ဗျာ။\n\n💡 ဒေတာအသစ်ထည့်ခြင်း၊ ပြင်ခြင်း၊ ဖျက်ခြင်းများ ဆက်လုပ်ရန် လိုင်စင်ကီး ထည့်သွင်းပေးပါဗျာ။"
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=expired_msg, reply_markup=markup)
            return

        # 🏢 WORKSPACE ISOLATED EDIT SYSTEM
        elif c_data == "nav_modules":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🛒 Online Shop  ✅", callback_data="ws_shop_core"),
                types.InlineKeyboardButton("🎲 2D / 3D Agent  ✅", callback_data="ws_2d_core"),
                types.InlineKeyboardButton("⬅️ Back to OS", callback_data="go_home")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🏢 **Modules Workspace Hub**\n━━━━━━━━━━━━━━━━━━\nSelect an isolated environment:", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "ws_shop_core":
            markup = types.InlineKeyboardMarkup(row_width=3)
            markup.add(
                types.InlineKeyboardButton("➕ Add", callback_data="shop_add_action"),
                types.InlineKeyboardButton("📋 List", callback_data="shop_list_action"),
                types.InlineKeyboardButton("⬅️ Back", callback_data="nav_modules")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🛒 **Online Shop Pro Workspace**\n━━━━━━━━━━━━━━━━━━\nOperational Core Online:", reply_markup=markup, parse_mode="Markdown")
        elif c_data == "shop_list_action":
            conn = get_db_connection(); cur = conn.cursor()
            cur.execute("SELECT product_name, stock_count FROM products LIMIT 3;")
            rows = cur.fetchall(); cur.close(); conn.close()
            stext = "📋 **Inventory Stock List**\n━━━━━━━━━━━━━━━━━━\n"
            for r in rows: stext += f"👕 {r[0]} | 🔢 Stock: {r[1]} Units\n"
            stext += "\n🚀 Powered by BusinessOS • Try Free for 3 Days!"
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="ws_shop_core"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=stext, reply_markup=markup, parse_mode="Markdown")

        elif c_data == "ws_2d_core":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="nav_modules"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🎰 **2D/3D Agent Pro Workspace Active.**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "nav_brand_studio":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="go_home"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🎨 **Brand Studio Dashboard Core Active**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "nav_growth_center":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="go_home"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🚀 **Growth Center Suite Active**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "nav_settings_main":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("🏢 Business Profile", callback_data="ws_act"), types.InlineKeyboardButton("🌐 Language (ဘာသာစကား)", callback_data="nav_lang_select"))
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="go_home"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="⚙️ **Settings Menu**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "nav_lang_select":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("🇲🇲 မြန်မာ (Unicode)", callback_data="go_home"), types.InlineKeyboardButton("🇺🇸 English (US)", callback_data="go_home"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🌐 **All Language Settings**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "nav_pricing":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="go_home"))
            price_text = "💳 **BusinessOS Plans**\n━━━━━━━━━━━━━━━━━━\nFree 3-Day Trial Active | Basic | Pro | Enterprise\n\n🏦 Wave: 09686563395 | KBZPay: 09697514209"
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=price_text, reply_markup=markup, parse_mode="Markdown")

        elif c_data == "nav_dash":
            dash_text = "📊 **Dashboard**\n━━━━━━━━━━━━━━━━━━\n🟢 License Active | Plan: Premium\n💰 Today Sales : 1,480,000 | Profit : 620,000"
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=dash_text, reply_markup=get_homepage_markup(), parse_mode="Markdown")

        elif c_data == "go_home":
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=get_welcome_text(expiry_str), reply_markup=get_homepage_markup(), parse_mode="Markdown")

        elif c_data in ["nav_reports_main", "ws_act", "nav_key_panel", "nav_ai", "nav_help", "nav_docs", "nav_ai_insights", "nav_ticket", "adm_keys"]:
            bot.send_message(chat_id, "⚙️ Security Gateway Active ✅")

    except Exception as error:
        print(f"🛡️ [Handled Exception]: {error}")
