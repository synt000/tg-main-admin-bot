from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from core.database import get_db_connection, release_db_connection
from core.auth.jwt import JWTManager
from core.auth.password import PasswordManager

auth_router = APIRouter(prefix="/auth", tags=["SaaS Security Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

@auth_router.post("/login", summary="Dynamic Enterprise Database Login API Route")
def login(payload: LoginRequest):
    # 🎯 Requirement: Input Boundary Check - Handle Empty Payload Constraints Safely
    if not payload.username or not payload.password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username and password fields cannot be empty"
        )

    # 🎯 Requirement: Core Database Pool Connection Execution Gate
    try:
        conn = get_db_connection()
        cur = conn.cursor()
    except Exception as db_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connectivity failed: {str(db_err)}"
        )
    
    try:
        # 🎯 Requirement: Query users table securely matching username and check records context
        cur.execute(
            "SELECT telegram_id, role, username, status, password_hash FROM users WHERE username = %s;", 
            (payload.username,)
        )
        user_record = cur.fetchone()
        
        # 🎯 Requirement: Unknown Username Handler - Return 401 Unauthorized Accurately
        if not user_record:
            cur.close()
            release_db_connection(conn)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid username or password"
            )
            
        # Safely extract dictionary mappings context supporting all cursor factory layouts
        if hasattr(user_record, "get"):
            t_id = user_record.get("telegram_id")
            role = user_record.get("role")
            user_status = user_record.get("status", "active")
            stored_hash = user_record.get("password_hash")
        else:
            # Sequence tuple index unpacking logic fallback matrix
            t_id, role, _, user_status, stored_hash = user_record

        # 🎯 Requirement: Wrong Password Handler - Return 401 Unauthorized Accurately
        is_valid_password = PasswordManager.verify_password(payload.password, stored_hash)
        if not is_valid_password:
            cur.close()
            release_db_connection(conn)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid username or password"
            )

        # 🎯 Requirement: Inactive User Enforcement Gate - Return 403 Forbidden Accurately
        if user_status == "inactive":
            cur.close()
            release_db_connection(conn)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive. Access denied."
            )
            
        # 🎯 Requirement: Tenant Isolation Check & Cryptographic JWT Token Generation Context
        token = JWTManager.generate_token({
            "sub": payload.username, 
            "tenant_id": t_id, 
            "role": role
        })
        
        cur.close()
        release_db_connection(conn)
        return {"access_token": token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): release_db_connection(conn)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database transaction failure: {str(e)}"
        )
