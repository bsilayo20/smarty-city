"""
Data Ingestion API endpoints
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from ...services.auth.dependencies import require_auth, require_permission
from ...services.auth.models import Permission
from ...services.data_ingestion.fetcher import DataFetcher
from ...services.data_ingestion.sources import TanzanianDataSources
from ...services.data_ingestion.router import (
    IngestionRequest,
    IngestionResponse,
    SourceListResponse,
)

router = APIRouter()


@router.get("/sources", response_model=SourceListResponse)
async def list_sources(
    current_user = Depends(require_permission(Permission.DATA_INGESTION_VIEW))
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


@router.post("/fetch", response_model=IngestionResponse)
async def trigger_ingestion(
    request: IngestionRequest,
    background_tasks: BackgroundTasks,
    current_user = Depends(require_permission(Permission.DATA_INGESTION_TRIGGER))
):
    """Trigger data ingestion"""
    fetcher = DataFetcher()
    
    try:
        if request.source_id:
            success = await fetcher.fetch_and_save(request.source_id, request.params)
            return IngestionResponse(
                success=success,
                message=f"Ingestion {'successful' if success else 'failed'}",
                source_id=request.source_id
            )
        elif request.source_type:
            # Fetch all sources of a type
            from ...services.data_ingestion.sources import DataSourceType
            source_type = DataSourceType(request.source_type)
            sources = TanzanianDataSources.get_sources_by_type(source_type)
            
            background_tasks.add_task(
                fetcher.fetch_all_sources
            )
            return IngestionResponse(
                success=True,
                message=f"Started ingestion for {len(sources)} sources"
            )
        else:
            background_tasks.add_task(fetcher.fetch_all_sources)
            return IngestionResponse(
                success=True,
                message="Data ingestion started in background"
            )
    finally:
        await fetcher.close()


@router.get("/status")
async def get_ingestion_status(
    current_user = Depends(require_auth)
) -> Dict[str, Any]:
    """Get ingestion status"""
    # TODO: Fetch from database
    return {
        "status": "active",
        "last_ingestion": None,
        "sources_count": len(TanzanianDataSources.SOURCES)
    }
