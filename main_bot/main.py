import os, sys, telebot
from dotenv import load_dotenv
from telebot import apihelper

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(base_dir, ".env"))

sys.path.append(base_dir)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN: 
    raise RuntimeError("CRITICAL: BOT_TOKEN not found in environment settings.")

# 🔒 TeleBot မတိုင်ခင် Middleware စနစ်အား ကမ္ဘာ့စံနှုန်းအတိုင်း သံမဏိဖွင့်လှစ်ခြင်း
apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# 🏢 CONNECT MIDDLEWARES PIPELINE (တံခါးစောင့်စနစ် Middleware Logic မှန်ကန်စွာ ပြုပြင်ခြင်း)
from middlewares.license_gate import LicenseMiddleware

@bot.middleware_handler(update_types=['message', 'callback_query'])
def run_business_os_middlewares(bot_instance, update):
    uid = None
    # 💡 FIX: update ထဲတွင် message/callback_query က တိုက်ရိုက် object အဖြစ် ဝင်လာခြင်းကို စစ်ဆေးခြင်း
    if isinstance(update, telebot.types.Message):
        uid = str(update.from_user.id)
    elif isinstance(update, telebot.types.CallbackQuery):
        uid = str(update.from_user.id)
    
    if uid:
        # Flow 1: ⏳ License Check (၃ ရက် Trial ကုန်ဆုံးမှု စစ်ဆေးခြင်း)
        is_licensed = LicenseMiddleware.verify_tenant_access(uid)
        if not is_licensed:
            if isinstance(update, telebot.types.Message):
                bot_instance.send_message(update.chat.id, "🔒 **[Access Denied]**: Trial Expired. Please register valid license key.")
            return False
            
    return True

from main_bot.handlers.home import register_home_handlers
from main_bot.callbacks.home import register_home_callbacks

register_home_handlers(bot)
register_home_callbacks(bot)

if __name__ == "__main__":
    print("🚀 BusinessOS Multi-Layer Middleware Router Engine Online...")
