# Quick Start Guide - Smart City FIS

Get up and running in 5 minutes!

## Prerequisites

- Docker Desktop (or Docker + Docker Compose)
- Git
- At least 8GB RAM (16GB recommended for Ollama)

## Step 1: Clone and Setup

```bash
# Navigate to project directory
cd smartcity-fis

# Copy environment template
cp .env.example .env

# (Optional) Edit .env with custom passwords/secrets
# For quick start, defaults will work but CHANGE THEM for production!
```

## Step 2: Start All Services

```bash
# Start all services in detached mode
docker-compose up -d

# This will:
# - Pull required Docker images
# - Build backend and frontend containers
# - Start all 8 services
# - Set up databases with initial schema
```

## Step 3: Wait for Services to Start

```bash
# Watch logs to see startup progress
docker-compose logs -f

# Or check status
docker-compose ps
```

Expected startup time:
- PostgreSQL, MongoDB, Redis: ~30 seconds
- Backend API: ~1 minute (installing dependencies)
- Frontend: ~2 minutes (installing dependencies)
- Ollama: ~2-3 minutes (downloads model on first run)

## Step 4: Access the Application

Once services are healthy:

1. **Frontend Dashboard**: http://localhost:3000
2. **Backend API**: http://localhost:8000
3. **API Documentation**: http://localhost:8000/docs
4. **Health Check**: http://localhost:8000/health

## Step 5: Verify Services

```bash
# Check all services are running
docker-compose ps

# Test API health
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000
```

## Common Commands

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Restart a specific service
docker-compose restart api_gateway

# View logs for a service
docker-compose logs -f api_gateway

# Rebuild and restart
docker-compose up -d --build

# Execute command in container
docker-compose exec api_gateway bash
```

## First-Time Ollama Setup

On first run, Ollama will download Llama 3 model (~5GB). Monitor progress:

```bash
docker-compose logs -f ollama
```

This may take 10-20 minutes depending on internet speed.

## Troubleshooting

### Ports already in use

If ports 3000, 8000, 5432, etc. are in use:

```bash
# Find what's using the port (Linux/Mac)
lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

### Services not starting

```bash
# Check logs
docker-compose logs service_name

# Restart service
docker-compose restart service_name

# Rebuild service
docker-compose up -d --build service_name
```

### Database connection errors

```bash
# Check database health
docker-compose exec postgres pg_isready -U smartcity_user
docker-compose exec mongodb mongosh --eval "db.runCommand('ping')"

# Restart databases
docker-compose restart postgres mongodb
```

### Out of memory

Ollama requires significant memory. If issues:

1. Close other applications
2. Allocate more RAM to Docker Desktop
3. Or disable Ollama service temporarily:
   ```bash
   docker-compose stop ollama
   ```

## Next Steps

1. Explore the API: http://localhost:8000/docs
2. View the dashboard: http://localhost:3000
3. Configure data sources in `backend/services/data_ingestion/sources.py`
4. Set up authentication (see main README)
5. Customize frontend components

## Stopping Services

```bash
# Stop all services (keeps data)
docker-compose stop

# Stop and remove containers (keeps volumes/data)
docker-compose down

# Stop and remove everything including data (WARNING!)
docker-compose down -v
```

## Getting Help

- Check logs: `docker-compose logs -f`
- Review README.md for detailed documentation
- Check service health: `docker-compose ps`
- View API docs: http://localhost:8000/docs

Happy building! 🚀
