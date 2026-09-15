import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"[SERVER] Starting Antigravity ATS Resume Scoring Chatbot on http://localhost:{settings.PORT}")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=False)
