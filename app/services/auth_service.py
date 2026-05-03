from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def register(db: Session, email: str, password: str):
        logger.info(f"[AUTH] Register attempt: {email}")

        # Prevent duplicate accounts using same email
        if UserRepository.get_by_email(db, email):
            logger.warning(f"[AUTH] Register failed - email exists: {email}")
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        # Hash password before storing for security (never store plain text passwords)
        hashed_password = hash_password(password)

        UserRepository.create(db, email, hashed_password)

        logger.info(f"[AUTH] User registered: {email}")

        return {"message": "User registered successfully"}

    @staticmethod
    def login(db: Session, email: str, password: str):
        logger.info(f"[AUTH] Login attempt: {email}")

        user = UserRepository.get_by_email(db, email)

        # Validate user existence and verify password hash
        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"[AUTH] Login failed: {email}")
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        # Create JWT access token with user identity (email stored in 'sub' claim)
        token = create_access_token({"sub": user.email})

        logger.info(f"[AUTH] Login success: {email}")

        return {
            "access_token": token,
            "token_type": "bearer"
        }