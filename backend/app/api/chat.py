from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ai_service import generate_ai_response
from app.db.session import AsyncSessionLocal

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat(prompt: str):
    response = await generate_ai_response(prompt)
    return {"response": response}
