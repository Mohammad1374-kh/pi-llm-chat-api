from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_user
from app.services.chat_service import ChatService
from app.schemas.chat_responses import ConversationResponse
from fastapi.responses import StreamingResponse
from app.schemas.chat_requests import ChatRequest
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
from app.core.logger import logger

router = APIRouter(prefix="/chat", tags=["Chat"])



@router.get(
    "/history",
    response_model=list[ConversationResponse],
    summary="Get all user conversations",
    description="Returns all conversations and related messages for the authenticated user."
)
def get_chat_history(
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return ChatService.get_history(db, user)


@router.post(
    "",
    summary="Send message to LLM",
    description="Streams assistant response token-by-token using Server-Sent Events (SSE)."
)
def chat(
        data: ChatRequest,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):

    logger.info(f"[CHAT_REQUEST] user_id={user.id}")
    logger.info(f"[CHAT_REQUEST] conversation_id={data.conversation_id}")
    logger.info(f"[CHAT_REQUEST] message_length={len(data.message)}")


    try:
        stream = ChatService.stream_chat(
        db,
        user,
        data.message,
        data.conversation_id
        )
    except Exception as e:
        logger.error(f"[CHAT_ERROR] user_id={user.id} error={str(e)}")
        raise

    return StreamingResponse(
        stream,
        media_type="text/event-stream"
    )

@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Get single conversation thread",
    description="Returns all messages for one conversation owned by authenticated user."
)
def get_chat_thread(
        conversation_id: int,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    result = ChatService.get_thread(
        db,
        user,
        conversation_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return result