"""
Configuration settings for the Smart City FIS backend
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Database Configuration
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "smartcity_db"
    POSTGRES_USER: str = "smartcity_user"
    POSTGRES_PASSWORD: str = "smartcity_pass_2024"
    
    # MongoDB Configuration
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: int = 27017
    MONGODB_USER: str = "smartcity_user"
    MONGODB_PASSWORD: str = "smartcity_pass_2024"
    MONGODB_DB: str = "smartcity_unstructured"
    
    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Ollama/LLM Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    OPENAI_API_KEY: Optional[str] = None
    USE_OPENAI: bool = False
    
    # Security
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AES_KEY: str = "32-byte-key-for-aes-256-encryption!!"
    
    # Application
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Data Ingestion
    INGESTION_SCHEDULE: str = "0 */6 * * *"  # Every 6 hours
    DATA_SOURCE_RETRY_ATTEMPTS: int = 3
    DATA_SOURCE_TIMEOUT: int = 30
    
    # Cleanup
    LOG_RETENTION_DAYS: int = 30
    CLEANUP_SCHEDULE: str = "0 2 * * *"  # Daily at 2 AM
    LOG_DIR: str = "logs"
    
    # Tanzania Open Data Sources
    TANZANIA_OPEN_DATA_BASE_URL: str = "https://www.opendata.go.tz"
    TANZANIA_GOV_API_URL: str = "https://api.tanzania.go.tz"
    NBS_API_URL: str = "https://www.nbs.go.tz/api"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
