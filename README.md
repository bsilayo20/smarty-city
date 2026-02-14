# Smart City FIS - Federated Integrated System

A comprehensive Federated Integrated System (FIS) for Smart City management in Tanzania, featuring microservices architecture, AI-powered analytics, and real-time resource distribution visualization.

## 🏗️ Architecture

- **Backend**: FastAPI (Python) with microservices architecture
- **Frontend**: Next.js 14 with React and TypeScript
- **Databases**: PostgreSQL with PostGIS (spatial data) + MongoDB (unstructured data)
- **Cache**: Redis
- **AI/LLM**: Ollama with Llama 3
- **Maps**: Leaflet/OpenStreetMap

## 📋 Prerequisites

- Docker and Docker Compose
- Git
- (Optional) NVIDIA GPU support for Ollama LLM acceleration

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Create project directory
mkdir smartcity-fis
cd smartcity-fis

# Copy all project files (or clone from repository)
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Important: Change default passwords and secrets!
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 4. Access Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379
- **Ollama**: http://localhost:11434

## 📦 Services

### Core Services

1. **PostgreSQL + PostGIS** (`postgres`)
   - Spatial database for location-based data
   - Port: 5432
   - Database: `smartcity_db`
   - User: `smartcity_user`

2. **MongoDB** (`mongodb`)
   - Document database for unstructured data
   - Port: 27017
   - Database: `smartcity_unstructured`

3. **Redis** (`redis`)
   - Caching and session management
   - Port: 6379

4. **Ollama** (`ollama`)
   - Local LLM for AI analytics
   - Port: 11434
   - Model: Llama 3 (downloads automatically on first use)

### Application Services

5. **API Gateway** (`api_gateway`)
   - Main FastAPI backend
   - Port: 8000
   - Hot-reload enabled in development

6. **Frontend** (`frontend`)
   - Next.js React dashboard
   - Port: 3000
   - Hot-reload enabled in development

### Background Services

7. **Data Ingestion** (`data_ingestion`)
   - Automated data fetching from Tanzanian Open Data portals
   - Runs on schedule (default: every 6 hours)

8. **Cleanup Service** (`cleanup_service`)
   - Automated log shredding and cleanup
   - Runs daily at 2 AM (configurable)

## 🔧 Configuration

### Environment Variables

Edit `.env` file or set environment variables:

```env
# Database passwords (IMPORTANT: Change in production!)
POSTGRES_PASSWORD=your_secure_password
MONGO_PASSWORD=your_secure_password

# Security keys (IMPORTANT: Change in production!)
JWT_SECRET_KEY=your-jwt-secret-key
AES_KEY=32-byte-key-for-aes-256-encryption!!

# Schedules (cron format)
INGESTION_SCHEDULE=0 */6 * * *  # Every 6 hours
CLEANUP_SCHEDULE=0 2 * * *      # Daily at 2 AM

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_MAPBOX_TOKEN=your-mapbox-token  # Optional, for Mapbox tiles
```

### Ollama Setup

On first start, Ollama will pull the Llama 3 model automatically. To use a different model:

```bash
# Access Ollama container
docker exec -it smartcity_ollama bash

# Pull different model (e.g., llama2)
ollama pull llama2

# Update environment variable in docker-compose.yml
OLLAMA_MODEL=llama2
```

### GPU Support (Optional)

To enable GPU acceleration for Ollama:

1. Install NVIDIA Docker runtime
2. Uncomment GPU section in `docker-compose.yml` (ollama service)
3. Restart services

## 📁 Project Structure

```
smartcity-fis/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Backend container
│   ├── services/
│   │   ├── data_ingestion/     # Data ingestion service
│   │   ├── auth/               # Authentication service
│   │   ├── database/           # Database utilities
│   │   └── cleanup/            # Cleanup service
│   └── database/
│       ├── init.sql            # PostgreSQL init script
│       └── mongo-init.js       # MongoDB init script
├── frontend/
│   ├── app/                    # Next.js app directory
│   ├── components/             # React components
│   ├── lib/                    # Utilities
│   ├── package.json            # Node dependencies
│   └── Dockerfile              # Frontend container
├── docker-compose.yml          # Docker services configuration
├── .env.example                # Environment template
└── README.md                   # This file
```

## 🛠️ Development

### Backend Development

```bash
# Enter backend container
docker exec -it smartcity_api_gateway bash

# Install new Python package
pip install package-name
pip freeze > requirements.txt

# Run tests (when implemented)
pytest
```

### Frontend Development

```bash
# Enter frontend container
docker exec -it smartcity_frontend sh

# Install new npm package
npm install package-name

# Build for production
npm run build
```

### Database Access

```bash
# PostgreSQL
docker exec -it smartcity_postgres psql -U smartcity_user -d smartcity_db

# MongoDB
docker exec -it smartcity_mongodb mongosh -u smartcity_user -p smartcity_pass_2024

# Redis
docker exec -it smartcity_redis redis-cli
```

## 📊 Data Sources

The system is configured to fetch data from Tanzanian Open Data portals:

- **National Bureau of Statistics (NBS)**: Population data
- **Tanzania Meteorological Authority (TMA)**: Climate and rainfall
- **Ministry of Health (MoH)**: Disease surveillance
- **Ministry of Water**: Water resources
- **Ministry of Agriculture**: Agricultural statistics
- **Ministry of Education**: School and education data
- **Tanzania Open Data Portal**: General datasets

## 🔐 Security

- JWT authentication with RBAC
- AES-256 encryption for sensitive data
- Environment-based secrets management
- CORS configuration
- SQL injection protection (SQLAlchemy ORM)
- Input validation (Pydantic)

## 📝 API Documentation

Once services are running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Troubleshooting

### Services not starting

```bash
# Check logs
docker-compose logs service_name

# Restart specific service
docker-compose restart service_name

# Rebuild and restart
docker-compose up -d --build service_name
```

### Database connection issues

```bash
# Check database health
docker-compose ps

# Test PostgreSQL connection
docker exec -it smartcity_postgres pg_isready -U smartcity_user

# Check MongoDB connection
docker exec -it smartcity_mongodb mongosh --eval "db.runCommand('ping')"
```

### Port conflicts

If ports are already in use, modify ports in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Change external port
```

### Ollama model download

Ollama models are large. First download may take time:
```bash
docker-compose logs -f ollama
```

## 📈 Monitoring

### Health Checks

All services have health checks. View status:
```bash
docker-compose ps
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api_gateway

# Last 100 lines
docker-compose logs --tail=100 api_gateway
```

## 🚀 Production Deployment

For production:

1. Change all default passwords and secrets
2. Use `.env` file (not `.env.example`)
3. Set `ENVIRONMENT=production`
4. Use production Dockerfiles (multi-stage builds)
5. Configure proper CORS origins
6. Set up SSL/TLS (reverse proxy recommended)
7. Configure backup strategies for databases
8. Set up monitoring and alerting
9. Use secrets management (Docker secrets, Vault, etc.)

## 📄 License

[Add your license here]

## 👥 Contributors

[Add contributors here]

## 📞 Support

[Add support contact information]
