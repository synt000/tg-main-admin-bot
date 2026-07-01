from telebot import types
from modules.ai.assistant import BusinessAI

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
                types.InlineKeyboardButton("🤖 Sprint D: AI OS Brain Engine ✅", callback_data="ws_ai_brain_sprint"),
                types.InlineKeyboardButton("🔙 Back to OS", callback_data="go_home")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="💼 **Business Hub Workspaces (v1.0)**", reply_markup=markup, parse_mode="Markdown")

        # 🧠 SPRINT D: AI INTEL LAYERS WORKSPACE FLOW
        elif c_data == "ws_ai_brain_sprint" or c_data == "nav_ai_center":
            insights_data = BusinessAI.generate_business_insight(biz_id)
            actions = BusinessAI.recommend_actions(biz_id)
            alerts = BusinessAI.generate_alerts(biz_id)

            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="go_home"))
            
            # Formatting AI outputs dynamically
            insight_str = "\n".join([f"• {i}" for i in insights_data['insights']])
            action_str = "\n".join([f"⚡ {a}" for i, a in enumerate(actions)])
            alert_str = "\n".join([f"{al}" for al in alerts]) if alerts else "🟢 System Stable • No Crucial Alerts"

            ai_text = (
                f"🤖 **BusinessOS Predictive AI Center**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📊 **[AI Strategic Insights]**\n{insight_str}\n\n"
                f"💡 **[Smart Recommendations]**\n{action_str}\n\n"
                f"🔔 **[Real-time Automation Alerts]**\n`{alert_str}`\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🚀 Powered by BusinessOS Intelligent AI Layer."
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=ai_text, reply_markup=markup, parse_mode="Markdown")

        elif c_data == "go_home":
            bot.delete_message(chat_id, message_id)
            bot.send_message(chat_id, "🏠 **BusinessOS Engine Home UI Active**\nSelect an operation workflow:")
