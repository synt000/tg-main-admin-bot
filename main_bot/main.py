import os, sys, telebot
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN: raise RuntimeError("BOT_TOKEN not found in .env")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# 🏢 REFACTOR CORES: HANDLERS & CALLBACKS REGISTRY
from main_bot.handlers.home import register_home_handlers
from main_bot.callbacks.home import register_home_callbacks

register_home_handlers(bot)
register_home_callbacks(bot)

if __name__ == "__main__":
    print("🚀 BusinessOS main_bot Dynamic Router Engine Online...")
