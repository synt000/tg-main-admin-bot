from core.database import get_db_connection

class BillingService:
    @staticmethod
    def create_subscription(biz_id, plan):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO subscriptions (business_id, plan, status, end_date)
            VALUES (%s, %s, 'ACTIVE', NOW() + INTERVAL '30 day');
        """, (biz_id, plan))
        conn.commit()
        cur.close()
        conn.close()
        return True

    @staticmethod
    def get_subscription_status(biz_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT plan, status FROM subscriptions 
            WHERE business_id = %s ORDER BY id DESC LIMIT 1;
        """, (biz_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    # 🔒 3. [FEATURE GATE APPLIED]: အစ်ကို ညွှန်ကြားထားသည့် သံမဏိ Plan Access Checking Logic
    @staticmethod
    def require_plan(biz_plan, required):
        plans = ["FREE", "PRO", "ENTERPRISE"]
        # Convert tuple row to raw string if passed from database cursor
        if isinstance(biz_plan, tuple): 
            try: biz_plan = biz_plan[0]
            except: biz_plan = "FREE"
            
        if biz_plan not in plans: biz_plan = "FREE"
        
        if plans.index(biz_plan) < plans.index(required):
            raise Exception("Upgrade required: Current tier privileges insufficient.")
        return True

    # 🤖 5. Telegram Billing Command Wrapper
    @staticmethod
    def buy_pro_plan(biz_id):
        return BillingService.create_subscription(biz_id, "PRO")
