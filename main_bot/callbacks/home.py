from telebot import types
from modules.billing.service import BillingService
from modules.crm.dashboard import CRMDashboard

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
                types.InlineKeyboardButton("🛍️ Online Shop Pro Workspace (FREE Plan)", callback_data="ws_shop_pro_sprint"),
                types.InlineKeyboardButton("🤖 AI Executive Assistant Workspace (PRO Required)", callback_data="ws_ai_premium_gate"),
                types.InlineKeyboardButton("💳 Upgrade to PRO Plan (SaaS Billing)", callback_data="saas_buy_pro"),
                types.InlineKeyboardButton("🔙 Back to OS", callback_data="go_home")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="💼 **Business Hub Multi-Tenant Workspaces**", reply_markup=markup, parse_mode="Markdown")

        # 💳 SAAS TELEGRAM BILLING COMMAND ACTION
        elif c_data == "saas_buy_pro":
            BillingService.buy_pro_plan(biz_id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔙 Back to Workspaces", callback_data="nav_modules"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="✅ **[PRO Plan Activated Successfully!]**\n━━━━━━━━━━━━━━━━━━\n💳 Payment Status: Verified\n🚀 Subscription Tier: Upgraded to **PRO TIER**\n💎 Perks Unlocked: CRM, Analytics & Predictive AI Engine.", reply_markup=markup, parse_mode="Markdown")

        # 🔒 FEATURE GATED PREMIUM WORKSPACE
        elif c_data == "ws_ai_premium_gate":
            # Fetch merchant current live subscription row from database
            sub = BillingService.get_subscription_status(biz_id)
            current_plan = sub if sub else "FREE"
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="nav_modules"))
            
            try:
                # 🔐 Feature Gate Check Triggering
                BillingService.require_plan(current_plan, "PRO")
                
                # If Passed, Render the Predictive AI Dashboard Layout
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🤖 **Welcome to Premium BusinessOS AI OS Engine**\n━━━━━━━━━━━━━━━━━━\nStatus: `Access Granted ✅` \n💡 Insights and predictive forecasting algorithms running optimally under current tier authorization context.", reply_markup=markup, parse_mode="Markdown")
            except Exception as ex:
                # If Failed, Intercept and Block the Handler Context
                upgrade_markup = types.InlineKeyboardMarkup(row_width=1)
                upgrade_markup.add(types.InlineKeyboardButton("💳 Buy PRO Plan Now", callback_data="saas_buy_pro"), types.InlineKeyboardButton("🔙 Back", callback_data="nav_modules"))
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"🔒 **[Feature Locked]**: `{ex}`\n━━━━━━━━━━━━━━━━━━\n⚠️ ဤ AI မော်ဂျူးအား အသုံးပြုနိုင်ရန် **PRO Plan** သို့ အဆင့်မြှင့်တင်ပေးရန် လိုအပ်ပါတယ်ဗျာ။", reply_markup=upgrade_markup, parse_mode="Markdown")

        elif c_data == "go_home":
            bot.delete_message(chat_id, message_id)
            bot.send_message(chat_id, "🏠 **BusinessOS Engine Home UI Active**")
