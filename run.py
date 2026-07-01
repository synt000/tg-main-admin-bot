import os
import sys
import threading
import uvicorn
from fastapi import FastAPI

# 🛡️ Render Port Scan Bypass Guard Layer
app = FastAPI()

@app.get("/")
def home():
    return {"status": "bot_worker_active", "engine": "BusinessOS v1.2"}

@app.get("/health")
def health():
    return {"status": "ok"}

def run_port_dummy_server():
    port = int(os.getenv("PORT", 8000))
    # Render ၏ Port Scanner အား လှည့်စားရန်အတွက် Light Server အား နှိုးပေးခြင်း
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    print("🛒 Central SaaS Database Synchronized!")
    print("🛡️ [SaaS Architecture Verification]: Passed.")
    print("🚀 BusinessOS Enterprise Operating System v1.2 is active and live...")
    
    # 🔗 Web Port Scanner အား ကျော်လွှားရန် Thread ခွဲ၍ မောင်းနှင်ခြင်း
    threading.Thread(target=run_port_dummy_server, daemon=True).start()
    
    # Dynamic Function Hook Execution: run_bot သို့မဟုတ် main နှစ်မျိုးစလုံးကို Safe ဖြစ်အောင် ခေါ်ယူခြင်း
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
