import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import threading
from main_bot.main import app as user_app
from admin_bot.main import app as admin_app
from admin_bot.main import ADMIN_TOKEN
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# URL လမ်းကြောင်း ဂျီကျမှုကို ဖြေရှင်းရန်အတွက် Admin Logic ကို သီးသန့် ခွဲထုတ်ခြင်း
# /admin-webhook-<token> ပုံစံမျိုးဖြင့် Telegram က လက်ခံနိုင်မည့် တိုက်ရိုက် URL ဖြစ်အောင် ပြောင်းလဲခြင်း
admin_path = f'/admin-webhook-{ADMIN_TOKEN}'

combined_app = DispatcherMiddleware(user_app, {
    admin_path: admin_app
})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    run_simple("0.0.0.0", port, combined_app, use_reloader=False, use_debugger=False)
