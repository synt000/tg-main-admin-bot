import os, sys, telebot
from dotenv import load_dotenv
from telebot import apihelper

# 🛠️ အစ်ကို ညွှန်ကြားထားသည့်အတိုင်း .env Path အား စိတ်အချရဆုံး Absolute Path အဖြစ် တိတိကျကျ သတ်မှတ်ခြင်း
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(base_dir, ".env"))

sys.path.append(base_dir)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN: 
    raise RuntimeError("CRITICAL: BOT_TOKEN not found in environment settings.")

# 🔒 TeleBot မတိုင်ခင် Middleware စနစ်အား ကမ္ဘာ့စံနှုန်းအတိုင်း သံမဏိဖွင့်လှစ်ခြင်း
apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# 🏢 CONNECT MIDDLEWARES PIPELINE (တံခါးစောင့်စနစ် Middleware)
from middlewares.license_gate import LicenseMiddleware

@bot.middleware_handler(update_types=['message', 'callback_query'])
def run_business_os_middlewares(bot_instance, update):
    uid = None
    if update.message: 
        uid = str(update.message.from_user.id)
    elif update.callback_query: 
        uid = str(update.callback_query.from_user.id)
    
    if uid:
        is_licensed = LicenseMiddleware.verify_tenant_access(uid)
        if not is_licensed:
            if update.message:
                bot_instance.send_message(update.message.chat.id, "🔒 **[Access Denied]**: Trial Expired. Please register valid license key.")
            return False
            
    return True

from main_bot.handlers.home import register_home_handlers
from main_bot.callbacks.home import register_home_callbacks

register_home_handlers(bot)
register_home_callbacks(bot)

if __name__ == "__main__":
    print("🚀 BusinessOS Multi-Layer Middleware Router Engine Online...")
