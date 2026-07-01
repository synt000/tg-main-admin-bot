import sys
import os
import secrets
from datetime import datetime, timedelta
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from core.database import get_db_connection

def create_merchant_and_key():
    if len(sys.argv) < 4:
        print("\n❌ အသုံးပြုပုံ မှားယွင်းနေပါသည်။")
        print("💡 ပုံစံ - python generate_key.py <လုပ်ငန်းကုဒ်> <လုပ်ငန်းအမည်> <အမျိုးအစား>")
        print("📝 အမျိုးအစားများ - ecommerce (အွန်လိုင်းရှော့) | restaurant (စားသောက်ဆိုင်) | lottery2d (၂Dဒိုင်) | trial (၃ရက်အစမ်းသုံး)")
        print("📝 ဥပမာ - python generate_key.py ko_zarni 'Zarni 2D' lottery2d\n")
        return

    merchant_id = sys.argv[1]
    shop_name = sys.argv[2]
    b_type = sys.argv[3]
    
    # ၃ရက် အစမ်းသုံးလား၊ ပရီမီယမ်လား ခွဲခြားသတ်မှတ်ခြင်း
    if b_type == "trial":
        key_type = "trial"
        b_type = "ecommerce" # အစမ်းသုံးကို အခြေခံ ရှော့ပင်းစနစ်ပေးခြင်း
        expires_at = datetime.now() + timedelta(days=3)
    else:
        key_type = "premium"
        expires_at = datetime.now() + timedelta(days=30) # ပုံမှန် ရက် ၃၀ လချုပ်

    # 🔑 လုံခြုံသော License Key အား အလိုအလျောက် ထုတ်လုပ်ခြင်း
    random_hex = secrets.token_hex(4).upper()
    license_key = f"PRO-KEY-{merchant_id.upper()}-{random_hex}"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # လုပ်ငန်းရှင်အချက်အလက် ထည့်ခြင်း
        cursor.execute('''
            INSERT INTO saas_merchants (merchant_id, shop_name, business_type)
            VALUES (%s, %s, %s)
            ON CONFLICT (merchant_id) DO UPDATE SET shop_name = EXCLUDED.shop_name, business_type = EXCLUDED.business_type;
        ''', (merchant_id, shop_name, b_type))
        
        # လိုင်စင်ကီး ထည့်ခြင်း
        cursor.execute('''
            INSERT INTO saas_licenses (license_key, merchant_id, key_type, expires_at)
            VALUES (%s, %s, %s, %s);
        ''', (license_key, merchant_id, key_type, expires_at))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n🎉 [License Generated]: ကီးအသစ် အောင်မြင်စွာ ထုတ်ပြီးပါပြီ !")
        print(f"🏪 လုပ်ငန်းအမည်: {shop_name} ({b_type.upper()})")
        print(f"🔑 သတ်မှတ်ပေးလိုက်သော KEY: {license_key}")
        print(f"⏳ သက်တမ်းကုန်ဆုံးမည့်ရက်: {expires_at.strftime('%Y-%m-%d %H:%M:%S')} ({key_type.upper()})\n")
        
    except Exception as e:
        print(f"❌ Key Generation Error: {e}")

if __name__ == "__main__":
    create_merchant_and_key()
