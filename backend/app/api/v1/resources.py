"""
Resources API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

from ...core.dependencies import get_postgres_db
from ...services.auth.dependencies import require_auth, require_permission
from ...services.auth.models import Permission
from ...core.exceptions import NotFoundError
from ...services.resources.service import ResourcesService
from ...services.resources.models import Resource, ResourceType

router = APIRouter()


class ResourceResponse(BaseModel):
    """Resource response model"""
    id: str
    name: str
    type: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: Optional[int] = None
    current_level: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class ResourceCreate(BaseModel):
    """Resource creation model"""
    name: str
    type: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: Optional[int] = None
    current_level: Optional[int] = None
    description: Optional[str] = None


@router.get("", response_model=List[ResourceResponse])
async def list_resources(
    type: Optional[ResourceType] = Query(None, alias="type"),
    location: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    skip: int = Query(0, ge=0),
    db_session = Depends(get_postgres_db)
):
    """List all resources with optional filtering"""
    service = ResourcesService(db_session)
    resources = await service.list_resources(
        resource_type=type,
        location=location,
        limit=limit,
        skip=skip
    )
    return resources


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: str,
    db_session = Depends(get_postgres_db)
):
    """Get a specific resource by ID"""
    service = ResourcesService(db_session)
    resource = await service.get_resource(resource_id)
    
    if not resource:
        raise NotFoundError("Resource", resource_id)
    
    return resource


@router.post("", response_model=ResourceResponse, status_code=201)
async def create_resource(
    resource: ResourceCreate,
    db_session = Depends(get_postgres_db),
    current_user = Depends(require_permission(Permission.RESOURCE_CREATE))
):
    """Create a new resource"""
    service = ResourcesService(db_session)
    created_resource = await service.create_resource(resource.dict())
    return created_resource


@router.get("/nearby", response_model=List[ResourceResponse])
async def get_nearby_resources(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius: float = Query(10, ge=0.1, le=1000, description="Radius in kilometers"),
    resource_type: Optional[ResourceType] = Query(None, alias="type"),
    db_session = Depends(get_postgres_db)
):
    """Get resources near a location"""
    service = ResourcesService(db_session)
    resources = await service.get_nearby_resources(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        resource_type=resource_type
    )
    return resources
