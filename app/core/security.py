from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.logger import logger
from app.models.user import User


ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

security = HTTPBearer()


def decode_access_token(token: str):
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        logger.warning("[SECURITY] Invalid JWT token")
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise HTTPException(401, "Invalid token")

    email = payload.get("sub")

    if not email:
        raise HTTPException(401, "Invalid token payload")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        logger.warning(f"[SECURITY] User not found: {email}")
        raise HTTPException(401, "User not found")

    logger.info(f"[SECURITY] Authenticated: {email}")

    return user


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=12)

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )