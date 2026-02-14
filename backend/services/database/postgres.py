"""
PostgreSQL with PostGIS database connection and utilities
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from loguru import logger
from config import settings

Base = declarative_base()


class PostgresDB:
    """PostgreSQL database connection manager"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize()
    
    def _initialize(self):
        """Initialize database connection"""
        try:
            connection_string = (
                f"postgresql://{settings.POSTGRES_USER}:"
                f"{settings.POSTGRES_PASSWORD}@"
                f"{settings.POSTGRES_HOST}:"
                f"{settings.POSTGRES_PORT}/"
                f"{settings.POSTGRES_DB}"
            )
            
            self.engine = create_engine(
                connection_string,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20
            )
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info("PostgreSQL connection initialized")
            
        except Exception as e:
            logger.error(f"Error initializing PostgreSQL: {str(e)}")
            raise
    
    @contextmanager
    def get_session(self):
        """Get database session context manager"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    def execute_raw(self, query: str, params: dict = None):
        """Execute raw SQL query"""
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            return result.fetchall()
    
    def check_postgis(self):
        """Check if PostGIS extension is enabled"""
        with self.get_session() as session:
            result = session.execute(
                text("SELECT PostGIS_version();")
            )
            version = result.scalar()
            logger.info(f"PostGIS version: {version}")
            return version


# Global instance
db = PostgresDB()
