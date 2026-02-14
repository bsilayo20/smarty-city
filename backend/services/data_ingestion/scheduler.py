"""
Scheduler for automated data ingestion from Tanzanian Open Data portals
"""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger
from datetime import datetime

from config import settings
from .fetcher import DataFetcher
from .sources import DataSourceType, TanzanianDataSources


class DataIngestionScheduler:
    """
    Schedules and manages automated data ingestion tasks
    """
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.fetcher = DataFetcher()
        
    async def ingest_all_data(self):
        """Run full data ingestion from all sources"""
        logger.info("Starting scheduled data ingestion")
        try:
            results = await self.fetcher.fetch_all_sources()
            logger.info(f"Data ingestion completed: {results}")
        except Exception as e:
            logger.error(f"Error in scheduled data ingestion: {str(e)}")
    
    async def ingest_by_type(self, source_type: DataSourceType):
        """Ingest data from sources of a specific type"""
        logger.info(f"Starting ingestion for type: {source_type.value}")
        sources = TanzanianDataSources.get_sources_by_type(source_type)
        
        for source in sources:
            source_id = None
            for sid, src in TanzanianDataSources.SOURCES.items():
                if src == source:
                    source_id = sid
                    break
            
            if source_id:
                await self.fetcher.fetch_and_save(source_id)
    
    def setup_schedules(self):
        """Configure scheduled tasks"""
        # Main ingestion schedule (every 6 hours)
        self.scheduler.add_job(
            self.ingest_all_data,
            CronTrigger.from_crontab(settings.INGESTION_SCHEDULE),
            id="full_ingestion",
            name="Full Data Ingestion",
            replace_existing=True
        )
        
        # Daily climate and rainfall data (most frequent updates)
        self.scheduler.add_job(
            lambda: self.ingest_by_type(DataSourceType.CLIMATE),
            CronTrigger(hour=0, minute=0),  # Daily at midnight
            id="climate_ingestion",
            name="Climate Data Ingestion",
            replace_existing=True
        )
        
        self.scheduler.add_job(
            lambda: self.ingest_by_type(DataSourceType.RAINFALL),
            CronTrigger(hour=0, minute=30),  # Daily at 00:30
            id="rainfall_ingestion",
            name="Rainfall Data Ingestion",
            replace_existing=True
        )
        
        # Weekly disease data
        self.scheduler.add_job(
            lambda: self.ingest_by_type(DataSourceType.DISEASES),
            CronTrigger(day_of_week=0, hour=2),  # Weekly on Sunday at 2 AM
            id="disease_ingestion",
            name="Disease Data Ingestion",
            replace_existing=True
        )
        
        logger.info("Data ingestion schedules configured")
    
    async def start(self):
        """Start the scheduler"""
        self.setup_schedules()
        self.scheduler.start()
        logger.info("Data Ingestion Scheduler started")
        
        # Run initial ingestion
        await self.ingest_all_data()
        
        try:
            # Keep running
            while True:
                await asyncio.sleep(3600)  # Sleep for 1 hour
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            self.scheduler.shutdown()
            await self.fetcher.close()


async def main():
    """Main entry point for the scheduler service"""
    scheduler = DataIngestionScheduler()
    await scheduler.start()


if __name__ == "__main__":
    asyncio.run(main())
