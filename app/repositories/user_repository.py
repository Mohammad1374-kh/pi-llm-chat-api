from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(
        db: Session,
        email: str,
        hashed_password: str
    ) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password
        )

        db.add(user)
        db.commit()

        # loads generated fields (id, created_at) from DB
        db.refresh(user)

        return user