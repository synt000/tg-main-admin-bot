from fastapi import FastAPI
from core.database import get_db_connection
from core.auth.router import auth_router
from web_admin.router import admin_router

app = FastAPI(title="BusinessOS SaaS", version="1.2.0")

# 🔗 🔐 [AUTH INTEGRATION]: Authentication Router နှင့် Admin Panel အား ချိတ်ဆက်ခြင်း
app.include_router(auth_router)
app.include_router(admin_router)

# 🚀 🗄️ [TASK 1 APPLIED]: Database Connection Checking Connected Health API
@app.get("/health", summary="Perform System Infrastructure Health Check", tags=["Production Hardening"])
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return {
            "status": "ok",
            "database": "connected",
            "version": "1.2.0",
            "environment": "production"
        }
    except Exception as e:
        return {
            "status": "error",
            "database": str(e)
        }
