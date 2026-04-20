from app.repositories.chat_repository import ChatRepository
from app.llm.factory import LLMFactory
from app.core.config import settings
from app.core.logger import logger
from app.core.timing import StreamingTimer


class ChatService:

    @staticmethod
    def get_thread(db, user, conversation_id: int):
        result = ChatRepository.get_conversation_with_messages(
            db,
            conversation_id,
            user.id
        )

        if not result:
            return None

        conversation, messages = result

        return {
            "conversation_id": conversation.id,
            "title": conversation.title,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content
                }
                for msg in messages
            ]
        }

    @staticmethod
    def get_history(db, user):
        conversations = ChatRepository.get_user_conversations(
            db,
            user.id
        )

        result = []

        for conv in conversations:
            messages = ChatRepository.get_messages(db, conv.id)

            result.append({
                "conversation_id": conv.id,
                "title": conv.title,
                "messages": [
                    {
                        "role": msg.role,
                        "content": msg.content
                    }
                    for msg in messages
                ]
            })

        return result

    @staticmethod
    def stream_chat(db, user, message: str, conversation_id=None):

        logger.info("[LLM_STREAM] token streaming started")
        timer = StreamingTimer()
        timer.start()

        # create or load conversation
        if conversation_id:
            conversation = ChatRepository.get_conversation(
                db,
                conversation_id,
                user.id
            )
        else:
            conversation = None

        if not conversation:
            title = message[:50]
            conversation = ChatRepository.create_conversation(
                db,
                user.id,
                title
            )

        # save user message
        ChatRepository.create_message(
            db,
            conversation.id,
            "user",
            message
        )

        logger.info(f"[LLM_START] provider={settings.LLM_PROVIDER}")
        logger.info("[LLM_START] streaming initiated")
        provider = LLMFactory.create(settings.LLM_PROVIDER)

        def event_stream():
            full_response = ""

            for token in provider.stream(message):
                timer.on_token(token)
                full_response += token
                #sends the token first to api layer then saves in db
                yield f"data: {token}\n\n"


            ChatRepository.create_message(
                db,
                conversation.id,
                "assistant",
                full_response
            )

            logger.info(f"[CHAT_DONE] conversation_id={conversation.id}")
            logger.info("[CHAT_DONE] message persisted successfully")

            timer.stop()

            result = {
                "ttft_ms": timer.ttft_ms,
                "ttlt_ms": timer.ttlt_ms,
                "chars_per_sec": timer.chars_per_sec,
                "chars": len(full_response),
            }

            logger.info(result)

        return event_stream()