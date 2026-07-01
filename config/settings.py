import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise RuntimeError("CRITICAL: BOT_TOKEN is missing inside Environment Context.")
