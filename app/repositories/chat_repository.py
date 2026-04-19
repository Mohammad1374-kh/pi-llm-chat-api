from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message


class ChatRepository:

    @staticmethod
    def get_user_conversations(db: Session, user_id: int):
        return (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .all()
        )

    @staticmethod
    def get_messages(db: Session, conversation_id: int):
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )