from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from modules.crm.dashboard import CRMDashboard

admin_router = APIRouter(prefix="/admin", tags=["Web Admin Panel"])
templates = Jinja2Templates(directory="web_admin/templates")

@admin_router.get("/dashboard/{biz_id}", response_class=HTMLResponse, summary="Render Executive Dashboard View")
async def render_enterprise_dashboard(request: Request, biz_id: str):
    """
    SaaS Executive Web Portal Dashboard Engine
    """
    summary = CRMDashboard.get_business_summary(biz_id)
    top_vips = CRMDashboard.get_top_customers(biz_id, limit=5)
    
    # Secure Unpacking Logic safely
    try:
        t_cust = summary[0] if summary else 0
        t_rev = summary[1] if summary else 0
        t_pts = summary[2] if summary else 0
    except Exception:
        t_cust, t_rev, t_pts = 0, 0, 0
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "biz_id": biz_id,
        "total_customers": t_cust,
        "revenue": float(t_rev),
        "total_points": int(t_pts),
        "top_vips": top_vips
    })
