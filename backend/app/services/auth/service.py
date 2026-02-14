"""
Authentication service with JWT and RBAC
"""
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from loguru import logger
from sqlalchemy.orm import Session
import secrets

from ...core.config import settings
from .models import User, UserCreate, UserUpdate, Token, TokenData, Role
from ...core.exceptions import AuthenticationError, NotFoundError, DatabaseError

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication and authorization service"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode_token(self, token: str) -> Optional[TokenData]:
        """Decode and verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            roles: list = payload.get("roles", [])
            
            if user_id is None:
                return None
            
            return TokenData(user_id=user_id, email=email, roles=roles)
        except JWTError as e:
            logger.warning(f"JWT decode error: {str(e)}")
            return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Token]:
        """Authenticate user and return access token"""
        try:
            # TODO: Query user from database
            # For now, use mock user data
            user = await self.get_user_by_email(email)
            
            if not user:
                logger.warning(f"Authentication failed: User not found - {email}")
                return None
            
            # Verify password
            # TODO: Get hashed password from database
            # For now, accept any password (mock)
            # if not self.verify_password(password, user.hashed_password):
            #     logger.warning(f"Authentication failed: Invalid password - {email}")
            #     return None
            
            if not user.is_active:
                logger.warning(f"Authentication failed: User inactive - {email}")
                return None
            
            # Create token
            token_data = {
                "sub": user.id,
                "email": user.email,
                "roles": [role.value for role in user.roles],
            }
            
            access_token = self.create_access_token(data=token_data)
            
            return Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=self.access_token_expire_minutes * 60,
                user=user
            )
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise AuthenticationError(f"Authentication failed: {str(e)}")
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            # TODO: Query from database
            # Mock implementation for now
            if email == "admin@example.com":
                return User(
                    id="1",
                    email=email,
                    full_name="Admin User",
                    roles=[Role.ADMIN],
                    is_active=True,
                    created_at=datetime.utcnow()
                )
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            raise DatabaseError(f"Failed to get user: {str(e)}")
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            # TODO: Query from database
            # Mock implementation
            if user_id == "1":
                return User(
                    id=user_id,
                    email="admin@example.com",
                    full_name="Admin User",
                    roles=[Role.ADMIN],
                    is_active=True
                )
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            raise DatabaseError(f"Failed to get user: {str(e)}")
    
    async def create_user(self, email: str, password: str, full_name: Optional[str] = None, roles: Optional[list] = None) -> User:
        """Create a new user"""
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(email)
            if existing_user:
                raise ValueError(f"User with email {email} already exists")
            
            # Hash password
            hashed_password = self.get_password_hash(password)
            
            # Create user
            user_id = secrets.token_urlsafe(16)
            user_roles = [Role(r) for r in roles] if roles else [Role.VIEWER]
            
            # TODO: Save to database
            user = User(
                id=user_id,
                email=email,
                full_name=full_name,
                roles=user_roles,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            logger.info(f"Created new user: {email}")
            return user
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise DatabaseError(f"Failed to create user: {str(e)}")
    
    async def update_user(self, user_id: str, user_update: UserUpdate) -> User:
        """Update user information"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise NotFoundError("User", user_id)
            
            # Update fields
            if user_update.full_name is not None:
                user.full_name = user_update.full_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            if user_update.is_active is not None:
                user.is_active = user_update.is_active
            
            user.updated_at = datetime.utcnow()
            
            # TODO: Save to database
            
            return user
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise DatabaseError(f"Failed to update user: {str(e)}")
