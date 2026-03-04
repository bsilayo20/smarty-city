from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, chat
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/health")
def health():
    return {"status": "ok"}
