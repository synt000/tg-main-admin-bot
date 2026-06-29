import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

MAIN_BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 0))
DATABASE = os.getenv("DATABASE")

# 🔥 safety check
if not MAIN_BOT_TOKEN:
    raise Exception("MAIN_BOT_TOKEN missing in .env")

if not ADMIN_BOT_TOKEN:
    raise Exception("ADMIN_BOT_TOKEN missing in .env")
