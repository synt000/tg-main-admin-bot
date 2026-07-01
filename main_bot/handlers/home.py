from telebot import types
from datetime import datetime, timedelta
from core.database import get_db_connection

def register_home_handlers(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        uid = str(message.from_user.id)
        trial_expiry = datetime.now() + timedelta(days=3)
        expiry_str = trial_expiry.strftime('%Y-%m-%d %H:%M:%S')

        try:
            # 🟠 SQLite ဖယ်ရှားပြီး PostgreSQL တစ်ခုတည်းသို့သာ တိုက်ရိုက် ရေးသွင်းခြင်း
            conn = get_db_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO licenses (license_key, merchant_id, key_type, is_activated, expires_at) VALUES (%s, %s, 'trial', TRUE, %s) ON CONFLICT DO NOTHING;", (f"TRIAL-{uid}", uid, trial_expiry))
            conn.commit(); cur.close(); conn.close()
        except: pass

        # 🏠 7-CORE Enterprise OS Homepage Layout
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🏠 Dashboard", callback_data="nav_dash"),
            types.InlineKeyboardButton("💼 Business Hub", callback_data="nav_modules"),
            types.InlineKeyboardButton("🎨 Brand Studio", callback_data="nav_brand_studio"),
            types.InlineKeyboardButton("🚀 Growth Center", callback_data="nav_growth_center"),
            types.InlineKeyboardButton("🤖 AI Center", callback_data="nav_ai_center"),
            types.InlineKeyboardButton("📊 Reports", callback_data="nav_reports_main"),
            types.InlineKeyboardButton("⚙️ Settings", callback_data="nav_settings_main")
        )

        welcome_text = (
            f"Welcome to BusinessOS v1.0 🚀\n"
            f"🔥 One Platform. Every Business.\n━━━━━━━━━━━━━━━━━━\n"
            f"🆓 3-Day Free Trial: **Activated ✅**\n"
            f"Valid Until : `{expiry_str}`\n"
            f"Remaining : `3 Days`\n\n"
            f"Manage Everything from Telegram. Select a core workspace:"
        )
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")
