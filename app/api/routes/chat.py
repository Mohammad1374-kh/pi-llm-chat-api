from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_user
from app.services.chat_service import ChatService
from app.schemas.chat_responses import ConversationResponse
from fastapi.responses import StreamingResponse
from app.schemas.chat_requests import ChatRequest
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/chat", tags=["chat"])



@router.get("/history", response_model=list[ConversationResponse])
def get_chat_history(
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return ChatService.get_history(db, user)


@router.post("")
def chat(
        data: ChatRequest,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    stream = ChatService.stream_chat(
        db,
        user,
        data.message,
        data.conversation_id
    )

    return StreamingResponse(
        stream,
        media_type="text/event-stream"
    )