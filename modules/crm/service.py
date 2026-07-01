from core.database import get_db_connection

class CRMService:
    @staticmethod
    def create_customer(biz_id, name, phone):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO customers (business_id, name, phone)
            VALUES (%s, %s, %s)
        """, (biz_id, name, phone))
        conn.commit()
        cur.close()
        conn.close()
        return True

    @staticmethod
    def get_customer(biz_id, customer_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT customer_id, name, phone, total_spent, loyalty_points
            FROM customers
            WHERE business_id=%s AND customer_id=%s
        """, (biz_id, customer_id))
        data = cur.fetchone()
        cur.close()
        conn.close()
        return data

    @staticmethod
    def add_activity(biz_id, customer_id, module, action, amount=0):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO customer_activity
            (customer_id, business_id, module, action, amount)
            VALUES (%s, %s, %s, %s, %s)
        """, (customer_id, biz_id, module, action, amount))
        conn.commit()
        cur.close()
        conn.close()
        return True
