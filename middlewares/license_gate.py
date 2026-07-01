from datetime import datetime
from core.database import get_db_connection
from core.logger import SystemLogger

class LicenseMiddleware:
    @staticmethod
    def verify_tenant_access(uid):
        try:
            conn = get_db_connection(); cur = conn.cursor()
            cur.execute("SELECT expires_at FROM licenses WHERE merchant_id = %s AND key_type = 'trial';", (uid,))
            row = cur.fetchone()
            cur.close(); conn.close()
            
            if row and datetime.now() > row[0]:
                SystemLogger.log("LICENSE", f"Access Denied: Tenant {uid} trial has expired.")
                return False
            return True
        except Exception as e:
            SystemLogger.log("ERROR", f"Middleware Exception: {e}")
            return True
