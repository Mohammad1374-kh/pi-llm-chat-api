from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine
from app.models import user, conversation, message
from app.api.routes.auth import router as auth_router
from app.api.routes.chat import router as chat_router



Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth_router)

app.include_router(chat_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}