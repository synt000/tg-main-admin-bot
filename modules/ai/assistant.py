from modules.crm.dashboard import CRMDashboard

class BusinessAI:
    @staticmethod
    def generate_business_insight(biz_id):
        summary = CRMDashboard.get_business_summary(biz_id)
        top_customers = CRMDashboard.get_top_customers(biz_id)

        # Tuple Safe Index Unpacking (Dict သို့မဟုတ် Tuple ၂ မျိုးစလုံး Safe ဖြစ်စေရန်)
        try:
            revenue = summary['revenue'] if summary else 0
            total_customers = summary['total_customers'] if summary else 0
        except:
            try:
                revenue = summary[1] if summary else 0
                total_customers = summary[0] if summary else 0
            except:
                revenue = 0
                total_customers = 0

        insight = []

        if revenue > 50000:
            insight.append("🔥 High revenue business detected")
        else:
            insight.append("📈 Revenue growth opportunity exists")

        if total_customers < 10:
            insight.append("⚠️ Low customer base")

        if top_customers:
            try:
                t_spent = top_customers[0]['total_spent']
            except:
                try: t_spent = top_customers[0][2]
                except: t_spent = 0
            insight.append(f"👑 Top customer spent: {t_spent}")

        return {
            "revenue": revenue,
            "customers": total_customers,
            "insights": insight
        }

    @staticmethod
    def recommend_actions(biz_id):
        data = BusinessAI.generate_business_insight(biz_id)
        actions = []

        if data["revenue"] < 50000:
            actions.append("Boost marketing campaign")

        if data["customers"] < 20:
            actions.append("Run customer acquisition promo")

        if len(data["insights"]) > 0:
            actions.append("Review top-performing products")

        return actions

    # 🚨 3. Auto Alert System Engine
    @staticmethod
    def generate_alerts(biz_id):
        alerts = []
        summary = CRMDashboard.get_business_summary(biz_id)

        try: revenue = summary['revenue'] if summary else 0
        except:
            try: revenue = summary[1] if summary else 0
            except: revenue = 0

        if revenue < 10000:
            alerts.append("🚨 Low revenue alert")

        if revenue > 100000:
            alerts.append("💰 High performance detected")

        return alerts
