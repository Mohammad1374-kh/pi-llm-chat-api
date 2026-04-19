from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine
from app.models import user, conversation, message

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)


@app.get("/health")
def health_check():
    return {"status": "ok"}