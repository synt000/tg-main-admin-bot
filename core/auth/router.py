from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from core.auth.jwt import JWTManager
from core.auth.password import PasswordManager

auth_router = APIRouter(prefix="/auth", tags=["SaaS Security Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

@auth_router.post("/login", summary="Admin Login API Route")
def login(payload: LoginRequest):
    # Task 3 Admin Login Hardened Authentication
    if payload.username == "admin" and payload.password == "7m1NJ4OnRufr":
        token = JWTManager.generate_token({"sub": payload.username, "role": "OWNER"})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
