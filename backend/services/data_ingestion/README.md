# Data Ingestion Service

This service handles automated fetching and ingestion of data from Tanzanian Open Data portals.

## Features

- **Multi-source data fetching**: Supports multiple Tanzanian government data sources
- **Automated scheduling**: Configurable cron-based scheduling for regular data updates
- **Error handling**: Robust retry mechanisms and error logging
- **Storage**: Stores structured data in PostgreSQL (PostGIS) and unstructured data in MongoDB
- **API endpoints**: RESTful API for manual ingestion triggers and status monitoring

## Data Sources

The service is configured to fetch from:

1. **National Bureau of Statistics (NBS)**: Population census data
2. **Tanzania Meteorological Authority (TMA)**: Climate and rainfall data
3. **Ministry of Health (MoH)**: Disease surveillance data
4. **Ministry of Water**: Water resources and infrastructure
5. **Ministry of Agriculture**: Crop production and agricultural statistics
6. **Ministry of Education**: School locations and enrollment data
7. **Tanzania Open Data Portal**: General open datasets

## Usage

### Manual Ingestion

```bash
# Fetch all sources
curl -X POST http://localhost:8000/api/v1/ingestion/fetch \
  -H "Authorization: Bearer YOUR_TOKEN"

# Fetch specific source
curl -X POST http://localhost:8000/api/v1/ingestion/fetch \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"source_id": "nbs_population"}'

# Fetch by type
curl -X POST http://localhost:8000/api/v1/ingestion/fetch \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"source_type": "climate"}'
```

### List Sources

```bash
curl http://localhost:8000/api/v1/ingestion/sources \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Scheduled Ingestion

The scheduler automatically runs:
- **Full ingestion**: Every 6 hours (configurable)
- **Climate data**: Daily at midnight
- **Rainfall data**: Daily at 00:30
- **Disease data**: Weekly on Sunday at 2 AM

## Configuration

Edit `config.py` or set environment variables to configure:
- Data source URLs and endpoints
- Ingestion schedules
- Retry attempts and timeouts
- Database connections

## Adding New Data Sources

To add a new data source, edit `sources.py`:

```python
"new_source": DataSource(
    name="New Data Source Name",
    source_type=DataSourceType.RESOURCES,
    url="https://example.com",
    api_endpoint="https://example.com/api/v1/data",
    auth_required=False,
    update_frequency="daily",
    format="json",
    description="Description of the data source"
)
```

## Error Handling

The service includes:
- Automatic retry with exponential backoff
- Error logging to MongoDB
- Status tracking for each ingestion attempt
- Graceful handling of unavailable sources

## Monitoring

Check ingestion status:
```bash
curl http://localhost:8000/api/v1/ingestion/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Logs are stored in:
- PostgreSQL: `data_ingestion_logs` table
- MongoDB: `data_ingestion_logs` collection
- Application logs: Configured via loguru
