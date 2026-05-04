from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger import logger
from app.core.timing import StreamingTimer
from app.llm.factory import LLMFactory
from app.repositories.chat_repository import ChatRepository


class ChatService:

    @staticmethod
    def _serialize_messages(messages):
        # Convert ORM Message objects into API-friendly dictionaries
        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]

    @staticmethod
    def get_thread(db: Session, user, conversation_id: int):
        # Fetch a specific conversation (using its id) with its related messages, ensuring it belongs to the user
        result = ChatRepository.get_conversation_with_messages(
            db,
            conversation_id,
            user.id
        )

        if not result:
            # Conversation not found or does not belong to user
            return None

        conversation, messages = result

        return {
            "conversation_id": conversation.id,
            "title": conversation.title,
            "messages": ChatService._serialize_messages(messages)
        }

    @staticmethod
    def get_history(db: Session, user):
        # Retrieve all conversations for user with their messages
        # Note: currently performs N+1 queries (one per conversation)
        conversations = ChatRepository.get_user_conversations(db, user.id)

        return [
            {
                "conversation_id": conv.id,
                "title": conv.title,
                "messages": ChatService._serialize_messages(
                    ChatRepository.get_messages(db, conv.id)
                )
            }
            for conv in conversations
        ]

    @staticmethod
    def stream_chat(db: Session, user, message: str, conversation_id=None):
        # Handle streaming chat interaction with LLM and persist messages

        logger.info(f"[CHAT] Request received user_id={user.id}")

        timer = StreamingTimer()
        timer.start()

        conversation = None

        # Load existing conversation if provided
        if conversation_id:
            conversation = ChatRepository.get_conversation(
                db,
                conversation_id,
                user.id
            )

        # Create new conversation if not found (or not provided)
        if not conversation:
            conversation = ChatRepository.create_conversation(
                db,
                user.id,
                message[:50]
            )

        # Persist user message before sending to LLM
        ChatRepository.create_message(
            db,
            conversation.id,
            "user",
            message
        )

        provider = LLMFactory.create(settings.LLM_PROVIDER)

        logger.info(f"[LLM] Streaming started provider={settings.LLM_PROVIDER}")

        def event_stream():
            # Generator that streams tokens to client (SSE)
            # while accumulating full response for persistence

            full_response = ""

            for token in provider.stream(message):
                timer.on_token(token)
                full_response += token
                # Stream token immediately to client (low latency)
                yield f"data: {token}\n\n"

            # Persist full assistant response after streaming completes
            ChatRepository.create_message(
                db,
                conversation.id,
                "assistant",
                full_response
            )

            # Stop timer and log latency metrics (TTFT, TTLT, ...)
            timer.stop()

            logger.info(
                f"[CHAT] Completed conversation_id={conversation.id}"
            )

            logger.info({
                "ttft_ms": timer.ttft_ms,
                "ttlt_ms": timer.ttlt_ms,
                "chars_per_sec": timer.chars_per_sec,
                "chars": len(full_response),
            })

        return event_stream()