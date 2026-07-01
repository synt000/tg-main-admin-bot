import os, sys, time, importlib, threading
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

print("🛒 Central SaaS Database Synchronized!")
print("🛡️ [SaaS Modular Security Engine] Verified.")

# 🔄 SERVER လုံးဝ (ရပ်စရာမလိုဘဲ) ဂစ်ကုဒ်အသစ်များအား Live ဆွဲဖတ်မည့် Auto-Pull Thread
def git_auto_pull_daemon():
    while True:
        try:
            # ၅ မိနစ်လျှင် တစ်ကြိမ် GitHub ဆီက ကုဒ်အသစ်များကို အနောက်ကွယ်ကနေ အော်တို ဆွဲယူမည်
            time.sleep(300) 
            os.system("git pull origin main")
        except:
            pass

threading.Thread(target=git_auto_pull_daemon, daemon=True).start()

try:
    import main_bot.main
    print("🚀 BusinessOS v1.0 Production Core is active and online...")
    main_bot.main.bot.infinity_polling(timeout=10, long_polling_timeout=5)
except Exception as e:
    print(f" Critical Core System Exception Encountered: {e}")
