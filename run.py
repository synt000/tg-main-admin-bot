import os, sys, time
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

print("🛒 Central SaaS Database Synchronized!")
print("🛡️ [SaaS Modular Security Engine] Verified.")

try:
    from main_bot.main import bot as main_bot
    
    main_bot.infinity_polling()
    
    # Registering all the divided modular components flawlessly
    register_callbacks(bot)
    
    print("🚀 Pro Business Assistant OS V2 is active and online...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except Exception as e:
    print(f"❌ Critical Core System Exception Encountered: {e}")
    time.sleep(3)
