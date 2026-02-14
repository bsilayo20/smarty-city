"""
Shared dependencies for API routes
"""
from fastapi import Depends, HTTPException, status
from typing import Optional
from loguru import logger

from ...services.database.postgres import db as postgres_db
from ...services.database.mongodb import mongo_db

# Import auth dependencies (they handle the actual auth logic)
from ..services.auth.dependencies import (
    get_current_user,
    require_auth,
    require_permission,
    require_role
)


async def get_postgres_db():
    """Dependency to get PostgreSQL database session"""
    try:
        with postgres_db.get_session() as session:
            yield session
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )


async def get_mongodb():
    """Dependency to get MongoDB instance"""
    try:
        yield mongo_db
    except Exception as e:
        logger.error(f"MongoDB connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MongoDB connection failed"
        )
