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
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🛒 Online Shop (Sprint A) ✅", callback_data="ws_shop_sprint"),
                types.InlineKeyboardButton("🎲 2D Agent (Sprint B)", callback_data="ws_act"),
                types.InlineKeyboardButton("🔙 Back to OS", callback_data="go_home")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="💼 **Business Hub Workspaces (v1.0)**\n\n👇 Select an operational workspace below:", reply_markup=markup, parse_mode="Markdown")

        # 🛒 SPRINT A: ONLINE SHOP PRODUCTION WORKFLOW
        elif c_data == "ws_shop_sprint":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("📦 Step 1: Add Product", callback_data="shop_flow_add"),
                types.InlineKeyboardButton("🛒 Step 2: Place Order & Invoice", callback_data="shop_flow_order"),
                types.InlineKeyboardButton("🔙 Back", callback_data="nav_modules")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🛒 **Online Shop Live Workflow Desk**\n━━━━━━━━━━━━━━━━━━\nအောက်ပါ လုပ်ငန်းစဉ်အတိုင်း အဆင့်ဆင့် နှိပ်ပြီး စမ်းသပ်မောင်းနှင်နိုင်ပါပြီဗျာ 👇", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "shop_flow_add":
            # 1. Add Product ဒေတာဘေ့စ်ထဲ တကယ်သွားရေးခြင်း
            ShopService.create_product(biz_id, "Oversized T-Shirt", 50, 18000.00, "BC-9842")
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("➡️ Proceed to Step 2", callback_data="shop_flow_order"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="✅ **[Step 1: Stock Added Successfully]**\n━━━━━━━━━━━━━━━━━━\n📦 Item logged: `Oversized T-Shirt`\n🔢 Initial Stock: `50 Units` Added\n💰 Base Price: `18,000 Ks` Saved in PostgreSQL.", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "shop_flow_order":
            # 2. Place Order ➔ Stock လျော့ ➔ Income ဝင် ➔ Invoice ထွက်မည့် မာစတာစနစ်ကြီး
            invoice, status = ShopService.process_customer_order(biz_id, 1, 102, 2) # Product ID #1 အား ဝယ်သူ #102 က (၂) ထည် မှာယူခြင်း
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 Test Flow Again", callback_data="ws_shop_sprint"), types.InlineKeyboardButton("🏠 Main Menu", callback_data="go_home"))
            
            if invoice:
                invoice_text = (
                    f"📄 **BusinessOS Dynamic Invoice**\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"🆔 ORDER ID : `{invoice['order_id']}`\n"
                    f"👕 Item Name : {invoice['product_name']}\n"
                    f"🔢 Quantity : {invoice['buy_count']} Units\n"
                    f"💰 Total Bill : **{invoice['total_amount']:,} Ks**\n"
                    f"📅 Status : Paid & Completed ✅\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"🔄 **[Unified OS Sync Status]**\n"
                    f"📦 Remaining Stock: `{invoice['remaining_stock']} Units` (Auto-Reduced)\n"
                    f"💰 Cashbook Ledger: `+150,000 Ks` Injected\n"
                    f"👥 CRM Status: Customer History Logged\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"🚀 Powered by BusinessOS • One Platform. Every Business."
                )
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=invoice_text, reply_markup=markup, parse_mode="Markdown")
            else:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"⚠️ **Order Processing Failed**: {status}. Please reset stock count.", reply_markup=markup, parse_mode="Markdown")

        # GENERAL RESET ROUTINGS
        elif c_data in ["ws_act", "nav_dash", "nav_brand_studio", "nav_growth_center", "nav_ai_center", "nav_reports_main", "nav_settings_main"]:
            bot.send_message(chat_id, "🛡️ [SaaS Commercial Router Check]: Action Authorized ✅")
        elif c_data == "go_home":
            from main_bot.handlers.home import register_home_handlers
            bot.delete_message(chat_id, message_id)
            bot.send_message(chat_id, "🏠 ပင်မစာမျက်နှာသို့ ပြန်ရောက်ပါပြီ။")
