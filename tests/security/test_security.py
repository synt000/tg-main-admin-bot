import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.security.rbac import require_permission

def test_rbac_logic():
    print("🧪 [Security Layer Test]: Verifying Authorization permissions...")
    assert require_permission("ADMIN", "crm") is True
    print("✅ Security RBAC Verification: PASS")

if __name__ == "__main__": test_rbac_logic()
