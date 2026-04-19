from pydantic import BaseModel


class MessageResponse(BaseModel):
    role: str
    content: str


class ConversationResponse(BaseModel):
    conversation_id: int
    title: str
    messages: list[MessageResponse]