import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Bot မပွင့်မီ Database Table များကို အလိုအလျောက် တည်ဆောက်ခိုင်းခြင်း
try:
    from core.database import init_ecommerce_db
    init_ecommerce_db()
    print("🛒 Database tables initialized successfully before startup!")
except Exception as e:
    print(f"⚠️ Database initialization failed: {e}")

from main_bot.main import app as user_app
from admin_bot.main import app as admin_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

combined_app = DispatcherMiddleware(user_app, {
    '/admin-webhook': admin_app
})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    run_simple("0.0.0.0", port, combined_app, use_reloader=False, use_debugger=False)
