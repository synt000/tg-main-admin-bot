from fastapi import FastAPI
from modules.crm.dashboard import CRMDashboard
from modules.ai.assistant import BusinessAI
from web_admin.router import admin_router

app = FastAPI(title="BusinessOS Enterprise SaaS Dashboard API", version="1.1")

# 🔗 🌐 [WEB ADMIN PANEL INTEGRATION]: Version 1.1 Router အား ပင်မအူတိုင်ထဲသို့ ချိတ်ဆက်ခြင်း
app.include_router(admin_router)

@app.get("/business/{biz_id}/summary")
def summary(biz_id: str):
    return CRMDashboard.get_business_summary(biz_id)

@app.get("/business/{biz_id}/insight")
def insight(biz_id: str):
    return BusinessAI.generate_business_insight(biz_id)

@app.get("/business/{biz_id}/top-customers")
def top(biz_id: str):
    return CRMDashboard.get_top_customers(biz_id)
