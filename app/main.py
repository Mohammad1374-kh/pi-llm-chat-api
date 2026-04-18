from fastapi import FastAPI

app = FastAPI(title="Pi LLM Chat API")


@app.get("/health")
def health_check():
    return {"status": "ok"}