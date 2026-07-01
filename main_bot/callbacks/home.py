from telebot import types
from modules.shop.service import ShopService

def register_home_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_home_navigation(call):
        bot.answer_callback_query(call.id)
        c_data = call.data
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        biz_id = "MOCK_BIZ_001"

        if c_data == "nav_modules":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🛍️ Online Shop Pro (Sprint B) ✅", callback_data="ws_shop_pro_sprint"),
                types.InlineKeyboardButton("🔙 Back to OS", callback_data="go_home")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="💼 **Business Hub Workspaces (v1.0)**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "ws_shop_pro_sprint":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("➕ Phase 1: Add New Product", callback_data="shop_p1_add"),
                types.InlineKeyboardButton("🛒 Phase 3 & 5: Create Order", callback_data="shop_p3_order"),
                types.InlineKeyboardButton("📊 Phase 7: Generate Report", callback_data="shop_p7_report"),
                types.InlineKeyboardButton("🔙 Back", callback_data="nav_modules")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🛒 **Online Shop Pro Control Desk**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "shop_p1_add":
            ShopService.create_product(biz_id, "Premium Cotton Jacket", 80, 45000.00, "SKU-JACK-99")
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("➡️ Proceed to Orders", callback_data="shop_p3_order"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="✅ **[Phase 1 & 2: Product Initialized]**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "shop_p3_order":
            from core.database import get_db_connection
            conn = get_db_connection(); cur = conn.cursor()
            cur.execute("SELECT product_id FROM products WHERE business_id = %s ORDER BY product_id DESC LIMIT 1;", (biz_id,))
            row = cur.fetchone(); p_id = row['product_id'] if row else 1
            cur.close(); conn.close()

            invoice, status = ShopService.create_enterprise_order(biz_id, p_id, 105, 1, "KBZPay")
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📊 Proceed to Phase 7 Reports", callback_data="shop_p7_report"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"📄 **BusinessOS Invoice Issued**: {status}", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "shop_p7_report" or c_data == "nav_reports_main":
            analytics = ShopService.get_shop_analytics(biz_id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🏠 OS Main Menu", callback_data="go_home"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"📊 **Sales Report**: Total Gross: {analytics['sales']:,} Ks", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "go_home":
            from main_bot.handlers.home import register_home_handlers
            bot.delete_message(chat_id, message_id)
            bot.send_message(chat_id, "🏠 **BusinessOS Engine Home UI Active**")
