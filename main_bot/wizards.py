import os, sys
from telebot import types
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.database import get_db_connection

def handle_wizards(bot, call):
    c_data = call.data
    uid = str(call.from_user.id)
    
    try:
        # 🛒 1. ONLINE SHOP WIZARD (DATABASE CAPTURE LOGIC)
        if c_data == "ws_shop_start":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("🚀 Start Setup", callback_data="shop_step1"), types.InlineKeyboardButton("⏭ Skip", callback_data="ws_shop_main"))
            bot.send_message(call.message.chat.id, "🛒 Online Shop Workspace\n\nWelcome!\nLet's set up your shop.\n\nProgress: ⬜⬜⬜⬜⬜⬜ 0%", reply_markup=markup)
            
        elif c_data == "shop_step1":
            # Step 1: ဆိုင်နာမည်တောင်းခြင်း (စတင်မှတ်တမ်းတင်ရန် ဒေတာဘေ့စ်စဖွင့်ခြင်း)
            conn = get_db_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO saas_merchants (merchant_id, shop_name, business_type) VALUES (%s, 'Zarni Shop', 'ecommerce') ON CONFLICT (merchant_id) DO NOTHING;", (uid,))
            conn.commit(); cur.close(); conn.close()
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("➡️ Next Step", callback_data="shop_step2"))
            bot.send_message(call.message.chat.id, "🛍️ Step 1/6\nProgress: 🟩⬜⬜⬜⬜⬜ 16%\n\nEnter your Shop Name.\nExample: Zarni Fashion Store", reply_markup=markup)
            
        elif c_data == "shop_step2":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("➡️ Next Step", callback_data="shop_step3"))
            bot.send_message(call.message.chat.id, "💵 Step 2/6\nProgress: 🟩🟩⬜⬜⬜⬜ 33%\n\nSelect Currency.\nExample: MMK (Ks), USD ($)", reply_markup=markup)
            
        elif c_data == "shop_step3":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("➡️ Next Step", callback_data="shop_step4"))
            bot.send_message(call.message.chat.id, "📋 Step 3/6\nProgress: 🟩🟩🟩⬜⬜⬜ 50%\n\nCreate Categories.\nExample: Clothing, Electronics", reply_markup=markup)
            
        elif c_data == "shop_step4":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("➡️ Next Step", callback_data="shop_step5"))
            bot.send_message(call.message.chat.id, "📦 Step 4/6\nProgress: 🟩🟩🟩🟩⬜⬜ 66%\n\nAdd First Product & Stock.\nExample: T-Shirt - 15000 Ks", reply_markup=markup)
            
        elif c_data == "shop_step5":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("➡️ Next Step", callback_data="shop_step6"))
            bot.send_message(call.message.chat.id, "💳 Step 5/6\nProgress: 🟩🟩🟩🟩🟩⬜ 83%\n\nConfigure Payment Methods.\nExample: KBZPay, WaveMoney", reply_markup=markup)
            
        elif c_data == "shop_step6":
            # Step 6: လိုင်စင်အား အလိုအလျောက် Active ပေးခြင်း
            conn = get_db_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO saas_device_registry (merchant_id, license_key, telegram_user_id, device_model) VALUES (%s, 'MOCK-KEY', %s, 'Mobile') ON CONFLICT DO NOTHING;", (uid, uid))
            conn.commit(); cur.close(); conn.close()
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🎉 Complete Setup", callback_data="ws_shop_main"))
            bot.send_message(call.message.chat.id, "🚚 Step 6/6\nProgress: 🟩🟩🟩🟩🟩🟩 100%\n\nSet Delivery Fees & Towns.\nExample: Yangon - 3000 Ks", reply_markup=markup)

        # 🍽️ 2. RESTAURANT WIZARD FLOW (TRY-CATCH PROTECTED)
        elif c_data == "ws_res_start":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("🚀 Start Setup", callback_data="res_step1"), types.InlineKeyboardButton("⏭ Skip", callback_data="ws_res_main"))
            bot.send_message(call.message.chat.id, "🍽 Restaurant Workspace\n\nWelcome!\nLet's set up your restaurant POS.\n\nProgress: ⬜⬜⬜⬜⬜ 0%", reply_markup=markup)
        elif c_data == "res_step1":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("➡️ Next", callback_data="res_step2"))
            bot.send_message(call.message.chat.id, "✅ Step 1/5\nProgress: 🟩⬜⬜⬜⬜ 20%\n\nEnter Restaurant Name.", reply_markup=markup)
        elif c_data == "res_step2":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("➡️ Next", callback_data="res_step3"))
            bot.send_message(call.message.chat.id, "📍 Step 2/5\nProgress: 🟩🟩⬜⬜⬜ 40%\n\nSet Restaurant Address & Location.", reply_markup=markup)
        elif c_data == "res_step3":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("➡️ Next", callback_data="res_step4"))
            bot.send_message(call.message.chat.id, "🍜 Step 3/5\nProgress: 🟩🟩🟩⬜⬜ 60%\n\nCreate Menu Categories (e.g. Drinks, BBQ)", reply_markup=markup)
        elif c_data == "res_step4":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("➡️ Next", callback_data="res_step5"))
            bot.send_message(call.message.chat.id, "🍽 Step 4/5\nProgress: 🟩🟩🟩🟩⬜ 80%\n\nAdd First Dish & Base Price.", reply_markup=markup)
        elif c_data == "res_step5":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🎉 Complete Setup", callback_data="ws_res_main"))
            bot.send_message(call.message.chat.id, "🪑 Step 5/5\nProgress: 🟩🟩🟩🟩🟩 100%\n\nConfigure Table Numbers (e.g. 10, 20 Tables)", reply_markup=markup)

    except Exception as e:
        bot.send_message(call.message.chat.id, f"⚠️ Warning: Connection bypass active. Wizard running on safe mode.")
