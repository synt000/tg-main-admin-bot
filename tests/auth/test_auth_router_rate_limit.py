import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from dashboard.app import app

client = TestClient(app)

# =================────────────────────────────────────────
# 🧪 TEST 7: Empty Data Payload Validation Handling (Expected to Fail on Static Code)
# =================────────────────────────────────────────
def test_login_empty_payload_returns_422():
    # Send standard unprocessable payload formatting context
    response = client.post("/auth/login", json={"username": "", "password": ""})
    
    # TDD Expectation: Current static/unprotected handler passes blanks through, 
    # but strict architecture demands an automated 422 payload execution blocking.
    assert response.status_code == 422
