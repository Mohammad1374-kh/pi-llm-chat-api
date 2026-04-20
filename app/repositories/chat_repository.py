from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message


class ChatRepository:

    @staticmethod
    def create_conversation(db, user_id: int, title: str):
        conv = Conversation(
            user_id=user_id,
            title=title
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return conv

    @staticmethod
    def get_conversation(db, conversation_id: int, user_id: int):
        return (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def create_message(db, conversation_id: int, role: str, content: str):
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        db.add(msg)
        db.commit()
        return msg



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