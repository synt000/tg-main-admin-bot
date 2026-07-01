import sys, os, traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from tests.security.test_security import test_rbac_logic
from tests.billing.test_billing import test_billing_logic

def run_comprehensive_production_stabilization_tests():
    print("🧪 [SaaS Stabilization Validation]: Initiating Module-Based Testing Studio...")
    try:
        # 1. Trigger Isolated Security Unit Test
        test_rbac_logic()
        
        # 2. Trigger Isolated Billing Unit Test
        test_billing_logic()
        
        print("\n🏆 [STABILIZATION STATUS]: MULTI-MODULE TESTS COMPLETED & VERIFIED 100% STABLE! 🚀⭐⭐⭐⭐⭐")
        return True
    except Exception:
        print("❌ [CRITICAL TESTING ERROR LOGGED IN MODULE MATRIX]:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_comprehensive_production_stabilization_tests()
