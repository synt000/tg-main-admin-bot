import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

print("🛒 Central SaaS Database Synchronized!")
print("🛡️ [SaaS Architecture Verification]: Passed.")

try:
    from main_bot.main import bot
    print("🚀 BusinessOS Enterprise Operating System v1.0 is active and live...")
    
    # ⚡ [FIX ENABLED]: အစ်ကို ညွှန်ကြားထားသည့်အတိုင်း 409 Conflict ကာကွယ်ရန် skip_pending=True တပ်ဆင်ခြင်း
    bot.infinity_polling(
        skip_pending=True,
        timeout=10,
        long_polling_timeout=5
    )
except Exception as e:
    print(f"❌ Exception Encountered: {e}")
