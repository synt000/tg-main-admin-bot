from core.database import get_db_connection

class CRMDashboard:
    @staticmethod
    def get_customer_profile(biz_id, customer_id):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT customer_id, name, phone, total_spent, loyalty_points, tier
            FROM customers
            WHERE business_id=%s AND customer_id=%s;
        """, (biz_id, customer_id))
        customer = cur.fetchone()

        cur.execute("""
            SELECT module, action, amount, created_at
            FROM customer_activity
            WHERE business_id=%s AND customer_id=%s
            ORDER BY created_at DESC;
        """, (biz_id, customer_id))
        activity = cur.fetchall()

        cur.close()
        conn.close()

        return {
            "profile": customer,
            "activity_timeline": activity
        }

    @staticmethod
    def get_top_customers(biz_id, limit=5):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT customer_id, name, total_spent, tier
            FROM customers
            WHERE business_id=%s
            ORDER BY total_spent DESC
            LIMIT %s;
        """, (biz_id, limit))
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows

    @staticmethod
    def get_business_summary(biz_id):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                COUNT(*) as total_customers,
                COALESCE(SUM(total_spent), 0) as revenue,
                COALESCE(SUM(loyalty_points), 0) as total_points
            FROM customers
            WHERE business_id=%s;
        """, (biz_id,))
        summary = cur.fetchone()

        cur.close()
        conn.close()
        return summary
