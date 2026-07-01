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
    def adjust_stock(biz_id, prod_id, count, action_type="in"):
        conn = get_db_connection(); cur = conn.cursor()
        if action_type == "in":
            cur.execute("UPDATE products SET stock_count = stock_count + %s WHERE product_id = %s AND business_id = %s;", (count, prod_id, biz_id))
        else:
            cur.execute("UPDATE products SET stock_count = stock_count - %s WHERE product_id = %s AND business_id = %s;", (count, prod_id, biz_id))
        conn.commit(); cur.close(); conn.close()
        return True

    @staticmethod
    def create_enterprise_order(biz_id, prod_id, customer_id, buy_count, payment_method="KBZPay"):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT product_name, stock_count, price FROM products WHERE product_id = %s AND business_id = %s;", (prod_id, biz_id))
        prod = cur.fetchone()
        
        if not prod or prod['stock_count'] < buy_count:
            cur.close(); conn.close()
            return None, "Low Stock Alert"
            
        new_stock = prod['stock_count'] - buy_count
        cur.execute("UPDATE products SET stock_count = %s WHERE product_id = %s;", (new_stock, prod_id))
        
        order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        total_amount = prod['price'] * buy_count
        
        cur.execute("INSERT INTO orders (order_id, business_id, customer_id, total_amount, delivery_status) VALUES (%s, %s, %s, %s, 'Confirm');", (order_id, biz_id, customer_id, total_amount))
        cur.execute("INSERT INTO income (business_id, amount, details) VALUES (%s, %s, %s);", (biz_id, total_amount, f"Order {order_id} via {payment_method}"))
        conn.commit(); cur.close(); conn.close()
        
        return {"order_id": order_id, "product_name": prod['product_name'], "buy_count": buy_count, "total_amount": total_amount, "remaining_stock": new_stock, "payment": payment_method}, "Success"

    @staticmethod
    def list_products(biz_id):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT product_name, stock_count FROM products WHERE business_id = %s;", (biz_id,))
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows

    @staticmethod
    def get_shop_analytics(biz_id):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT COALESCE(SUM(amount), 0) as total_sales FROM income WHERE business_id = %s;", (biz_id,))
        sales = cur.fetchone()
        cur.execute("SELECT COUNT(*) as total_orders FROM orders WHERE business_id = %s;", (biz_id,))
        orders = cur.fetchone()
        cur.close(); conn.close()
        return {"sales": sales['total_sales'], "orders": orders['total_orders']}
