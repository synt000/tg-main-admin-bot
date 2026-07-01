import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    # ⚙️ Phase 1 Production Hardening Enforcements
    APP_ENV = os.getenv("APP_ENV", "production")
    SECRET_KEY = os.getenv("SECRET_KEY", "default-64-character-fallback-secret-key-for-local-v1.2")
    
    # 💳 Billing Provider Token Infrastructure
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    # 🤖 Core Platform Contracts
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
