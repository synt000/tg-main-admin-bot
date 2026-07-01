class RBAC:
    ROLES = ["OWNER", "ADMIN", "STAFF", "VIEWER"]
    PERMISSIONS = {
        "OWNER": ["*"],
        "ADMIN": ["read", "write", "finance", "crm"],
        "STAFF": ["read", "write"],
        "VIEWER": ["read"]
    }

    @staticmethod
    def check_permission(role, action):
        allowed = RBAC.PERMISSIONS.get(role, [])
        if "*" in allowed: return True
        return action in allowed

def require_permission(role, action):
    if not RBAC.check_permission(role, action):
        raise Exception(f"Access denied: {role} cannot execute {action}")
    return True
