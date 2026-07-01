import os, sys, telebot
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN: raise RuntimeError("BOT_TOKEN not found in .env")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# 🏢 CONNECT MIDDLEWARES PIPELINE (အစ်ကို ညွှန်ကြားထားသည့် စံနှုန်းစီးဆင်းမှုတံခါးစောင့်)
from middlewares.license_gate import LicenseMiddleware

@bot.middleware_handler(update_types=['message', 'callback_query'])
def run_business_os_middlewares(bot_instance, update):
    uid = None
    if update.message: uid = str(update.message.from_user.id)
    elif update.callback_query: uid = str(update.callback_query.from_user.id)
    
    if uid:
        # Flow 1: ⏳ License Check (၃ ရက် Trial ကုန်ဆုံးမှု စစ်ဆေးခြင်း)
        is_licensed = LicenseMiddleware.verify_tenant_access(uid)
        if not is_licensed:
            # လိုင်စင်မရှိပါက Handler ဆီမလွှတ်ဘဲ တိုက်ရိုက် ကြားဖြတ် ပိတ်ချခြင်း
            if update.message:
                bot_instance.send_message(update.message.chat.id, "🔒 **[Access Denied]**: Trial Expired. Please register valid license key.")
            return False
            
        # Flow 2: 👥 Permission Check (ဆောက်ရန်အဆင်သင့် Interface ခံထားခြင်း)
        pass 
        
    return True # Flow 3: 🏁 သတ်မှတ်ချက်များ ကိုက်ညီပါက Handler ဆီသို့ သန့်ရှင်းစွာ လမ်းဖွင့်ပေးခြင်း

from main_bot.handlers.home import register_home_handlers
from main_bot.callbacks.home import register_home_callbacks

register_home_handlers(bot)
register_home_callbacks(bot)

if __name__ == "__main__":
    print("🚀 BusinessOS Multi-Layer Middleware Router Engine Online...")
