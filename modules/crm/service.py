from core.database import get_db_connection

class CRMService:
    @staticmethod
    def create_customer(biz_id, name, phone):
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT customer_id FROM customers
            WHERE business_id=%s AND phone=%s;
        """, (biz_id, phone))
        exists = cur.fetchone()

        if exists:
            cur.close()
            conn.close()
            try: return exists[0]
            except: return exists

        cur.execute("""
            INSERT INTO customers (business_id, name, phone)
            VALUES (%s, %s, %s);
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
            SELECT customer_id, name, phone, total_spent, loyalty_points, tier
            FROM customers
            WHERE business_id=%s AND customer_id=%s;
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
            VALUES (%s, %s, %s, %s, %s);
        """, (customer_id, biz_id, module, action, amount))
        conn.commit()
        cur.close()
        conn.close()
        return True

    # 🚀 🔒 [FIX APPLIED 1]: အစ်ကို ညွှန်ကြားထားသည့် update_customer_stats အား ကွက်တိ ဖြည့်စွက်ခြင်း
    @staticmethod
    def update_customer_stats(biz_id, customer_id, amount):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE customers
            SET total_spent = COALESCE(total_spent, 0) + %s
            WHERE business_id=%s AND customer_id=%s;
        """, (amount, biz_id, customer_id))
        conn.commit()
        cur.close()
        conn.close()
        return True

    # 🚀 🔒 [FIX APPLIED 2]: အစ်ကို ညွှန်ကြားထားသည့် update_loyalty + Dynamic Tier Recalculation ပါဝင်သော Master Core
    @staticmethod
    def update_loyalty(biz_id, customer_id, amount):
        conn = get_db_connection()
        cur = conn.cursor()
        points = int(amount / 1000)

        cur.execute("""
            UPDATE customers
            SET loyalty_points = COALESCE(loyalty_points, 0) + %s
            WHERE business_id=%s AND customer_id=%s;
        """, (points, biz_id, customer_id))

        cur.execute("""
            SELECT total_spent FROM customers
            WHERE business_id=%s AND customer_id=%s;
        """, (biz_id, customer_id))
        row = cur.fetchone()
        
        try: spent = float(row[0])
        except: spent = 0.0

        if spent >= 20000: tier = "VIP"
        elif spent >= 5000: tier = "Gold"
        elif spent >= 1000: tier = "Silver"
        else: tier = "Regular"

        cur.execute("""
            UPDATE customers
            SET tier=%s
            WHERE business_id=%s AND customer_id=%s;
        """, (tier, biz_id, customer_id))

        conn.commit()
        cur.close()
        conn.close()
        return {"points": points, "tier": tier}
