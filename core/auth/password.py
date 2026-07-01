import hashlib

class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        # Termux Component Environment Safe SHA256 Salted Hashing Standard
        salt = "SaaS_Enterprise_Salt_v12"
        hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return hashed

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordManager.hash_password(plain_password) == hashed_password
