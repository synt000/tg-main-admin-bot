import sys, os
from datetime import datetime
from core.database import get_db_connection, release_db_connection

class CronJobEngine:
    # 🚀 🔒 [NATIVE PYTHON CRON ACTIVE]: အစ်ကို ညွှန်ကြားထားသည့်အတိုင်း FastAPI Dependencies များအား အမြစ်ပြတ် ဖြုတ်ချပြီးခြင်း
    @staticmethod
    def find_expired_licenses() -> list:
        # 🎯 Contract 1: သက်တမ်းကုန် Merchant များကို ရှာဖွေခြင်း (Standard Parameterized Check)
        conn = get_db_connection()
        cur = conn.cursor()
        current_time = datetime.now()
        try:
            cur.execute(
                "SELECT business_id, end_date FROM subscriptions WHERE end_date < %s AND status = %s;", 
                (current_time, "active")
            )
            expired_records = cur.fetchall()
            cur.close()
            release_db_connection(conn)
            return expired_records
        except Exception:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): release_db_connection(conn)
            return []

    @staticmethod
    def deactivate_expired_merchants() -> int:
        # 🎯 Contract 2 & 3: SQL Parameterized execution ဖြင့် status အား inactive သို့ ပြောင်းလဲခြင်း
        conn = get_db_connection()
        cur = conn.cursor()
        current_time = datetime.now()
        try:
            cur.execute(
                "UPDATE subscriptions SET status = %s WHERE end_date < %s AND status = %s;", 
                ("inactive", current_time, "active")
            )
            affected_rows = cur.rowcount
            conn.commit()
            cur.close()
            release_db_connection(conn)
            return affected_rows
        except Exception as e:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.rollback(); release_db_connection(conn)
            # HTTPException အစား Standalone RuntimeError ဖြင့် သန့်ရှင်းစွာ ဖြတ်ချခြင်း
            raise RuntimeError(f"Cron Mutation Persistence Failure: {str(e)}")

    @staticmethod
    def run_cron_cycle() -> dict:
        # 🎯 Contract 4: run_cron_cycle() မှ processed, updated, status အပြည့်အစုံပါဝင်သော summary ပြန်ပေးခြင်း
        try:
            expired_list = CronJobEngine.find_expired_licenses()
            processed_count = len(expired_list)
            
            # Execute systemic data states mutations
            updated_rows = CronJobEngine.deactivate_expired_merchants()
            
            return {
                "status": "success",
                "processed": processed_count,
                "affected_rows": updated_rows,
                "message": "License validation cron loop executed cleanly."
            }
        except Exception as ex:
            return {
                "status": "failed",
                "processed": 0,
                "affected_rows": 0,
                "error": str(ex)
            }
