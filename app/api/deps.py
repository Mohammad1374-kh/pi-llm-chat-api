from app.core.database import SessionLocal


def get_db():
    # Provide DB session per request
    db = SessionLocal()
    try:
        # injects db into the endpoint
        yield db
    finally:
        db.close()