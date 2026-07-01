from fastapi import FastAPI
from modules.crm.dashboard import CRMDashboard
from modules.ai.assistant import BusinessAI
from web_admin.router import admin_router

app = FastAPI(
    title="BusinessOS Multi-Tenant SaaS Engine", 
    version="1.2.0",
    description="Production-ready Intelligent Business Management API Documentation (v1.2)"
)

# 🔗 🌐 [ROUTER INJECTION]: Web Admin Panel Integration Route
app.include_router(admin_router)

# 🚀 🔒 [PHASE 1 APPLIED]: အစ်ကို ညွှန်ကြားထားသည့် Render Production Health Check Endpoint
@app.get("/health", summary="Perform System Infrastructure Health Check", tags=["Production Hardening"])
def health():
    return {
        "status": "ok",
        "version": "1.2",
        "environment": "production"
    }

@app.get("/business/{biz_id}/summary", summary="Get Financial Sales Summary")
def summary(biz_id: str):
    return CRMDashboard.get_business_summary(biz_id)

@app.get("/business/{biz_id}/insight", summary="Generate AI Business Decision Insight")
def insight(biz_id: str):
    return BusinessAI.generate_business_insight(biz_id)

@app.get("/business/{biz_id}/top-customers", summary="Fetch VIP Customer Leaderboard")
def top(biz_id: str):
    return CRMDashboard.get_top_customers(biz_id)
