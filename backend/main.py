from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="KnowledgeBase AI API")

@app.get("/")
def read_root():
    return{"status": "ok", "message": "KnowledgeBase AI backend is running!"}