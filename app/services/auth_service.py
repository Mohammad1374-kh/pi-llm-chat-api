from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    def register(db: Session, email: str, password: str):

        logger.info(f"[AUTH] Register attempt: {email}")

        existing = UserRepository.get_by_email(db, email)

        if existing:
            logger.warning(f"[AUTH] Register failed (exists): {email}")
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        hashed = hash_password(password)

        UserRepository.create(db, email, hashed)

        logger.info(f"[AUTH] User created: {email}")

        return {"message": "User registered successfully"}

    @staticmethod
    def login(db: Session, email: str, password: str):
        logger.info(f"[AUTH] Login attempt: {email}")

        user = UserRepository.get_by_email(db, email)

        if not user:
            logger.warning(f"[AUTH] Login failed - user not found: {email}")
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if not verify_password(password, user.hashed_password):
            logger.warning(f"[AUTH] Login failed - invalid password: {email}")
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token = create_access_token({"sub": user.email})

        logger.info(f"[AUTH] Login success: {email}")

        return {
            "access_token": token,
            "token_type": "bearer"
        }