"""
Authentication dependencies for FastAPI
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from loguru import logger
from sqlalchemy.orm import Session

from ...core.dependencies import get_postgres_db
from .service import AuthService
from .models import User, Permission, Role

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db_session: Session = Depends(get_postgres_db)
) -> Optional[User]:
    """Get current authenticated user from JWT token"""
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        auth_service = AuthService(db_session)
        token_data = auth_service.decode_token(token)
        
        if not token_data or not token_data.user_id:
            return None
        
        user = await auth_service.get_user_by_id(token_data.user_id)
        return user
        
    except Exception as e:
        logger.warning(f"Error getting current user: {str(e)}")
        return None


async def require_auth(current_user: Optional[User] = Depends(get_current_user)) -> User:
    """Require authentication"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


def require_permission(permission: Permission):
    """Dependency factory for requiring specific permissions"""
    async def permission_checker(
        current_user: User = Depends(require_auth)
    ) -> User:
        if not current_user.has_permission(permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission.value}",
            )
        return current_user
    
    return permission_checker


def require_role(role: Role):
    """Dependency factory for requiring specific role"""
    async def role_checker(
        current_user: User = Depends(require_auth)
    ) -> User:
        if not current_user.has_role(role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role required: {role.value}",
            )
        return current_user
    
    return role_checker
