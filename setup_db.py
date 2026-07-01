import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from core.database import get_db_connection

def configure_whitelabel_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # ဆိုင်ရှင်များ၏ သီးသန့် Bot Token ပါ သိမ်းမည့် ဇယားအသစ်
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shops (
                id SERIAL PRIMARY KEY,
                shop_code VARCHAR(50) UNIQUE NOT NULL,
                shop_name VARCHAR(100) NOT NULL,
                shop_type VARCHAR(50) NOT NULL,
                merchant_bot_token TEXT,
                tg_group_id VARCHAR(50),
                is_active BOOLEAN DEFAULT TRUE
            );
        ''')
        
        # မူလ စမ်းသပ်ထားသော ဆိုင်အား သီးသန့် Token ကော်လံဖြင့် အစားထိုးခြင်း
        # 🚨 (အစ်ကို့ Main Bot Token ကိုပဲ လက်ရှိ ဆိုင်ရှင်တစ်ယောက်အနေနဲ့ စမ်းသပ်ထည့်သွင်းထားပါသည်)
        cursor.execute('''
            INSERT INTO shops (shop_code, shop_name, shop_type, merchant_bot_token, tg_group_id)
            VALUES 
            ('onlineshop_001', 'Zarni Online Shop', 'ecommerce', '8795273928:AAHaQ9SjrqrCjtdT-St0ts708BlOlYe9Bss', '-1004450260207')
            ON CONFLICT (shop_code) 
            DO UPDATE SET merchant_bot_token = EXCLUDED.merchant_bot_token, tg_group_id = EXCLUDED.tg_group_id;
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Whitelabel Database Engine Configured Successfully!")
    except Exception as e:
        print(f"❌ Database Setup Error: {e}")

if __name__ == "__main__":
    configure_whitelabel_db()
