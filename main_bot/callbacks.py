from datetime import datetime, timedelta
import secrets
from telebot import types
from main_bot.main import get_homepage_markup
from main_bot.wizards import handle_wizards
from main_bot.wizards_part2 import handle_wizards_extended
from main_bot.workspaces import load_workspaces

def register_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: True)
    def core_callback_handler(call):
        bot.answer_callback_query(call.id)
        c_data = call.data
        
        if c_data.startswith("gen_"):
            parts = c_data.split("_")
            shop_id, b_type, duration = parts[1], parts[2], parts[3]
            days = 30; d_text = "၃ လ"
            if duration == "1w": days = 7; d_text = "၁ ပတ်"
            elif duration == "10d": days = 10; d_text = "၁၀ ရက်"
            elif duration == "3m": days = 90; d_text = "၃ လ"
            elif duration == "6m": days = 180; d_text = "၆ လ"
            elif duration == "1y": days = 365; d_text = "၁ နှစ်"
            exp_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            license_key = f"PRO-KEY-{shop_id.upper()}-{secrets.token_hex(4).upper()}"
            success_msg = f"🔑 [SaaS Key Issued! 🎉]\n━━━━━━━━━━━━━━\n🆔 ဆိုင်ကုဒ်: {shop_id.upper()}\n⏳ သက်တမ်း: {d_text}\n📅 ကုန်ဆုံးရက်: {exp_date}\n🔑 LICENSE KEY:\n{license_key}"
            bot.send_message(call.message.chat.id, success_msg)
            return

        if c_data.startswith("ws_") or c_data.startswith("shop_") or c_data.startswith("res_") or c_data.startswith("hotel_") or c_data.startswith("2d_"):
            handle_wizards(bot, call)
            handle_wizards_extended(bot, call)
            load_workspaces(bot, call)
            return

        if c_data == "nav_dash":
            bot.send_message(call.message.chat.id, "📊 Business Dashboard\n━━━━━━━━━━━━━━━━━━\n🟢 License : Active\n🛒 Shop : Enabled\n🍽 Restaurant : Not Activated\n🏨 Hotel : Enabled\n🤖 AI : Online\n📦 Storage : 68%\n📅 Expire : 28 Jul 2026\n━━━━━━━━━━━━━━━━━━\n💰 Today Sales : 1,480,000 Ks\n🧾 Orders : 82\n👥 Customers : 46\n📦 Products : 325")
        elif c_data == "nav_design":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🖼️ Auto Framing", callback_data="go_home"), types.InlineKeyboardButton("✂️ Remove Background", callback_data="go_home"), types.InlineKeyboardButton("⬅️ Back", callback_data="go_home"))
            bot.send_message(call.message.chat.id, "🎨 AI Studio\n🎨 AI Smart Design Studio", reply_markup=markup)
            
        elif c_data == "nav_pricing":
            # 💳 Pricing မန်နူးအောက်ခြေတွင် ဆက်သွယ်ရန် ဖုန်းနံပါတ်အစစ်အား ထည့်သွင်းခြင်း
            price_text = (
                "💳 Pricing\n"
                "💳 SaaS Licensing\n\n"
                "🥉 Basic\n39,000 Ks\n\n"
                "🥈 Professional\n150,000 Ks\n✔ Save 15%\n\n"
                "🥇 Enterprise\n290,000 Ks\n⭐ Best Value\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "☎️ Contact Support to Activate:\n"
                "📞 KPay No: 09697514209 / Wave No: 09686563395"
            )
            bot.send_message(call.message.chat.id, price_text)
            
        elif c_data == "nav_support":
            # ☎️ Support မန်နူးတွင် အစ်ကို့ရဲ့ ဖုန်းနံပါတ်အစစ်နှင့် အချက်အလက်များ ထည့်သွင်းခြင်း
            support_text = (
                "☎️ Support\n"
                "☎️ Customer Support\n\n"
                "👤 Telegram\n@ZarniSaaSSupport\n\n"
                "📞 Hotline Phone\n09-686563395\n\n"
                "🕘 Service Hours\n09:00 AM - 09:00 PM\n\n"
                "⚡ Average Response\n< 10 Minutes\n\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "💬 Need help?\nContact us anytime."
            )
            bot.send_message(call.message.chat.id, support_text)
            
        elif c_data == "nav_key_panel":
            bot.send_message(call.message.chat.id, "💡 ကီးထုတ်ရန်ပုံစံ:\n/genkey ဆိုင်ကုဒ် ဆိုင်အမည် လုပ်ငန်းအမျိုးအစား")
        elif c_data == "nav_ai":
            bot.send_message(call.message.chat.id, "🤖 AI Assistant\n\n🟢 Status : Online\n⚡ AI Engine : Active\n🧠 Version : Pro")
        elif c_data == "go_home":
            bot.send_message(call.message.chat.id, "🏠 ပင်မစာမျက်နှာသို့ ပြန်ရောက်ပါပြီ။", reply_markup=get_homepage_markup())
