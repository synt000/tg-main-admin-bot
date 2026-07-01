from telebot import types

class HomeKeyboards:
    @staticmethod
    def get_homepage_markup():
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🏠 Dashboard", callback_data="nav_dash"),
            types.InlineKeyboardButton("💼 Business Hub", callback_data="nav_modules"),
            types.InlineKeyboardButton("🎨 Brand Studio", callback_data="nav_brand_studio"),
            types.InlineKeyboardButton("🚀 Growth Center", callback_data="nav_growth_center"),
            types.InlineKeyboardButton("🤖 AI OS Center", callback_data="nav_ai_center"),
            types.InlineKeyboardButton("📊 Reports", callback_data="nav_reports_main"),
            types.InlineKeyboardButton("⚙️ Settings", callback_data="nav_settings_main")
        )
        return markup
