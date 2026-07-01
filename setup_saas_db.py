import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from core.database import get_db_connection

def build_advanced_saas_tables():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # ၁။ လုပ်ငန်းရှင်များနှင့် ၎င်းတို့၏ Device ID၊ လုပ်ငန်းအမျိုးအစား မှတ်မည့်ဇယား
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saas_merchants (
                id SERIAL PRIMARY KEY,
                merchant_id VARCHAR(50) UNIQUE NOT NULL,
                shop_name VARCHAR(100) NOT NULL,
                business_type VARCHAR(50) NOT NULL, -- ecommerce, restaurant, delivery, booking, lottery2d
                device_id VARCHAR(100) DEFAULT NULL, -- 1 Device လုံခြုံရေးအတွက်
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # ၂။ 1 Device 1 Key စနစ်အတွက် License Keys များ မှတ်မည့်ဇယား
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saas_licenses (
                id SERIAL PRIMARY KEY,
                license_key VARCHAR(100) UNIQUE NOT NULL,
                merchant_id VARCHAR(50) REFERENCES saas_merchants(merchant_id) ON DELETE CASCADE,
                is_activated BOOLEAN DEFAULT FALSE,
                key_type VARCHAR(20) DEFAULT 'premium', -- trial (၃ရက်), premium (လချုပ်/နှစ်ချုပ်)
                expires_at TIMESTAMP NOT NULL
            );
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("📊 [SaaS Engine]: Advanced License & Device Security Tables Created Successfully!")
    except Exception as e:
        print(f"❌ Database Setup Error: {e}")

if __name__ == "__main__":
    build_advanced_saas_tables()
