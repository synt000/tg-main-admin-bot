import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from dashboard.app import app

client = TestClient(app)

# =================────────────────────────────────────────
# 🧪 TEST 1: Valid Webhook Request Handling Context
# =================────────────────────────────────────────
@patch("stripe.Webhook.construct_event")
def test_stripe_webhook_valid_request(mock_construct):
    # Simulate dynamic stripe event decoding context safely
    mock_event = MagicMock()
    mock_event.type = "checkout.session.completed"
    mock_event.data.object = {
        "id": "cs_test_mock_session_123",
        "client_reference_id": "MOCK_BIZ_TENANT_999",
        "customer": "cus_mock_user_111"
    }
    mock_construct.return_value = mock_event

    headers = {"stripe-signature": "t=123,v1=mock_cryptographic_signature_hash"}
    payload = {"id": "evt_test_123", "type": "checkout.session.completed"}

    # TDD Expectation: Expected to fail (404/405) before route implementation phase
    response = client.post("/api/v1/payments/webhook", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

# =================────────────────────────────────────────
# 🧪 TEST 2: Invalid HTTP Method Enforcement Boundary (GET Blocking)
# =================────────────────────────────────────────
def test_stripe_webhook_invalid_http_method():
    # Stripe Webhooks MUST strictly accept POST requests only
    response = client.get("/api/v1/payments/webhook")
    assert response.status_code == 405 # Method Not Allowed Enforced

# =================────────────────────────────────────────
# 🧪 TEST 3: Missing Payload Input Boundary Constraints Handling
# =================────────────────────────────────────────
def test_stripe_webhook_missing_payload():
    headers = {"stripe-signature": "t=123,v1=mock_signature"}
    # Send empty request packet query to test input handler boundaries
    response = client.post("/api/v1/payments/webhook", headers=headers)
    assert response.status_code == 422 # Unprocessable Entity Validation Block

# =================────────────────================────────
# 🧪 TEST 4: Missing Stripe Signature Header Security Guard Check
# =================────────────────────────────────────────
def test_stripe_webhook_missing_signature_header():
    payload = {"id": "evt_test_123", "type": "checkout.session.completed"}
    # Send transaction payload without injecting the necessary stripe cryptographic validation tokens
    response = client.post("/api/v1/payments/webhook", json=payload)
    assert response.status_code == 400 # Bad Request Block due to missing security credentials
