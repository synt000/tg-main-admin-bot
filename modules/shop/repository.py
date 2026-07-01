from core.database import get_db_connection

class ShopRepository:
    # 👥 Phase 1: Customer CRUD Engine
    @staticmethod
    def db_register_customer(biz_id, name, phone, address):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO customers (business_id, name, phone, address) VALUES (%s, %s, %s, %s) ON CONFLICT (phone) DO UPDATE SET name = EXCLUDED.name, address = EXCLUDED.address;", (biz_id, name, phone, address))
        conn.commit(); cur.close(); conn.close()
        return True

    @staticmethod
    def db_get_customer_profile(biz_id, phone):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT name, phone, address, total_orders, total_spending FROM customers WHERE phone = %s AND business_id = %s;", (phone, biz_id))
        row = cur.fetchone(); cur.close(); conn.close()
        return row

    @staticmethod
    def db_delete_customer(biz_id, phone):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE phone = %s AND business_id = %s;", (phone, biz_id))
        conn.commit(); cur.close(); conn.close()
        return True

    # 🧾 Orders Status & Timelines
    @staticmethod
    def db_update_order_status(biz_id, order_id, new_status):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("UPDATE orders SET delivery_status = %s WHERE order_id = %s AND business_id = %s;", (new_status, order_id, biz_id))
        conn.commit(); cur.close(); conn.close()
        return True

    @staticmethod
    def db_get_timeframe_sales(biz_id, days_back=1):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT COALESCE(SUM(amount), 0) as sales FROM income WHERE business_id = %s AND created_at >= NOW() - INTERVAL '%s day';", (biz_id, days_back))
        row = cur.fetchone(); cur.close(); conn.close()
        try: return row['sales'] if row['sales'] else 0
        except: return row if row else 0
