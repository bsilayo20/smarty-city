from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import LoginSchema, RegisterSchema
from app.services.auth_service import register_user, login_user
from app.db.session import AsyncSessionLocal

router = APIRouter(prefix="/auth", tags=["Auth"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/register")
async def register(data: RegisterSchema, db: AsyncSession = Depends(get_db)):
    return await register_user(data, db)

@router.post("/login")
async def login(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    return await login_user(data, db)
