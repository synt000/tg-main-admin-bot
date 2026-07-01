from modules.crm.service import CRMService

class CRMEvents:
    @staticmethod
    def record_purchase(biz_id, customer_id, module, amount):
        # 1. Add activity log to central crm ledger
        CRMService.add_activity(
            biz_id,
            customer_id,
            module,
            "purchase",
            amount
        )

        # 2. Update central crm customer statistics
        CRMService.update_customer_stats(biz_id, customer_id, amount)

        # 3. Process central loyalty and tier recalculation
        CRMService.update_loyalty(biz_id, customer_id, amount)
        return True
