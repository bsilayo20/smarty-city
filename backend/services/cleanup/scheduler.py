"""
Cleanup Scheduler - Automated log shredding and data cleanup
"""
import asyncio
import os
import glob
from datetime import datetime, timedelta
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from config import settings


class CleanupScheduler:
    """
    Schedules and manages automated cleanup tasks
    """
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.log_dir = Path(getattr(settings, 'LOG_DIR', 'logs'))
        self.log_dir.mkdir(exist_ok=True, parents=True)
        
    async def cleanup_logs(self):
        """Clean up old log files"""
        try:
            retention_days = settings.LOG_RETENTION_DAYS
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            logger.info(f"Starting log cleanup. Retention: {retention_days} days")
            
            # Find all log files
            log_files = glob.glob(str(self.log_dir / "*.log"))
            deleted_count = 0
            
            for log_file in log_files:
                try:
                    file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
                    if file_time < cutoff_date:
                        os.remove(log_file)
                        deleted_count += 1
                        logger.info(f"Deleted old log file: {log_file}")
                except Exception as e:
                    logger.error(f"Error deleting log file {log_file}: {str(e)}")
            
            logger.info(f"Log cleanup completed. Deleted {deleted_count} files")
            
        except Exception as e:
            logger.error(f"Error in log cleanup: {str(e)}")
    
    def setup_schedules(self):
        """Configure scheduled cleanup tasks"""
        # Log cleanup schedule
        self.scheduler.add_job(
            self.cleanup_logs,
            CronTrigger.from_crontab(settings.CLEANUP_SCHEDULE),
            id="log_cleanup",
            name="Log Cleanup",
            replace_existing=True
        )
        
        logger.info("Cleanup schedules configured")
    
    async def start(self):
        """Start the scheduler"""
        self.setup_schedules()
        self.scheduler.start()
        logger.info("Cleanup Scheduler started")
        
        # Run initial cleanup
        await self.cleanup_logs()
        
        try:
            # Keep running
            while True:
                await asyncio.sleep(3600)  # Sleep for 1 hour
        except KeyboardInterrupt:
            logger.info("Stopping cleanup scheduler...")
            self.scheduler.shutdown()


async def main():
    """Main entry point for the cleanup service"""
    scheduler = CleanupScheduler()
    await scheduler.start()


if __name__ == "__main__":
    asyncio.run(main())
