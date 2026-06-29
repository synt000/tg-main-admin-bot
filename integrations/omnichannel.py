import json
import psycopg2
from core.database import get_db_connection

def sync_external_order(tenant_id, platform, platform_order_id, customer_name, items, total_price):
    """
    Facebook / TikTok မှ ဝင်လာသော အော်ဒါများကို ဗဟို Database သို့ သိမ်းဆည်းပြီး 
    Stock အရေအတွက်အား အလိုအလျောက် နှုတ်ပေးသည့် (Auto-Deduct) ဗိသုကာ Logic ဖြစ်သည်။
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # ၁။ အော်ဒါဟောင်း ရှိ၊ မရှိ စစ်ဆေးခြင်း (Duplicate Order ID Error ကာကွယ်ရန်)
        cursor.execute('''
            SELECT ext_order_id FROM external_orders 
            WHERE tenant_id = %s AND platform = %s AND platform_order_id = %s;
        ''', (tenant_id, platform, platform_order_id))
        
        if cursor.fetchone():
            print(f"⚠️ Order {platform_order_id} on {platform} already synced. Skipping...")
            return {"status": "skipped", "reason": "duplicate"}

        # ၂။ အော်ဒါအသစ်အား external_orders table ထဲသို့ သေသေချာချာ ထည့်သွင်းခြင်း
        cursor.execute('''
            INSERT INTO external_orders (tenant_id, platform, platform_order_id, customer_name, items_summary, total_price)
            VALUES (%s, %s, %s, %s, %s, %s);
        ''', (tenant_id, platform, platform_order_id, customer_name, json.dumps(items), total_price))
        
        # ၃။ 🛒 AUTO STOCK DEDUCTION LOGIC (ပစ္စည်းများ၏ Stock စာရင်းအား အလိုအလျောက် နှုတ်ပေးခြင်း)
        # items array format ဥပမာ: [{"product_id": 5, "quantity": 2}, {"product_id": 8, "quantity": 1}]
        for item in items:
            p_id = item.get("product_id")
            qty = item.get("quantity", 0)
            
            if p_id and qty > 0:
                # 🚨 RLS Security အတွက် လက်ရှိ ဆိုင်ရှင် Tenant ID အား Context ထဲ ထည့်ပေးရန် လိုအပ်ပါသည်
                cursor.execute(f"SET LOCAL app.current_tenant_id = {tenant_id};")
                
                # လက်ရှိ Stock အရေအတွက်အား စစ်ဆေးခြင်း
                cursor.execute("SELECT stock_quantity FROM products WHERE product_id = %s;", (p_id,))
                prod_data = cursor.fetchone()
                
                if prod_data:
                    current_stock = prod_data['stock_quantity']
                    # -1 ဆိုလျှင် ကန့်သတ်ချက်မရှိသော ပစ္စည်း (F&B / ဝန်ဆောင်မှု) ဖြစ်သဖြင့် Stock နှုတ်ရန်မလိုပါ
                    if current_stock != -1:
                        new_stock = max(0, current_stock - qty)
                        cursor.execute('''
                            UPDATE products SET stock_quantity = %s WHERE product_id = %s;
                        ''', (new_stock, p_id))
                        print(f"📉 Auto-deducted Stock for Product ID {p_id}: {current_stock} -> {new_stock}")

        conn.commit()
        print(f"✅ Omnichannel Order successfully synced from {platform} for Tenant ID: {tenant_id}")
        return {"status": "success", "platform_order_id": platform_order_id}
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Omnichannel Sync Failed: {e}")
        return {"status": "error", "message": str(e)}
        
    finally:
        cursor.close()
        conn.close()
