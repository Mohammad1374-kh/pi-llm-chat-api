from app.repositories.chat_repository import ChatRepository


class ChatService:

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