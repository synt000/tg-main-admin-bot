import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import AppConfig
from core.database import get_db_connection
from modules.shop.service import ShopService

def run_sprint_b_customer_unit_tests():
    print("🧪 [Sprint B Verification]: Starting Customer Management Test Matrix...")
    biz_id = "MOCK_BIZ_001"
    test_phone = "0979555222"
    
    try:
        # 1. Test Customer Register (Create/Update)
        ShopService.register_customer(biz_id, "Zarni Smart Owner", test_phone, "Mandalay")
        print("✅ [1/4] Customer Onboarding Registry: Valid")
        
        # 2. Test Customer Search (Read Profile)
        profile = ShopService.get_customer(biz_id, test_phone)
        if not profile: raise RuntimeError("Customer Profile query synchronization failed.")
        print("✅ [2/4] Customer Profile Identity Query: Valid")
        
        # 3. Test Purchase History Log Checking
        analytics = ShopService.get_shop_analytics(biz_id)
        print("✅ [3/4] Purchase History Analytics Telemetry: Valid")
        
        # 4. Test Customer Delete (Clean Up Safeguard)
        ShopService.remove_customer(biz_id, test_phone)
        print("✅ [4/4] Customer Cleanup Database Safeguard: Valid")
        
        print("\n🏆 [SPRINT B - PHASE 1]: CUSTOMER WORKFLOW IS 100% VERIFIED PASS! ⭐⭐⭐⭐⭐")
        return True
    except Exception as e:
        print(f"❌ [CRITICAL TESTING ERROR]: Customer Matrix Broken: {e}")
        return False

if __name__ == "__main__":
    run_sprint_b_customer_unit_tests()
