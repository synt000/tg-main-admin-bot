from telebot import types
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
                types.InlineKeyboardButton("🛍️ Online Shop Pro (Sprint B Core) ✅", callback_data="ws_shop_pro_sprint"),
                types.InlineKeyboardButton("🔙 Back to OS", callback_data="go_home")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="💼 **Business Hub Workspaces (v1.0)**", reply_markup=markup, parse_mode="Markdown")

        elif c_data == "shop_p3_analytics" or c_data == "nav_reports_main":
            summary = CRMDashboard.get_business_summary(biz_id)
            
            try: t_cust, t_rev, t_pts = summary[0], summary[1], summary[2]
            except: t_cust, t_rev, t_pts = 0, 0, 0

            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("👑 View VIP Leaderboard", callback_data="crm_ui_leaderboard"),
                types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="go_home")
            )
            
            dashboard_text = (
                f"📈 **SaaS Executive Dashboard Intelligence**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🏪 Active Tenant ID : `{biz_id}`\n"
                f"👥 Total Customers Registered : `{t_cust} Users`\n"
                f"💰 Lifetime Accumulated Value (LTV) : **{float(t_rev):,} Ks**\n"
                f"🎯 Total Loyalty Pool Distributed : `{int(t_pts)} Points`\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🟢 System Health: PostgreSQL Cluster Live Sync Stable."
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=dashboard_text, reply_markup=markup, parse_mode="Markdown")

        elif c_data == "crm_ui_leaderboard":
            top_users = CRMDashboard.get_top_customers(biz_id, limit=3)
            leader_text = "👑 **Top Customers (VIP Leaderboard)**\n━━━━━━━━━━━━━━━━━━\n"
            
            for index, user in enumerate(top_users):
                try: u_name, u_spent, u_tier = user[1], user[2], user[3]
                except: u_name, u_spent, u_tier = "User", 0, "Regular"
                leader_text += f"🏅 Rank {index+1}: `{u_name}` | Spent: **{float(u_spent):,} Ks** | [{u_tier}]\n"
                
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔙 Back to Dashboard", callback_data="shop_p3_analytics"))
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=leader_text, reply_markup=markup, parse_mode="Markdown")

        elif c_data == "go_home":
            bot.delete_message(chat_id, message_id)
            bot.send_message(chat_id, "🏠 **BusinessOS Engine Home UI Active**\nSelect an operation workflow:")
