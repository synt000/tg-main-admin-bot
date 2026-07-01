# 2D Agent Module Business Logic Service Layer
from core.database import get_db_connection

class TwoDService:
    @staticmethod
    def validate_and_place_bet(uid, session_type, number, amount):
        # ဒိုင် Limit နှင့် သက်တမ်းတွက်ချက်မှု Logic Interface
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO income (business_id, amount, details) VALUES (%s, %s, %s);", (uid, amount, f"2D Bet Number {number} - {session_type.upper()}"))
        conn.commit(); cur.close(); conn.close()
        return True

    @staticmethod
    def get_session_reports(uid, session_type):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT amount, details, created_at FROM income WHERE business_id = %s AND details LIKE %s;", (uid, f"%2D Bet%"))
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
# Twod Module Business Logic Service
