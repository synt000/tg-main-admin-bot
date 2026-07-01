import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('BOT_TOKEN')

# 🔗 အစ်ကို ထောက်ပြပေးထားသည့်အတိုင်း URL ပုံစံအမှန်သို့ ပြင်ဆင်ထားပါသည်
url = f"https://api.telegram.org/bot{token}/getUpdates"

try:
    response = requests.get(url).json()
    print("\n📥 --- RECENT TELEGRAM UPDATES ---")
    
    results = response.get("result", [])
    if not results:
        print("❌ မကြာသေးမီက ပို့ထားသော စာစောင်များကို ရှာမတွေ့ပါ။")
        print("💡 အတည်ပြုရန် သင်၏ Telegram Group ထဲတွင် စာတစ်စောင် (ဥပမာ- 'test') အရင်ရိုက်ပို့ပေးပါ။")
    
    for update in results:
        if "message" in update and "chat" in update["message"]:
            chat = update["message"]["chat"]
            chat_title = chat.get("title", chat.get("first_name", "Unknown"))
            chat_id = chat.get("id")
            chat_type = chat.get("type")
            
            print(f"🏪 Chat/Group အမည်: {chat_title} ({chat_type})")
            print(f"🆔 တကယ့် ID အစစ်အမှန်: {chat_id}")
            print("───────────────────────────────────")

except Exception as e:
    print(f"❌ Error: {e}")
