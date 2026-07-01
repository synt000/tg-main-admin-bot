import uuid
from core.database import get_db_connection

class ShopService:
    @staticmethod
    def create_product(biz_id, name, count, price, barcode=None):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO products (business_id, product_name, stock_count, price, barcode) VALUES (%s, %s, %s, %s, %s);", (biz_id, name, count, price, barcode))
        conn.commit(); cur.close(); conn.close()
        return True

    @staticmethod
    def process_customer_order(biz_id, prod_id, customer_id, buy_count):
        conn = get_db_connection(); cur = conn.cursor()
        
        # 1. 📦 Stock အခြေအနေကို စစ်ဆေးပြီး အလိုအလျောက် လျှော့ချခြင်း
        cur.execute("SELECT product_name, stock_count, price FROM products WHERE product_id = %s AND business_id = %s;", (prod_id, biz_id))
        prod = cur.fetchone()
        
        if not prod or prod['stock_count'] < buy_count:
            cur.close(); conn.close()
            return None, "Low Stock"
            
        new_stock = prod['stock_count'] - buy_count
        cur.execute("UPDATE products SET stock_count = %s WHERE product_id = %s;", (new_stock, prod_id))
        
        # 2. 🧾 Orders ဇယားထဲသို့ အော်တို သိမ်းဆည်းခြင်း
        order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        total_amount = prod['price'] * buy_count
        cur.execute("INSERT INTO orders (order_id, business_id, customer_id, total_amount, delivery_status) VALUES (%s, %s, %s, %s, 'Completed');", (order_id, biz_id, customer_id, total_amount))
        
        # 3. 💰 Income ဝင်ငွေစာရင်းထဲသို့ Auto-Sync သွန်းလောင်းခြင်း
        cur.execute("INSERT INTO income (business_id, amount, details) VALUES (%s, %s, %s);", (biz_id, total_amount, f"Shop Order {order_id} Sync"))
        
        # 4. 👥 CRM Spending စာရင်းအား အလိုအလျောက် သွားရောက် Update လုပ်ခြင်း
        cur.execute("UPDATE customers SET total_orders = total_orders + 1, total_spending = total_spending + %s WHERE customer_id = %s;", (total_amount, customer_id))
        
        conn.commit(); cur.close(); conn.close()
        
        # 📄 Invoice ပြန်ထုတ်ပေးရန် ဒေတာပက်ကတ် စုစည်းခြင်း
        return {
            "order_id": order_id,
            "product_name": prod['product_name'],
            "buy_count": buy_count,
            "total_amount": total_amount,
            "remaining_stock": new_stock
        }, "Success"
