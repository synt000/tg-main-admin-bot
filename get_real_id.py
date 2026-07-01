import os
import sys
import telebot
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

# မူလ Main Bot Token ကို အသုံးပြုခြင်း
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

print("📡 Group ID အစစ်အမှန်ကို ရှာဖွေနေပါသည်...")
print("💡 လူကြီးမင်း၏ Telegram Group ထဲတွင် စာတစ်စောင် (ဥပမာ- 'test') ဟု ရိုက်ပို့ပေးပါ...")

try:
    updates = bot.get_updates(limit=10, timeout=10)
    print("\n📥 --- TELEGRAM RECENT UPDATES ---")
    found = False
    for u in updates:
        if u.message and u.message.chat:
            found = True
            chat_type = u.message.chat.type
            chat_title = u.message.chat.title or u.message.chat.first_name or "Unknown"
            print(f"💬 Chat အမျိုးအစား: {chat_type.upper()}")
            print(f"🏪 Chat/Group အမည်: {chat_title}")
            print(f"🆔 တကယ့် Chat ID အစစ်အမှန်: {u.message.chat.id}")
            print("───────────────────────────────────")
    if not found:
        print("❌ မကြာသေးမီက ပို့ထားသော စာစောင်များကို ရှာမတွေ့ပါ။ Group ထဲတွင် စာတစ်စောင် အရင်ရိုက်ပို့ပေးပါ။")
except Exception as e:
    print(f"❌ Error: {e}")
