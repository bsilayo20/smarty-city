"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from ...services.auth.service import AuthService
from ...core.dependencies import get_postgres_db
from ...services.auth.dependencies import get_current_user, require_auth
from ...services.auth.models import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User response model"""
    id: str
    email: str
    roles: List[str]
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """User creation model"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserCreate,
    db_session = Depends(get_postgres_db)
):
    """Register a new user"""
    service = AuthService(db_session)
    try:
        user = await service.create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session = Depends(get_postgres_db)
):
    """Login and get access token"""
    service = AuthService(db_session)
    token = await service.authenticate_user(
        email=form_data.username,  # OAuth2 uses username for email
        password=form_data.password
    )
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user information"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return current_user


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """Logout current user"""
    # TODO: Invalidate token in Redis/blacklist
    return {"message": "Successfully logged out"}
