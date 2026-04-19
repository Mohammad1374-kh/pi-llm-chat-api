from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    def register(db: Session, email: str, password: str):
        existing = UserRepository.get_by_email(db, email)

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        hashed = hash_password(password)

        UserRepository.create(db, email, hashed)

        return {"message": "User registered successfully"}

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token = create_access_token({"sub": user.email})

        return {
            "access_token": token,
            "token_type": "bearer"
        }