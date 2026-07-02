import sys, os
from datetime import datetime
from core.database import get_db_connection, release_db_connection

class DashboardAnalyticsService:
    @staticmethod
    def get_enterprise_global_analytics(business_id: str = None) -> dict:
        conn = get_db_connection()
        cur = conn.cursor()
        today_date_str = datetime.now().strftime("%Y-%m-%d")
        
        try:
            # 🎯 1. Dynamic total_merchants
            cur.execute("SELECT COALESCE(COUNT(*), 0) FROM tenants;")
            res = cur.fetchone()
            total_merchants = res[0] if isinstance(res, tuple) else (res.get("count", 0) if hasattr(res, "get") else res) if res else 0

            # 🎯 2. Dynamic total_customers
            if business_id:
                cur.execute("SELECT COALESCE(COUNT(*), 0) FROM customers WHERE business_id = %s;", (business_id,))
            else:
                cur.execute("SELECT COALESCE(COUNT(*), 0) FROM customers;")
            res = cur.fetchone()
            total_customers = res[0] if isinstance(res, tuple) else (res.get("count", 0) if hasattr(res, "get") else res) if res else 0

            # 🎯 3. Dynamic active_subscriptions
            cur.execute("SELECT COALESCE(COUNT(*), 0) FROM subscriptions WHERE status = %s;", ("active",))
            res = cur.fetchone()
            active_subscriptions = res[0] if isinstance(res, tuple) else (res.get("count", 0) if hasattr(res, "get") else res) if res else 0

            # 🎯 4. Dynamic total_orders
            if business_id:
                cur.execute("SELECT COALESCE(COUNT(*), 0) FROM orders WHERE business_id = %s;", (business_id,))
            else:
                cur.execute("SELECT COALESCE(COUNT(*), 0) FROM orders;")
            res = cur.fetchone()
            total_orders = res[0] if isinstance(res, tuple) else (res.get("count", 0) if hasattr(res, "get") else res) if res else 0

            # 🎯 5. Dynamic total_revenue
            if business_id:
                cur.execute("""
                    SELECT COALESCE(SUM(amount), 0.00) 
                    FROM payment_transactions 
                    WHERE status = %s AND business_id = %s;
                """, ("success", business_id))
            else:
                cur.execute("SELECT COALESCE(SUM(amount), 0.00) FROM payment_transactions WHERE status = %s;", ("success",))
            res = cur.fetchone()
            total_revenue = float(res[0] if isinstance(res, tuple) else (res.get("sum", 0.00) if hasattr(res, "get") else res) if res else 0.00)

            # 🎯 6. Dynamic today_revenue
            if business_id:
                cur.execute("""
                    SELECT COALESCE(SUM(amount), 0.00) 
                    FROM payment_transactions 
                    WHERE status = %s AND business_id = %s AND created_at::text LIKE %s;
                """, ("success", business_id, f"{today_date_str}%"))
            else:
                cur.execute("""
                    SELECT COALESCE(SUM(amount), 0.00) 
                    FROM payment_transactions 
                    WHERE status = %s AND created_at::text LIKE %s;
                """, ("success", f"{today_date_str}%"))
            res = cur.fetchone()
            today_revenue = float(res[0] if isinstance(res, tuple) else (res.get("sum", 0.00) if hasattr(res, "get") else res) if res else 0.00)

            cur.close()
            release_db_connection(conn)

            return {
                "status": "success",
                "metrics": {
                    "total_merchants": int(total_merchants),
                    "total_customers": int(total_customers),
                    "active_subscriptions": int(active_subscriptions),
                    "total_orders": int(total_orders),
                    "total_revenue": float(total_revenue),
                    "today_revenue": float(today_revenue)
                },
                "version": "1.2.0"
            }

        except Exception as query_fault_ex:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): release_db_connection(conn)
            # 🛡️ Native local exception fallback structure that easily bridges into cloud layers
            raise RuntimeError(f"Live Analytical transactional data compilation failed: {str(query_fault_ex)}")
