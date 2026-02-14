"""
Analytics API endpoints
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from ...core.dependencies import get_postgres_db
from ...services.auth.dependencies import require_auth, require_permission
from ...services.auth.models import Permission
from ...services.analytics.service import AnalyticsService
from ...services.resources.models import ResourceType

router = APIRouter()


class StatsResponse(BaseModel):
    """Statistics response model"""
    total_resources: int
    by_type: Dict[str, int]
    by_location: Dict[str, int]


class DistributionResponse(BaseModel):
    """Distribution response model"""
    type: str
    count: int
    percentage: float


@router.get("/stats")
async def get_statistics(
    db_session = Depends(get_postgres_db)
) -> StatsResponse:
    """Get overall statistics"""
    service = AnalyticsService(db_session)
    stats = await service.get_statistics()
    return stats


@router.get("/distribution")
async def get_distribution(
    resource_type: Optional[ResourceType] = Query(None, alias="type"),
    db_session = Depends(get_postgres_db)
) -> List[DistributionResponse]:
    """Get resource distribution by type or location"""
    service = AnalyticsService(db_session)
    distribution = await service.get_distribution(resource_type)
    return distribution


@router.post("/predict")
async def predict_infrastructure_needs(
    location: str,
    resource_type: ResourceType,
    db_session = Depends(get_postgres_db),
    current_user = Depends(require_permission(Permission.ANALYTICS_PREDICT))
) -> Dict[str, Any]:
    """Predict infrastructure needs using AI"""
    service = AnalyticsService(db_session)
    prediction = await service.predict_infrastructure_needs(
        location=location,
        resource_type=resource_type
    )
    return prediction


@router.get("/trends")
async def get_trends(
    resource_type: Optional[ResourceType] = Query(None, alias="type"),
    days: int = Query(30, ge=1, le=365),
    db_session = Depends(get_postgres_db)
) -> Dict[str, Any]:
    """Get resource trends over time"""
    service = AnalyticsService(db_session)
    trends = await service.get_trends(resource_type, days)
    return trends
