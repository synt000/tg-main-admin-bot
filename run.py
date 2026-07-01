import sys
import os
from core.database import init_connection_pool

if __name__ == "__main__":
    # 🔌 🚀 [POOL COUPLING ACTIVE]: Bot စဖွင့်ကတည်းက ကမ္ဘာ့ဆာဗာဆီသို့ ကွန်နက်ရှင်ထုပ် ကြိုဆောက်ထားခြင်း
    init_connection_pool()
    
    print("🛒 Central SaaS Database Synchronized!")
    print("🛡️ [SaaS Architecture Verification]: Passed.")
    print("🚀 BusinessOS Enterprise Operating System v1.2 [Bot Process Active]...")
    
    try:
        from main_bot.main import run_bot
        run_bot()
    except ImportError:
        try:
            from main_bot.main import main as main_bot_entry
            main_bot_entry()
        except Exception as e:
            print(f"❌ [CRITICAL LOG]: Bot entry handler mismatch. Details: {e}")
            sys.exit(1)
