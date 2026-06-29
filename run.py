import threading
import os
from main_bot.main import app as user_app
from admin_bot.main import app as admin_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

combined_app = DispatcherMiddleware(user_app, {
    '/admin': admin_app
})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    run_simple("0.0.0.0", port, combined_app, use_reloader=False, use_debugger=False)
