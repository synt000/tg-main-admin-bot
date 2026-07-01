from core.database import get_db_connection

class AuditLogger:
    @staticmethod
    def log_action(biz_id, user_id, action, details, ip="127.0.0.1"):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO audit_logs (business_id, user_id, action, details, ip_address)
            VALUES (%s, %s, %s, %s, %s);
        """, (biz_id, user_id, action, details, ip))
        conn.commit(); cur.close(); conn.close()
        return True

    @staticmethod
    def trigger_system_alert(biz_id, alert_type, message):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO telegram_alerts (business_id, alert_type, message)
            VALUES (%s, %s, %s);
        """, (biz_id, alert_type, message))
        conn.commit(); cur.close(); conn.close()
        return True
