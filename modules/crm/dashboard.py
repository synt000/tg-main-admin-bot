import sys, os
from datetime import datetime
from fastapi import HTTPException, status
from core.database import get_db_connection, release_db_connection

class CRMDashboard:
    # 🚀 📊 [SOLID LIVE ANALYTICS ENGINE ACTIVE]: Mock အဟောင်းများအား ရာနှုန်းပြည့်ဖယ်ရှား၍ Live DB Queries ဖြင့် တည်ဆောက်ခြင်း
    @staticmethod
    def get_enterprise_global_analytics(business_id: str = None) -> dict:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Capture precise timestamp limits dynamically for today's automated revenue auditing
        today_date_str = datetime.now().strftime("%Y-%m-%d")
        
        try:
            # 🎯 1. Dynamic Merchant Count from tenants table safely
            cur.execute("SELECT COALESCE(COUNT(*), 0) FROM tenants;")
            total_merchants = cur.fetchone()[0] if hasattr(cur, "fetchone") else 0

            # 🎯 2. Dynamic Customer Count from customers table safely
            if business_id:
                cur.execute("SELECT COALESCE(COUNT(*), 0) FROM customers WHERE business_id = %s;", (business_id,))
            else:
                cur.execute("SELECT COALESCE(COUNT(*), 0) FROM customers;")
            total_customers = cur.fetchone()[0] if hasattr(cur, "fetchone") else 0

            # 🎯 3. Dynamic Active Subscriptions counting boundaries
            cur.execute("SELECT COALESCE(COUNT(*), 0) FROM subscriptions WHERE status = %s;", ("active",))
            active_subscriptions = cur.fetchone()[0] if hasattr(cur, "fetchone") else 0

            # 🎯 4. Dynamic Order Statistics transaction records counts
            if business_id:
                cur.execute("SELECT COALESCE(COUNT(*), 0) FROM orders WHERE business_id = %s;", (business_id,))
            else:
                cur.execute("SELECT COALESCE(COUNT(*), 0) FROM orders;")
            total_orders_count = cur.fetchone()[0] if hasattr(cur, "fetchone") else 0

            # 🎯 5. Dynamic Total Revenue parameter computation from transactional layers
            if business_id:
                cur.execute("""
                    SELECT COALESCE(SUM(amount), 0.00) 
                    FROM payment_transactions 
                    WHERE status = %s AND business_id = %s;
                """, ("success", business_id))
            else:
                cur.execute("SELECT COALESCE(SUM(amount), 0.00) FROM payment_transactions WHERE status = %s;", ("success",))
            total_revenue = float(cur.fetchone()[0]) if hasattr(cur, "fetchone") else 0.00

            # 🎯 6. Dynamic Today's Revenue parameters checking securely via Parameterized constraints
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
            today_revenue = float(cur.fetchone()[0]) if hasattr(cur, "fetchone") else 0.00

            # Clean transaction connections layers context cleanly prior to release locks
            cur.close()
            release_db_connection(conn)

            # Compile and dispatch final explicit unified architecture payload specification
            return {
                "status": "success",
                "metrics": {
                    "total_merchants": int(total_merchants),
                    "total_customers": int(total_customers),
                    "active_subscriptions": int(active_subscriptions),
                    "total_orders_count": int(total_orders_count),
                    "total_revenue_mmk": float(total_revenue),
                    "today_revenue_mmk": float(today_revenue)
                },
                "version": "1.2.0"
            }

        except Exception as query_fault_ex:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): release_db_connection(conn)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Live Analytical transactional data compilation failed: {str(query_fault_ex)}"
            )
