# License Module Business Logic Service
from core.database import get_db_connection

class LicenseService:
    @staticmethod
    def provision_trial_license(uid, trial_expiry):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO licenses (license_key, merchant_id, key_type, is_activated, expires_at) "
                "VALUES (%s, %s, 'trial', TRUE, %s) "
                "ON CONFLICT (license_key) DO NOTHING;",
                (f"TRIAL-{uid}", uid, trial_expiry)
            )
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Service Error: {e}")
            return False
