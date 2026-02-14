"""
Authentication and authorization models
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    """User roles"""
    ADMIN = "admin"
    MANAGER = "manager"
    ANALYST = "analyst"
    VIEWER = "viewer"
    DATA_INGESTION = "data_ingestion"


class Permission(str, Enum):
    """Permissions"""
    # Resource permissions
    RESOURCE_VIEW = "resource:view"
    RESOURCE_CREATE = "resource:create"
    RESOURCE_UPDATE = "resource:update"
    RESOURCE_DELETE = "resource:delete"
    
    # Analytics permissions
    ANALYTICS_VIEW = "analytics:view"
    ANALYTICS_PREDICT = "analytics:predict"
    
    # Data ingestion permissions
    DATA_INGESTION_VIEW = "data_ingestion:view"
    DATA_INGESTION_TRIGGER = "data_ingestion:trigger"
    
    # User management permissions
    USER_VIEW = "user:view"
    USER_CREATE = "user:create"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    
    # Admin permissions
    ADMIN_ALL = "admin:all"


# Role to permissions mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: [
        Permission.RESOURCE_VIEW,
        Permission.RESOURCE_CREATE,
        Permission.RESOURCE_UPDATE,
        Permission.RESOURCE_DELETE,
        Permission.ANALYTICS_VIEW,
        Permission.ANALYTICS_PREDICT,
        Permission.DATA_INGESTION_VIEW,
        Permission.DATA_INGESTION_TRIGGER,
        Permission.USER_VIEW,
        Permission.USER_CREATE,
        Permission.USER_UPDATE,
        Permission.USER_DELETE,
        Permission.ADMIN_ALL,
    ],
    Role.MANAGER: [
        Permission.RESOURCE_VIEW,
        Permission.RESOURCE_CREATE,
        Permission.RESOURCE_UPDATE,
        Permission.ANALYTICS_VIEW,
        Permission.ANALYTICS_PREDICT,
        Permission.DATA_INGESTION_VIEW,
        Permission.DATA_INGESTION_TRIGGER,
        Permission.USER_VIEW,
    ],
    Role.ANALYST: [
        Permission.RESOURCE_VIEW,
        Permission.ANALYTICS_VIEW,
        Permission.ANALYTICS_PREDICT,
        Permission.DATA_INGESTION_VIEW,
    ],
    Role.DATA_INGESTION: [
        Permission.RESOURCE_VIEW,
        Permission.DATA_INGESTION_VIEW,
        Permission.DATA_INGESTION_TRIGGER,
    ],
    Role.VIEWER: [
        Permission.RESOURCE_VIEW,
        Permission.ANALYTICS_VIEW,
    ],
}


class User(BaseModel):
    """User model"""
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    roles: List[Role] = [Role.VIEWER]
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def has_role(self, role: Role) -> bool:
        """Check if user has a specific role"""
        return role in self.roles
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has a specific permission"""
        # Admin has all permissions
        if Permission.ADMIN_ALL in self.get_permissions():
            return True
        
        return permission in self.get_permissions()
    
    def get_permissions(self) -> List[Permission]:
        """Get all permissions for user based on roles"""
        permissions = set()
        for role in self.roles:
            if role in ROLE_PERMISSIONS:
                permissions.update(ROLE_PERMISSIONS[role])
        return list(permissions)


class UserCreate(BaseModel):
    """User creation model"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    roles: List[Role] = [Role.VIEWER]


class UserUpdate(BaseModel):
    """User update model"""
    full_name: Optional[str] = None
    roles: Optional[List[Role]] = None
    is_active: Optional[bool] = None


class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Optional[User] = None


class TokenData(BaseModel):
    """Token payload data"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    roles: List[str] = []
