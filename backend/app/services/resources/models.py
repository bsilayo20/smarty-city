"""
Resource models
"""
from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ResourceType(str, Enum):
    """Resource type enum"""
    WATER = "water"
    HEALTH = "health"
    EDUCATION = "education"
    AGRICULTURE = "agriculture"
    INFRASTRUCTURE = "infrastructure"
    TRANSPORT = "transport"
    ENERGY = "energy"


class ResourceStatus(str, Enum):
    """Resource status enum"""
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    UNDER_CONSTRUCTION = "under_construction"
    DECOMMISSIONED = "decommissioned"


class Resource(BaseModel):
    """Resource model"""
    id: Optional[str] = None
    name: str
    type: ResourceType
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: Optional[int] = None
    current_level: Optional[int] = None
    status: ResourceStatus = ResourceStatus.OPERATIONAL
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True
