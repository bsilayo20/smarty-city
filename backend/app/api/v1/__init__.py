"""
API v1 routes
"""
from fastapi import APIRouter

from . import (
    resources,
    analytics,
    ingestion,
    auth,
    health,
)

api_router = APIRouter()

# Include all route modules
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(resources.router, prefix="/resources", tags=["Resources"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(ingestion.router, prefix="/ingestion", tags=["Data Ingestion"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
