import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from core.database import get_db_connection

def add_new_merchant_bot():
    if len(sys.argv) < 5:
        print("\n❌ အသုံးပြုပုံ မှားယွင်းနေပါသည်။")
        print("💡 ပုံစံ - python add_merchant_bot.py <ဆိုင်ကုဒ်> <ဆိုင်အမည်> <Bot_Token> <Group_ID>")
        print("📝 ဥပမာ - python add_merchant_bot.py coffee_002 'Golden Coffee' '1234:AAxx...' '-100xxxx'\n")
        return

    shop_code = sys.argv[1]
    shop_name = sys.argv[2]
    bot_token = sys.argv[3]
    real_group_id = sys.argv[4]
    shop_type = "ecommerce"
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO shops (shop_code, shop_name, shop_type, merchant_bot_token, tg_group_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (shop_code) 
            DO UPDATE SET shop_name = EXCLUDED.shop_name, merchant_bot_token = EXCLUDED.merchant_bot_token, tg_group_id = EXCLUDED.tg_group_id;
        ''', (shop_code, shop_name, shop_type, bot_token, real_group_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n🎉 အောင်မြင်ပါသည်။ ဆိုင်ရှင်သစ် အငှား Bot အား စနစ်ထဲသို့ ထည့်သွင်းပြီးပါပြီ !")
        print(f"🏪 ဆိုင်အမည်: {shop_name} ({shop_code})")
        print(f"🆔 ချိတ်ဆက်ထားသော Group ID: {real_group_id}")
        print(f"💡 အပြောင်းအလဲ သိရှိစေရန် ပထမ Session (run.py) အား Restart ချပေးပါဗျာ။\n")
        
    except Exception as e:
        print(f"❌ Database Insert Error: {e}")

if __name__ == "__main__":
    add_new_merchant_bot()
