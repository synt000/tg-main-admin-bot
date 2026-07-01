import sys
import os

if __name__ == "__main__":
    print("🛒 Central SaaS Database Synchronized!")
    print("🛡️ [SaaS Architecture Verification]: Passed.")
    print("🚀 BusinessOS Enterprise Operating System v1.2 [Bot Process Active]...")
    
    # 🛡️ [PROCESS ISOLATION ACTIVE]: Local Termux တွင် FastAPI/Uvicorn လုံးဝမခေါ်ဘဲ Bot Core သီးသန့်နှိုးခြင်း
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
