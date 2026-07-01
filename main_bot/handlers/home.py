from datetime import datetime, timedelta
from main_bot.keyboards.home import HomeKeyboards
from modules.license.service import LicenseService

def register_home_handlers(bot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        uid = str(message.from_user.id)
        trial_expiry = datetime.now() + timedelta(days=3)
        expiry_str = trial_expiry.strftime('%Y-%m-%d %H:%M:%S')

        # ⚙️ 2. SERVICES LAYER: Business Logic ကို Handler ထဲမှ ထုတ်၍ သီးသန့်ခေါ်ယူခြင်း
        LicenseService.provision_trial_license(uid, trial_expiry)

        welcome_text = (
            f"Welcome to BusinessOS v1.0 🚀\n"
            f"🔥 One Platform. Every Business.\n━━━━━━━━━━━━━━━━━━\n"
            f"Free 3-Day Trial: **Activated ✅**\n"
            f"Valid Until : `{expiry_str}`\n"
            f"Remaining : `3 Days`\n\n"
            f"Manage Everything from Telegram. Select a core workspace:"
        )
        
        # 🏢 1. KEYBOARDS LAYER: Button မာကတ်များကို သီးသန့်ဖိုင်ဆီမှ ဆွဲဖတ်ခြင်း
        bot.send_message(message.chat.id, welcome_text, reply_markup=HomeKeyboards.get_homepage_markup(), parse_mode="Markdown")
