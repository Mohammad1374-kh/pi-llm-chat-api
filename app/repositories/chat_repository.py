from pyexpat.errors import messages

from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message


class ChatRepository:

    @staticmethod
    def get_conversation_with_messages(
        db: Session,
        conversation_id: int,
        user_id: int
    ):
        # Fetch conversation and its messages, ensuring it belongs to the user

        conversation = ChatRepository.get_conversation(
                db,
                conversation_id,
                user_id
            )

        # Conversation not found or does not belong to user
        if not conversation:
            return None

        messages = ChatRepository.get_messages(db, conversation_id)

        return conversation, messages



    @staticmethod
    def create_conversation(
        db: Session,
        user_id: int,
        title: str
    ) -> Conversation:
        conv = Conversation(
            user_id=user_id,
            title=title
        )

        # Create and persist a new conversation
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return conv

    @staticmethod
    def get_conversation(
        db: Session,
        conversation_id: int,
        user_id: int
    ):
        return (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def create_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str
    ) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        # Persist a single chat message (user or assistant)
        db.add(msg)
        db.commit()
        return msg

    @staticmethod
    def get_user_conversations(
        db: Session,
        user_id: int
    ):
        # Retrieve all conversations for a user (most recent first)
        return (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .all()
        )

    @staticmethod
    def get_messages(
        db: Session,
        conversation_id: int
    ):
        # Retrieve messages for a conversation in chronological order
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )