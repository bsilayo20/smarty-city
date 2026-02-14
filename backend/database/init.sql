-- Initialize PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Create schema for spatial data
CREATE SCHEMA IF NOT EXISTS spatial;

-- Create tables for data ingestion tracking
CREATE TABLE IF NOT EXISTS data_ingestion_logs (
    id SERIAL PRIMARY KEY,
    source_id VARCHAR(255) NOT NULL,
    source_type VARCHAR(100) NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'success',
    record_count INTEGER DEFAULT 0,
    error_message TEXT,
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_ingestion_source ON data_ingestion_logs(source_id);
CREATE INDEX IF NOT EXISTS idx_ingestion_type ON data_ingestion_logs(source_type);
CREATE INDEX IF NOT EXISTS idx_ingestion_date ON data_ingestion_logs(ingested_at);

-- Create table for spatial locations (regions, districts)
CREATE TABLE IF NOT EXISTS spatial.locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location_type VARCHAR(50) NOT NULL, -- region, district, ward
    parent_id INTEGER REFERENCES spatial.locations(id),
    geometry GEOMETRY(GEOMETRY, 4326),
    properties JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_locations_type ON spatial.locations(location_type);
CREATE INDEX IF NOT EXISTS idx_locations_geometry ON spatial.locations USING GIST(geometry);

-- Create table for population data
CREATE TABLE IF NOT EXISTS spatial.population (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES spatial.locations(id),
    year INTEGER NOT NULL,
    total_population INTEGER,
    male_population INTEGER,
    female_population INTEGER,
    age_groups JSONB,
    data_source VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_population_location ON spatial.population(location_id);
CREATE INDEX IF NOT EXISTS idx_population_year ON spatial.population(year);

-- Create table for climate data
CREATE TABLE IF NOT EXISTS spatial.climate (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES spatial.locations(id),
    station_name VARCHAR(255),
    date DATE NOT NULL,
    temperature_avg DECIMAL(5,2),
    temperature_min DECIMAL(5,2),
    temperature_max DECIMAL(5,2),
    humidity DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    data_source VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_climate_location ON spatial.climate(location_id);
CREATE INDEX IF NOT EXISTS idx_climate_date ON spatial.climate(date);

-- Create table for rainfall data
CREATE TABLE IF NOT EXISTS spatial.rainfall (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES spatial.locations(id),
    station_name VARCHAR(255),
    date DATE NOT NULL,
    rainfall_mm DECIMAL(8,2),
    station_geometry GEOMETRY(POINT, 4326),
    data_source VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_rainfall_location ON spatial.rainfall(location_id);
CREATE INDEX IF NOT EXISTS idx_rainfall_date ON spatial.rainfall(date);
CREATE INDEX IF NOT EXISTS idx_rainfall_geometry ON spatial.rainfall USING GIST(station_geometry);

-- Create table for disease data
CREATE TABLE IF NOT EXISTS spatial.diseases (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES spatial.locations(id),
    disease_name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    cases INTEGER DEFAULT 0,
    deaths INTEGER DEFAULT 0,
    recovered INTEGER DEFAULT 0,
    age_groups JSONB,
    data_source VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_diseases_location ON spatial.diseases(location_id);
CREATE INDEX IF NOT EXISTS idx_diseases_name ON spatial.diseases(disease_name);
CREATE INDEX IF NOT EXISTS idx_diseases_date ON spatial.diseases(date);

-- Create table for water resources
CREATE TABLE IF NOT EXISTS spatial.water_resources (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES spatial.locations(id),
    resource_type VARCHAR(100), -- well, river, lake, reservoir
    name VARCHAR(255),
    capacity DECIMAL(12,2),
    current_level DECIMAL(12,2),
    geometry GEOMETRY(GEOMETRY, 4326),
    properties JSONB,
    data_source VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_water_location ON spatial.water_resources(location_id);
CREATE INDEX IF NOT EXISTS idx_water_geometry ON spatial.water_resources USING GIST(geometry);

-- Create table for agriculture data
CREATE TABLE IF NOT EXISTS spatial.agriculture (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES spatial.locations(id),
    crop_type VARCHAR(100),
    season VARCHAR(50),
    year INTEGER,
    area_hectares DECIMAL(10,2),
    production_tons DECIMAL(10,2),
    yield_per_hectare DECIMAL(8,2),
    data_source VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_agriculture_location ON spatial.agriculture(location_id);
CREATE INDEX IF NOT EXISTS idx_agriculture_year ON spatial.agriculture(year);

-- Create table for infrastructure predictions (AI generated)
CREATE TABLE IF NOT EXISTS spatial.infrastructure_predictions (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES spatial.locations(id),
    infrastructure_type VARCHAR(100), -- hospital, school, water_source
    priority_score DECIMAL(5,2),
    predicted_capacity INTEGER,
    reasoning TEXT,
    confidence_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_version VARCHAR(50)
);

CREATE INDEX IF NOT EXISTS idx_predictions_location ON spatial.infrastructure_predictions(location_id);
CREATE INDEX IF NOT EXISTS idx_predictions_type ON spatial.infrastructure_predictions(infrastructure_type);
CREATE INDEX IF NOT EXISTS idx_predictions_priority ON spatial.infrastructure_predictions(priority_score DESC);
