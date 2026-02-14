"""
Health check endpoints
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from loguru import logger

from ...core.dependencies import get_postgres_db, get_mongodb
from ...services.database.postgres import db as postgres_db
from ...services.database.mongodb import mongo_db

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "Smart City FIS API",
        "version": "1.0.0"
    }


@router.get("/health/detailed")
async def detailed_health_check(
    db_session = Depends(get_postgres_db)
) -> Dict[str, Any]:
    """Detailed health check with database connections"""
    health_status = {
        "status": "healthy",
        "service": "Smart City FIS API",
        "version": "1.0.0",
        "components": {}
    }
    
    try:
        # Check PostgreSQL
        with postgres_db.get_session() as session:
            session.execute("SELECT 1")
        health_status["components"]["postgresql"] = "healthy"
    except Exception as e:
        logger.error(f"PostgreSQL health check failed: {str(e)}")
        health_status["components"]["postgresql"] = "unhealthy"
        health_status["status"] = "degraded"
    
    try:
        # Check MongoDB
        mongo_db.client.admin.command('ping')
        health_status["components"]["mongodb"] = "healthy"
    except Exception as e:
        logger.error(f"MongoDB health check failed: {str(e)}")
        health_status["components"]["mongodb"] = "unhealthy"
        health_status["status"] = "degraded"
    
    return health_status
