from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth_requests import (
    RegisterRequest,
    LoginRequest
)
from app.api.deps import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    return AuthService.register(
        db,
        str(data.email),
        data.password
    )


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    return AuthService.login(
        db,
        str(data.email),
        data.password
    )