import os

MAIN_BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

DATABASE = "database.db"
