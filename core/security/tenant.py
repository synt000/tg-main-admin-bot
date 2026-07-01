class TenantGuard:
    @staticmethod
    def validate(biz_id):
        # 🏢 All queries must follow: WHERE business_id = %s
        if not biz_id:
            raise Exception("CRITICAL ACCESS VIOLATION: Invalid business access registry layer key.")
        return True

class AccessControl:
    @staticmethod
    def can_manage_finance(role):
        # 👥 Roles: OWNER, ADMIN, STAFF, VIEWER
        return role in ["OWNER", "ADMIN"]

def require_role(user_role, allowed_roles):
    if user_role not in allowed_roles:
        raise Exception("SECURITY ERROR: Access denied. Role privileges insufficient.")
    return True
