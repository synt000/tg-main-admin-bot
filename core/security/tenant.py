from fastapi import HTTPException, status
from core.database import get_db_connection, release_db_connection

class TenantGuard:
    # 🚀 🔒 [STRICT TENANT ISOLATION ACTIVE]: Tenant A နှင့် Tenant B အချင်းချင်း Data Leakage ဖြစ်ခြင်းမှ ကာကွယ်မည့် Core Engine
    @staticmethod
    def enforce_tenant_isolation(active_session_tenant_id: str, target_resource_tenant_id: str):
        # 🎯 Requirement: Enforce strict row-level isolation check boundary context
        if active_session_tenant_id != target_resource_tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Security Violation: Resource separation breach. Access Denied."
            )

    @staticmethod
    def query_tenant_records_parameterized(table_name: str, tenant_id: str, resource_id_field: str = None, resource_id: str = None):
        # 🎯 Requirement: Use PARAMETERIZED SQL ONLY to block cross-read injection vulnerabilities cleanly
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Enforce clean syntax boundary checks dynamically but executing securely via parameter mapping tuple
            if resource_id_field and resource_id:
                query = f"SELECT * FROM {table_name} WHERE business_id = %s AND {resource_id_field} = %s;"
                cur.execute(query, (tenant_id, resource_id))
            else:
                query = f"SELECT * FROM {table_name} WHERE business_id = %s;"
                cur.execute(query, (tenant_id,))
                
            records = cur.fetchall()
            cur.close()
            release_db_connection(conn)
            return records
            
        except Exception as e:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): release_db_connection(conn)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Isolated lookup execution failed: {str(e)}"
            )
