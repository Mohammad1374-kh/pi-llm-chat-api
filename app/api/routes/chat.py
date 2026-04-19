from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_user
from app.services.chat_service import ChatService
from app.schemas.chat_responses import ConversationResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/history", response_model=list[ConversationResponse])
def get_chat_history(
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return ChatService.get_history(db, user)