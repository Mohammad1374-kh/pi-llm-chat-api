from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.models import user, conversation, message
from app.api.routes.auth import router as auth_router
from app.api.routes.chat import router as chat_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pi LLM Chat API",
    description="""
Minimal LLM-powered chat backend built with FastAPI.

Features:
- JWT authentication
- Streaming chat responses (SSE)
- Conversation history persistence
- Dockerized deployment
- Pluggable LLM providers (Groq / OpenRouter)
""",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/health", summary="Health check")
def health_check():
    return {"status": "ok"}