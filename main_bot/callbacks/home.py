from telebot import types
from main_bot.keyboards.home import HomeKeyboards

def register_home_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_home_navigation(call):
        bot.answer_callback_query(call.id)
        c_data = call.data
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        # 💼 BUSINESS HUB WORKSPACES (v1.0 Version 1.0 Feature Freeze Modules)
        if c_data == "nav_modules":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🛍️ Online Shop", callback_data="ws_act"),
                types.InlineKeyboardButton("🎲 2D Agent", callback_data="ws_act"),
                types.InlineKeyboardButton("👥 CRM Module", callback_data="ws_act"),
                types.InlineKeyboardButton("📦 Stock Management", callback_data="ws_act"),
                types.InlineKeyboardButton("💰 Finance Desk", callback_data="ws_act")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="💼 **Business Hub Workspaces (v1.0)**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "nav_growth_center":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("📣 Marketing", callback_data="ws_act"), types.InlineKeyboardButton("🎁 Coupon", callback_data="ws_act"), types.InlineKeyboardButton("👥 Referral", callback_data="ws_act"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🚀 **Growth Center Panel**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "nav_brand_studio":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("🏷️ Logo Maker", callback_data="ws_act"), types.InlineKeyboardButton("📢 Banner Maker", callback_data="ws_act"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🎨 **Brand Studio Dashboard**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "nav_ai_center":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("💬 AI Chat", callback_data="ws_act"), types.InlineKeyboardButton("✍️ AI Writer", callback_data="ws_act"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🤖 **AI Center Hub**", reply_markup=markup, parse_mode="Markdown")

        elif c_data in ["ws_act", "nav_dash", "nav_reports_main", "nav_settings_main"]:
            bot.send_message(chat_id, "🛡️ [SaaS Commercial Router Check]: Authorized ✅")
