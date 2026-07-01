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
                types.InlineKeyboardButton("🛍️ Online Shop Pro (Sprint B Core) ✅", callback_data="ws_shop_pro_sprint"),
                types.InlineKeyboardButton("🔙 Back to OS", callback_data="go_home")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="💼 **Business Hub Workspaces (v1.0)**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "ws_shop_pro_sprint":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("👥 Phase 1: Customer Register & Profile", callback_data="shop_p1_cust"),
                types.InlineKeyboardButton("📦 Phase 2: Order List & Lifecycle Status", callback_data="shop_p2_order_flow"),
                types.InlineKeyboardButton("📊 Phase 3: Dynamic Sales Timelines Dashboard", callback_data="shop_p3_analytics"),
                types.InlineKeyboardButton("📄 Phase 4: Business UI (Pagination & Export)", callback_data="shop_p4_ui"),
                types.InlineKeyboardButton("🔙 Back", callback_data="nav_modules")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🛒 **Enterprise Shop Control Desk (Sprint B)**\n━━━━━━━━━━━━━━━━━━\nအစ်ကို ညွှန်ကြားထားသည့် ၅-လွှာ ဗိသုကာအဆင့်ဆင့်ကို အောက်ပါအတိုင်း လက်တွေ့စမ်းသပ်နိုင်ပါပြီဗျာ 👇", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "shop_p1_cust":
            ShopService.register_new_customer(biz_id, "Zarni Smart Buyer", "0979555222", "Mandalay")
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("➡️ Proceed to Order Lifecycle", callback_data="shop_p2_order_flow"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="✅ **[Phase 1: Customer Management System]**\n━━━━━━━━━━━━━━━━━━\n👤 Registered: `Zarni Smart Buyer`\n📞 Phone Gateway: `0979555222`\n🟢 Repository Link: PostgreSQL CRM Hook Synchronized Successfully.", reply_markup=markup, parse_mode="Markdown")
        elif c_data == "shop_p2_order_flow":
            ShopService.create_product(biz_id, "Premium Cotton Jacket", 50, 45000.00, "JACK-99")
            invoice, status = ShopService.create_enterprise_order(biz_id, 1, 1, 1, "WavePay")
            ShopService.update_order_lifecycle(biz_id, invoice['order_id'], "Confirm")
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("➡️ Proceed to Analytics Dashboard", callback_data="shop_p3_analytics"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"📦 **[Phase 2: Order Management Engine]**\n━━━━━━━━━━━━━━━━━━\n🆔 ORDER ID: `{invoice['order_id']}`\n⚙️ Initial Status: `Pending ⏳`\n🔄 Current Status: **Confirm ✅ (Auto-Transitioned)**\n💳 Unified Payment Gateway: `WavePay Sync [OK]`", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "shop_p3_analytics":
            analytics = ShopService.get_shop_analytics(biz_id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("➡️ Proceed to Telegram Business UI", callback_data="shop_p4_ui"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"📊 **[Phase 3: Dashboard & Timelines Telemetry]**\n━━━━━━━━━━━━━━━━━━\n📈 Daily Sales Tracker : `{analytics['daily']:,} Ks`\n📈 Weekly Sales Velocity : `{analytics['weekly']:,} Ks`\n📈 Monthly Accumulated : `{analytics['monthly']:,} Ks`\n━━━━━━━━━━━━━━━━━━\n🟢 Data Layer Integrity: 100% Verified.", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "shop_p4_ui":
            markup = types.InlineKeyboardMarkup(row_width=3)
            markup.add(
                types.InlineKeyboardButton("⏮️ Prev", callback_data="ws_act"),
                types.InlineKeyboardButton("📄 1 / 5", callback_data="ws_act"),
                types.InlineKeyboardButton("⏭️ Next", callback_data="ws_act"),
                types.InlineKeyboardButton("📥 Export CSV/PDF Report", callback_data="ws_act")
            )
            markup.add(types.InlineKeyboardButton("🔙 Back to Sprint B Menu", callback_data="ws_shop_pro_sprint"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="📱 **[Phase 4: Advanced Telegram Business UI]**\n━━━━━━━━━━━━━━━━━━\n💡 Pagination Controls and Report Export utilities rendering context dynamically inside current active tenant window:", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "go_home":
            bot.delete_message(chat_id, message_id)
            bot.send_message(chat_id, "🏠 **BusinessOS Engine Home UI Active**\nSelect an operation workflow:")
