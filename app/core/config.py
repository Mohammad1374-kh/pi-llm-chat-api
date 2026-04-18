import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Pi LLM Chat API"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    GROQ_MODEL = os.getenv("GROQ_MODEL")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

settings = Settings()