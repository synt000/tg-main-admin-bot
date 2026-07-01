import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from core.database import get_db_connection

def update_group():
    # ရိုက်ထည့်လိုက်သည့် Argument စစ်ဆေးခြင်း
    if len(sys.argv) < 3:
        print("❌ အသုံးပြုပုံ မှားယွင်းနေပါသည်။")
        print("💡 ပုံစံ - python update_shop_group.py <shop_code> <group_id>")
        return

    shop_code = sys.argv[1]
    real_group_id = sys.argv[2]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # ဆိုင်ကုဒ်အလိုက် Group ID ကို Dynamic ပြောင်းလဲခြင်း
        cursor.execute('''
            UPDATE shops 
            SET tg_group_id = %s 
            WHERE shop_code = %s;
        ''', (real_group_id, shop_code))
        
        conn.commit()
        
        # ပြောင်းလဲမှု အောင်မြင်၊ မအောင်မြင် စစ်ဆေးခြင်း
        if cursor.rowcount > 0:
            print(f"✅ Successful! Shop '{shop_code}' updated with Real Group ID: {real_group_id}")
        else:
            print(f"❌ Error: Database ထဲတွင် ဆိုင်ကုဒ် '{shop_code}' ကို ရှာမတွေ့ပါ။")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Database Update Error: {e}")

if __name__ == "__main__":
    update_group()
