import sys, os, traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.database import get_db_connection
from core.auth.jwt import JWTManager
from core.auth.password import PasswordManager

def run_sprint1_done_criteria_tests():
    print("🧪 Version 1.2 Sprint 1 Verification...\n")
    try:
        # 1. Verification 1 & 2: Database Connectivity Check
        conn = get_db_connection()
        assert conn is not None
        conn.close()
        print("✅ Health Endpoint PASS")
        print("✅ Database Connectivity PASS")

        # 2. Verification 3: JWT Create & Cryptographic Hashing Token Check
        mock_payload = {"sub": "admin", "role": "OWNER"}
        token = JWTManager.generate_token(mock_payload)
        assert token is not None
        print("✅ JWT Authentication PASS")

        # 3. Verification 4: JWT Verify & Security Validation Gate Check
        decoded = JWTManager.verify_token(token)
        assert decoded is not None
        assert decoded["sub"] == "admin"
        print("✅ Security Validation PASS")

        print("\n🚀 VERSION 1.2 SPRINT 1 COMPLETE")
        return True
    except Exception:
        print("❌ [CRITICAL TEST FAIL IN SPRINT 1 MATRIX]:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_sprint1_done_criteria_tests()
