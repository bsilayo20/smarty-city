"""
API Router for Data Ingestion Service
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from .fetcher import DataFetcher
from .sources import TanzanianDataSources, DataSourceType
from ..auth.dependencies import get_current_user, require_permission
from ..auth.models import User, Permission

router = APIRouter(prefix="/api/v1/ingestion", tags=["Data Ingestion"])


class IngestionRequest(BaseModel):
    source_id: Optional[str] = None
    source_type: Optional[str] = None
    params: Optional[Dict[str, Any]] = None


class IngestionResponse(BaseModel):
    success: bool
    message: str
    source_id: Optional[str] = None
    ingested_at: Optional[datetime] = None


class SourceListResponse(BaseModel):
    sources: List[Dict[str, Any]]


@router.get("/sources", response_model=SourceListResponse)
async def list_sources(
    current_user: User = Depends(get_current_user)
):
    """List all available data sources"""
    sources = TanzanianDataSources.get_all_sources()
    
    source_list = []
    for source_id, source in TanzanianDataSources.SOURCES.items():
        source_list.append({
            "id": source_id,
            "name": source.name,
            "type": source.source_type.value,
            "url": source.url,
            "update_frequency": source.update_frequency,
            "description": source.description
        })
    
    return SourceListResponse(sources=source_list)


@router.get("/sources/{source_id}")
async def get_source_details(
    source_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get details about a specific data source"""
    source = TanzanianDataSources.get_source(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    return {
        "id": source_id,
        "name": source.name,
        "type": source.source_type.value,
        "url": source.url,
        "api_endpoint": source.api_endpoint,
        "update_frequency": source.update_frequency,
        "format": source.format,
        "description": source.description
    }


@router.post("/fetch", response_model=IngestionResponse)
async def trigger_ingestion(
    request: IngestionRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_permission(Permission.DATA_INGESTION))
):
    """
    Manually trigger data ingestion
    
    Can fetch from a specific source or all sources of a type
    """
    fetcher = DataFetcher()
    
    try:
        if request.source_id:
            # Fetch specific source
            success = await fetcher.fetch_and_save(request.source_id, request.params)
            return IngestionResponse(
                success=success,
                message=f"Ingestion {'successful' if success else 'failed'}",
                source_id=request.source_id,
                ingested_at=datetime.utcnow()
            )
        
        elif request.source_type:
            # Fetch all sources of a type
            source_type = DataSourceType(request.source_type)
            sources = TanzanianDataSources.get_sources_by_type(source_type)
            
            success_count = 0
            for source in sources:
                source_id = None
                for sid, src in TanzanianDataSources.SOURCES.items():
                    if src == source:
                        source_id = sid
                        break
                
                if source_id:
                    if await fetcher.fetch_and_save(source_id, request.params):
                        success_count += 1
            
            return IngestionResponse(
                success=success_count > 0,
                message=f"Ingested {success_count}/{len(sources)} sources",
                ingested_at=datetime.utcnow()
            )
        
        else:
            # Fetch all sources (run in background for large operations)
            background_tasks.add_task(fetcher.fetch_all_sources)
            return IngestionResponse(
                success=True,
                message="Data ingestion started in background",
                ingested_at=datetime.utcnow()
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        await fetcher.close()


@router.get("/status")
async def get_ingestion_status(
    current_user: User = Depends(get_current_user)
):
    """Get status of recent data ingestion"""
    # This would query the database for recent ingestion logs
    # Implementation depends on your logging setup
    return {
        "status": "active",
        "last_ingestion": datetime.utcnow().isoformat(),
        "sources_count": len(TanzanianDataSources.SOURCES)
    }
