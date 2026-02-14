"""
Data Fetcher - Handles fetching data from various Tanzanian Open Data sources
"""
import httpx
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .sources import DataSource, TanzanianDataSources
from ..database.postgres import PostgresDB
from ..database.mongodb import MongoDB
from config import settings


class DataFetcher:
    """
    Fetches data from Tanzanian Open Data portals
    """
    
    def __init__(self):
        self.postgres_db = PostgresDB()
        self.mongodb = MongoDB()
        self.client = httpx.AsyncClient(
            timeout=settings.DATA_SOURCE_TIMEOUT,
            follow_redirects=True
        )
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException))
    )
    async def fetch_from_api(
        self, 
        source: DataSource, 
        params: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch data from an API endpoint
        
        Args:
            source: DataSource configuration
            params: Optional query parameters
            
        Returns:
            JSON response data or None
        """
        try:
            headers = {}
            if source.auth_required and source.auth_token:
                headers["Authorization"] = f"Bearer {source.auth_token}"
            
            logger.info(f"Fetching data from {source.name} - {source.api_endpoint}")
            
            response = await self.client.get(
                source.api_endpoint,
                headers=headers,
                params=params or {}
            )
            response.raise_for_status()
            
            if source.format == "json":
                data = response.json()
            elif source.format == "xml":
                # For XML, return raw text for later parsing
                data = {"raw_xml": response.text}
            else:
                data = {"raw_data": response.text}
            
            logger.success(f"Successfully fetched data from {source.name}")
            return data
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching from {source.name}: {e.response.status_code}")
            return None
        except httpx.TimeoutException:
            logger.error(f"Timeout fetching from {source.name}")
            raise
        except Exception as e:
            logger.error(f"Error fetching from {source.name}: {str(e)}")
            return None
    
    async def fetch_from_url(self, url: str, format: str = "json") -> Optional[Any]:
        """
        Fetch data from a direct URL (for CSV, JSON files)
        
        Args:
            url: URL to fetch from
            format: Expected format (json, csv, xml)
            
        Returns:
            Parsed data or None
        """
        try:
            logger.info(f"Fetching data from URL: {url}")
            response = await self.client.get(url)
            response.raise_for_status()
            
            if format == "json":
                return response.json()
            elif format == "csv":
                return {"raw_csv": response.text}
            else:
                return {"raw_data": response.text}
                
        except Exception as e:
            logger.error(f"Error fetching from URL {url}: {str(e)}")
            return None
    
    async def save_to_postgres(
        self,
        source: DataSource,
        data: Dict[str, Any],
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Save structured data to PostgreSQL with PostGIS
        
        Args:
            source: DataSource configuration
            data: Data to save
            metadata: Additional metadata
            
        Returns:
            Success status
        """
        try:
            # Extract spatial data if present
            ingestion_record = {
                "source_id": source.name.lower().replace(" ", "_"),
                "source_type": source.source_type.value,
                "ingested_at": datetime.utcnow(),
                "data": data,
                "metadata": metadata or {}
            }
            
            # Store in MongoDB for unstructured data
            await self.mongodb.insert_document(
                collection="data_ingestion_logs",
                document=ingestion_record
            )
            
            # For structured spatial data, store in PostGIS
            if "location" in data or "coordinates" in data:
                await self._save_spatial_data(source, data)
            
            logger.success(f"Saved data from {source.name} to database")
            return True
            
        except Exception as e:
            logger.error(f"Error saving data to PostgreSQL: {str(e)}")
            return False
    
    async def _save_spatial_data(self, source: DataSource, data: Dict[str, Any]):
        """Save spatial/geographic data to PostGIS"""
        # Implementation for PostGIS spatial data storage
        # This will be handled by the spatial service
        pass
    
    async def fetch_and_save(
        self,
        source_id: str,
        params: Optional[Dict] = None
    ) -> bool:
        """
        Fetch data from a source and save it
        
        Args:
            source_id: ID of the data source
            params: Optional query parameters
            
        Returns:
            Success status
        """
        source = TanzanianDataSources.get_source(source_id)
        if not source:
            logger.error(f"Source {source_id} not found")
            return False
        
        data = await self.fetch_from_api(source, params)
        if not data:
            return False
        
        metadata = {
            "fetched_at": datetime.utcnow().isoformat(),
            "source_url": source.url,
            "source_type": source.source_type.value
        }
        
        return await self.save_to_postgres(source, data, metadata)
    
    async def fetch_all_sources(self) -> Dict[str, bool]:
        """
        Fetch data from all configured sources
        
        Returns:
            Dictionary mapping source IDs to success status
        """
        results = {}
        sources = TanzanianDataSources.get_all_sources()
        
        logger.info(f"Starting batch fetch for {len(sources)} sources")
        
        # Fetch all sources concurrently
        tasks = []
        source_ids = []
        
        for source_id, source in TanzanianDataSources.SOURCES.items():
            tasks.append(self.fetch_and_save(source_id))
            source_ids.append(source_id)
        
        results_list = await asyncio.gather(*tasks, return_exceptions=True)
        
        for source_id, result in zip(source_ids, results_list):
            if isinstance(result, Exception):
                logger.error(f"Exception fetching {source_id}: {str(result)}")
                results[source_id] = False
            else:
                results[source_id] = result
        
        successful = sum(1 for v in results.values() if v)
        logger.info(f"Batch fetch completed: {successful}/{len(sources)} successful")
        
        return results
