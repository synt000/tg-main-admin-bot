from modules.ai.assistant import BusinessAI
from modules.crm.dashboard import CRMDashboard

class TelegramAI:
    @staticmethod
    def handle_report(biz_id):
        summary = CRMDashboard.get_business_summary(biz_id)
        try:
            t_cust = summary[0] if summary else 0
            t_rev = summary[1] if summary else 0
        except:
            t_cust, t_rev = 0, 0
        return {"message": f"📊 Revenue: {t_rev}\n👥 Customers: {t_cust}"}

    @staticmethod
    def handle_insight(biz_id):
        ai = BusinessAI.generate_business_insight(biz_id)
        return {"message": "\n".join(ai["insights"])}

    @staticmethod
    def handle_recommend(biz_id):
        actions = BusinessAI.recommend_actions(biz_id)
        return {"message": "\n".join(actions)}
