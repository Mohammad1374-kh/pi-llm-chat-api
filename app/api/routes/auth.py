from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth_requests import (
    RegisterRequest,
    LoginRequest
)
from app.api.deps import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    summary="Register a new user",
    description="Create a new account using email and password."
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    return AuthService.register(
        db,
        str(data.email),
        data.password
    )


@router.post(
    "/login",
    summary="Login user",
    description="Authenticate user credentials and return JWT token."
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    return AuthService.login(
        db,
        str(data.email),
        data.password
    )