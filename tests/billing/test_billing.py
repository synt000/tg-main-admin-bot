import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from modules.billing.service import BillingService

def test_billing_logic():
    print("🧪 [Billing Layer Test]: Verifying subscription token controls...")
    assert BillingService.require_plan("PRO", "PRO") is True
    print("✅ Billing Subscription Logic: PASS")

if __name__ == "__main__": test_billing_logic()
