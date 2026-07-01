import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import AppConfig

def run_startup_unit_tests():
    print("🧪 Running Startup Infrastructure Validation Tests...")
    try:
        AppConfig.validate()
        print("✅ [PASS]: Environment variables syntax validation successful.")
        return True
    except Exception as e:
        print(f"❌ [FAIL]: Startup Validation Failed: {e}")
        return False

if __name__ == "__main__":
    run_startup_unit_tests()
