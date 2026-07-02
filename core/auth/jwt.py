import base64
import json
import hmac
import hashlib
import time
from config.settings import AppConfig

class JWTManager:
    SECRET_KEY = AppConfig.SECRET_KEY if AppConfig.SECRET_KEY else "fallback-secret-key-64-char-token-guard"

    @staticmethod
    def generate_token(data: dict, expires_in: int = 3600) -> str:
        # Standard Lightweight JSON Web Token Generator for Cross-Platform Performance
        header = {"alg": "HS256", "typ": "JWT"}
        payload = data.copy()
        payload["exp"] = int(time.time()) + expires_in
        
        encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
        encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        
        signature_base = f"{encoded_header}.{encoded_payload}".encode()
        signature = hmac.new(JWTManager.SECRET_KEY.encode(), signature_base, hashlib.sha256).digest()
        encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip("=")
        
        return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            parts = token.split(".")
            if len(parts) != 3: return None
            
            encoded_header, encoded_payload, encoded_signature = parts
            signature_base = f"{encoded_header}.{encoded_payload}".encode()
            
            # Verify Signature Cryptographically
            expected_signature = hmac.new(JWTManager.SECRET_KEY.encode(), signature_base, hashlib.sha256).digest()
            actual_signature = base64.urlsafe_b64decode(encoded_signature + "==")
            
            if not hmac.compare_digest(expected_signature, actual_signature): return None
            
            payload = json.loads(base64.urlsafe_b64decode(encoded_payload + "==").decode())
            if payload.get("exp", 0) < int(time.time()): return None # Expired Check
            return payload
        except Exception:
            return None
