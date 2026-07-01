from fastapi import FastAPI
from modules.crm.dashboard import CRMDashboard
from modules.ai.assistant import BusinessAI

app = FastAPI(title="BusinessOS Enterprise SaaS Dashboard API", version="1.0")

@app.get("/business/{biz_id}/summary")
def summary(biz_id: str):
    return CRMDashboard.get_business_summary(biz_id)

@app.get("/business/{biz_id}/insight")
def insight(biz_id: str):
    return BusinessAI.generate_business_insight(biz_id)

@app.get("/business/{biz_id}/top-customers")
def top(biz_id: str):
    return CRMDashboard.get_top_customers(biz_id)
