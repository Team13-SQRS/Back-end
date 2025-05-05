from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.crud import (
    create_user,
    authenticate_user,
    get_user_by_username,
)
from app.database.database import get_db
from app.security.tokens import create_access_token
from pydantic import BaseModel
from app.auth.dependencies import get_current_user

router = APIRouter()


class SignupRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, request.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = create_user(db, request.username, request.password)
    return {
        "message": "User created successfully",
        "username": new_user.username,
    }


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_current_user_info(current_user=Depends(get_current_user)):
    return {"username": current_user.username, "id": current_user.id}
