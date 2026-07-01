from core.database import get_db_connection

class BillingService:
    # 🔒 Webhook Idempotency Check & Server-Side Verification Secure Logic
    @staticmethod
    def process_verified_payment_webhook(biz_id, plan, provider, reference, amount):
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. 🛡️ Idempotency Verification: ဤ reference စာရင်း ရှိပြီးသားလား အရင်ဆုံး စစ်ဆေးခြင်း
        cur.execute("SELECT id FROM payment_transactions WHERE transaction_reference = %s;", (reference,))
        exists = cur.fetchone()
        
        if exists:
            cur.close(); conn.close()
            return False, "Duplicate Webhook Blocked (Idempotency Active)"
            
        # 2. 🧾 Record Audit Transaction Log
        cur.execute("""
            INSERT INTO payment_transactions (business_id, provider, amount, status, transaction_reference)
            VALUES (%s, %s, %s, 'SUCCESS', %s);
        """, (biz_id, provider, amount, reference))
        
        # 3. ✨ Automatically Activate Plan & Unlock Premium Features
        cur.execute("""
            INSERT INTO subscriptions (business_id, plan, status, provider, payment_reference, end_date)
            VALUES (%s, %s, 'ACTIVE', %s, %s, NOW() + INTERVAL '30 day');
        """, (biz_id, plan, provider, reference))
        
        conn.commit()
        cur.close(); conn.close()
        return True, "Subscription Activated Successfully"

    @staticmethod
    def get_subscription_status(biz_id):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT plan, status FROM subscriptions WHERE business_id = %s ORDER BY id DESC LIMIT 1;", (biz_id,))
        row = cur.fetchone(); cur.close(); conn.close()
        return row

    @staticmethod
    def require_plan(biz_plan, required):
        plans = ["FREE", "PRO", "ENTERPRISE"]
        if isinstance(biz_plan, tuple):
            try: biz_plan = biz_plan[0]
            except: biz_plan = "FREE"
        if biz_plan not in plans: biz_plan = "FREE"
        if plans.index(biz_plan) < plans.index(required):
            raise Exception("Upgrade required: Current tier privileges insufficient.")
        return True
