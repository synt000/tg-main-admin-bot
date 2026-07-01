from telebot import types
from modules.billing.service import BillingService
from modules.crm.dashboard import CRMDashboard

def register_home_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_home_navigation(call):
        # 🚀 🔒 [SAFE BYPASS GLITCH APPLIED]: Callback Query Crash မဖြစ်စေရန် အစ်ကို့နည်းလမ်းအတိုင်း Safe Intercept လုပ်ခြင်း
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass

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

        elif c_data == "saas_buy_pro":
            BillingService.buy_pro_plan(biz_id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔙 Back to Workspaces", callback_data="nav_modules"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="✅ **[PRO Plan Activated Successfully!]**\n━━━━━━━━━━━━━━━━━━\n💳 Payment Status: Verified\n🚀 Subscription Tier: Upgraded to **PRO TIER**\n💎 Perks Unlocked: CRM, Analytics & Predictive AI Engine.", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "ws_ai_premium_gate":
            sub = BillingService.get_subscription_status(biz_id)
            current_plan = sub if sub else "FREE"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="nav_modules"))
            
            try:
                BillingService.require_plan(current_plan, "PRO")
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🤖 **Welcome to Premium BusinessOS AI OS Engine**\n━━━━━━━━━━━━━━━━━━\nStatus: `Access Granted ✅` \n💡 Insights and predictive forecasting algorithms running optimally under current tier authorization context.", reply_markup=markup, parse_mode="Markdown")
            except Exception as ex:
                upgrade_markup = types.InlineKeyboardMarkup(row_width=1)
                upgrade_markup.add(types.InlineKeyboardButton("💳 Buy PRO Plan Now", callback_data="saas_buy_pro"), types.InlineKeyboardButton("🔙 Back", callback_data="nav_modules"))
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"🔒 **[Feature Locked]**: `{ex}`\n━━━━━━━━━━━━━━━━━━\n⚠️ ဤ AI မော်ဂျူးအား အသုံးပြုနိုင်ရန် **PRO Plan** သို့ အဆင့်မြှင့်တင်ပေးရန် လိုအပ်ပါတယ်ဗျာ။", reply_markup=upgrade_markup, parse_mode="Markdown")

        elif c_data == "go_home":
            # 🚀 🔒 [SAFE MESSAGE DELETE APPLIED]: Message ပျောက်သွားခဲ့လျှင် Crash မဖြစ်စေရန် Intercept လုပ်ခြင်း
            try:
                bot.delete_message(chat_id, message_id)
            except Exception:
                pass
            bot.send_message(chat_id, "🏠 **BusinessOS Engine Home UI Active**", parse_mode="Markdown")
