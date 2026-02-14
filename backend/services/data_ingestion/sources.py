"""
Tanzanian Open Data Sources Configuration
"""
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass


class DataSourceType(str, Enum):
    POPULATION = "population"
    CLIMATE = "climate"
    RAINFALL = "rainfall"
    DISEASES = "diseases"
    RESOURCES = "resources"
    HEALTH = "health"
    EDUCATION = "education"
    WATER = "water"
    AGRICULTURE = "agriculture"


@dataclass
class DataSource:
    name: str
    source_type: DataSourceType
    url: str
    api_endpoint: Optional[str] = None
    auth_required: bool = False
    auth_token: Optional[str] = None
    update_frequency: str = "daily"
    format: str = "json"  # json, csv, xml
    description: str = ""


class TanzanianDataSources:
    """
    Configuration for Tanzanian Open Data Portal sources
    """
    
    SOURCES: Dict[str, DataSource] = {
        # Population Data
        "nbs_population": DataSource(
            name="National Bureau of Statistics - Population Census",
            source_type=DataSourceType.POPULATION,
            url="https://www.nbs.go.tz",
            api_endpoint="https://www.nbs.go.tz/api/v1/population",
            auth_required=False,
            update_frequency="yearly",
            format="json",
            description="Population census data by region and district"
        ),
        
        # Climate Data
        "tma_climate": DataSource(
            name="Tanzania Meteorological Authority - Climate Data",
            source_type=DataSourceType.CLIMATE,
            url="https://www.meteo.go.tz",
            api_endpoint="https://www.meteo.go.tz/api/v1/climate",
            auth_required=False,
            update_frequency="daily",
            format="json",
            description="Temperature, humidity, and climate data by region"
        ),
        
        # Rainfall Data
        "tma_rainfall": DataSource(
            name="TMA - Rainfall Data",
            source_type=DataSourceType.RAINFALL,
            url="https://www.meteo.go.tz",
            api_endpoint="https://www.meteo.go.tz/api/v1/rainfall",
            auth_required=False,
            update_frequency="daily",
            format="json",
            description="Rainfall measurements by station and region"
        ),
        
        # Health/Diseases Data
        "moh_diseases": DataSource(
            name="Ministry of Health - Disease Surveillance",
            source_type=DataSourceType.DISEASES,
            url="https://www.moh.go.tz",
            api_endpoint="https://www.moh.go.tz/api/v1/diseases",
            auth_required=False,
            update_frequency="weekly",
            format="json",
            description="Disease incidence and prevalence by region"
        ),
        
        # Water Resources
        "maji_resources": DataSource(
            name="Ministry of Water - Water Resources",
            source_type=DataSourceType.WATER,
            url="https://www.maji.go.tz",
            api_endpoint="https://www.maji.go.tz/api/v1/resources",
            auth_required=False,
            update_frequency="monthly",
            format="json",
            description="Water availability and infrastructure by region"
        ),
        
        # Agriculture Data
        "kilimo_agriculture": DataSource(
            name="Ministry of Agriculture - Crop Data",
            source_type=DataSourceType.AGRICULTURE,
            url="https://www.kilimo.go.tz",
            api_endpoint="https://www.kilimo.go.tz/api/v1/crops",
            auth_required=False,
            update_frequency="seasonal",
            format="json",
            description="Crop production and agricultural statistics"
        ),
        
        # Open Data Portal
        "opendata_portal": DataSource(
            name="Tanzania Open Data Portal",
            source_type=DataSourceType.RESOURCES,
            url="https://www.opendata.go.tz",
            api_endpoint="https://www.opendata.go.tz/api/v1/datasets",
            auth_required=False,
            update_frequency="monthly",
            format="json",
            description="General open datasets from Tanzania Open Data Portal"
        ),
        
        # Education Data
        "elimu_education": DataSource(
            name="Ministry of Education - School Data",
            source_type=DataSourceType.EDUCATION,
            url="https://www.moe.go.tz",
            api_endpoint="https://www.moe.go.tz/api/v1/schools",
            auth_required=False,
            update_frequency="yearly",
            format="json",
            description="School locations, enrollment, and infrastructure"
        ),
    }
    
    @classmethod
    def get_source(cls, source_id: str) -> Optional[DataSource]:
        """Get a specific data source by ID"""
        return cls.SOURCES.get(source_id)
    
    @classmethod
    def get_sources_by_type(cls, source_type: DataSourceType) -> List[DataSource]:
        """Get all sources of a specific type"""
        return [src for src in cls.SOURCES.values() if src.source_type == source_type]
    
    @classmethod
    def get_all_sources(cls) -> List[DataSource]:
        """Get all configured sources"""
        return list(cls.SOURCES.values())
