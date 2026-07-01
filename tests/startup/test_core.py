import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import AppConfig
from core.database import get_db_connection
from core.logger import SystemLogger

def run_production_unit_tests():
    print("🧪 Running Startup Infrastructure Validation Tests...")
    try:
        # 1. Config Import စစ်ဆေးခြင်း
        AppConfig.validate()
        print("✅ [PASS]: AppConfig context variables validation successful.")
        
        # 2. Database Connection အစစ်အမှန် မိမမိ စစ်ဆေးခြင်း
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close(); conn.close()
        print("✅ [PASS]: PostgreSQL Connection Pool link established perfectly.")
        
        # 3. Logger Initialize ဖြစ်မဖြစ် စစ်ဆေးခြင်း
        SystemLogger.log("STARTUP", "System infrastructure unit tests verified clean.")
        print("✅ [PASS]: SystemLogger stream initial write success.")
        return True
    except Exception as e:
        print(f"❌ [FAIL]: Startup Infrastructure Aborted: {e}")
        return False

if __name__ == "__main__":
    run_production_unit_tests()
