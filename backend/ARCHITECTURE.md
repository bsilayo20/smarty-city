# FastAPI Backend Architecture

## Microservices Structure

The backend is organized as a modular microservices architecture with the following structure:

```
backend/
├── app/
│   ├── core/              # Core infrastructure
│   │   ├── config.py      # Configuration
│   │   ├── dependencies.py # Shared dependencies
│   │   ├── exceptions.py  # Custom exceptions & handlers
│   │   └── middleware.py  # Custom middleware
│   ├── api/
│   │   └── v1/           # API v1 routes
│   │       ├── auth.py    # Authentication endpoints
│   │       ├── resources.py # Resource endpoints
│   │       ├── analytics.py # Analytics endpoints
│   │       ├── ingestion.py # Data ingestion endpoints
│   │       └── health.py  # Health check endpoints
│   └── services/          # Business logic services
│       ├── auth/          # Authentication service
│       │   ├── models.py  # User, Role, Permission models
│       │   ├── service.py # Auth business logic
│       │   ├── dependencies.py # Auth dependencies
│       │   └── utils.py   # Encryption utilities
│       ├── resources/     # Resources service
│       │   ├── models.py  # Resource models
│       │   └── service.py # Resource business logic
│       ├── analytics/     # Analytics service
│       │   └── service.py # Analytics business logic
│       ├── data_ingestion/ # Data ingestion service
│       │   ├── sources.py # Data source configurations
│       │   ├── fetcher.py # Data fetching logic
│       │   └── scheduler.py # Scheduled ingestion
│       └── database/      # Database utilities
│           ├── postgres.py # PostgreSQL connection
│           └── mongodb.py  # MongoDB connection
├── main.py               # Application entry point
└── config.py            # Global configuration
```

## Architecture Principles

### 1. Separation of Concerns
- **API Layer**: Handles HTTP requests/responses, validation
- **Service Layer**: Contains business logic
- **Data Layer**: Database access and models

### 2. Dependency Injection
- FastAPI's dependency injection system used throughout
- Services injected into routes via dependencies
- Database sessions managed via context managers

### 3. Error Handling
- Custom exception classes for different error types
- Centralized exception handlers
- Consistent error response format

### 4. Security
- JWT-based authentication
- Role-Based Access Control (RBAC)
- Permission-based authorization
- AES-256 encryption for sensitive data

## Services

### Authentication Service (`app/services/auth/`)

**Responsibilities:**
- User authentication (login/logout)
- JWT token generation and validation
- User management (CRUD)
- Role and permission management
- Password hashing

**Models:**
- `User`: User model with roles and permissions
- `Role`: Enum of available roles (ADMIN, MANAGER, ANALYST, VIEWER, DATA_INGESTION)
- `Permission`: Enum of available permissions
- `Token`: JWT token response

**Endpoints:**
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout

### Resources Service (`app/services/resources/`)

**Responsibilities:**
- Resource management (CRUD)
- Spatial queries using PostGIS
- Resource filtering and search
- Nearby resources queries

**Models:**
- `Resource`: Resource model with location data
- `ResourceType`: Enum of resource types
- `ResourceStatus`: Enum of resource statuses

**Endpoints:**
- `GET /api/v1/resources` - List resources
- `GET /api/v1/resources/{id}` - Get resource
- `POST /api/v1/resources` - Create resource
- `GET /api/v1/resources/nearby` - Get nearby resources

### Analytics Service (`app/services/analytics/`)

**Responsibilities:**
- Statistical analysis
- Resource distribution analysis
- Trend analysis
- AI-powered predictions

**Endpoints:**
- `GET /api/v1/analytics/stats` - Get statistics
- `GET /api/v1/analytics/distribution` - Get distribution
- `POST /api/v1/analytics/predict` - Predict infrastructure needs
- `GET /api/v1/analytics/trends` - Get trends

### Data Ingestion Service (`app/services/data_ingestion/`)

**Responsibilities:**
- Fetching data from Tanzanian Open Data portals
- Scheduled data ingestion
- Data transformation and storage
- Error handling and retries

**Endpoints:**
- `GET /api/v1/ingestion/sources` - List data sources
- `POST /api/v1/ingestion/fetch` - Trigger ingestion
- `GET /api/v1/ingestion/status` - Get ingestion status

## Authentication & Authorization

### JWT Authentication

Tokens are generated with:
- `sub`: User ID
- `email`: User email
- `roles`: List of user roles
- `exp`: Expiration time
- `iat`: Issued at time

### Role-Based Access Control (RBAC)

**Roles:**
- **ADMIN**: Full access to all resources
- **MANAGER**: Manage resources, view analytics, trigger ingestion
- **ANALYST**: View resources, analytics, and make predictions
- **DATA_INGESTION**: View resources and trigger data ingestion
- **VIEWER**: Read-only access to resources and analytics

**Permissions:**
- Resource permissions: `resource:view`, `resource:create`, `resource:update`, `resource:delete`
- Analytics permissions: `analytics:view`, `analytics:predict`
- Data ingestion permissions: `data_ingestion:view`, `data_ingestion:trigger`
- User management permissions: `user:view`, `user:create`, `user:update`, `user:delete`
- Admin permissions: `admin:all`

### Usage

```python
# Require authentication
from app.services.auth.dependencies import require_auth

@router.get("/protected")
async def protected_route(current_user: User = Depends(require_auth)):
    return {"user": current_user.email}

# Require specific permission
from app.services.auth.dependencies import require_permission
from app.services.auth.models import Permission

@router.post("/resources")
async def create_resource(
    resource: ResourceCreate,
    current_user: User = Depends(require_permission(Permission.RESOURCE_CREATE))
):
    # Create resource
    pass

# Require specific role
from app.services.auth.dependencies import require_role
from app.services.auth.models import Role

@router.delete("/users/{id}")
async def delete_user(
    id: str,
    current_user: User = Depends(require_role(Role.ADMIN))
):
    # Delete user
    pass
```

## Database Models

### PostgreSQL (PostGIS)
- Structured data
- Spatial data (locations, geometries)
- Resources with geographic coordinates
- Relationships and constraints

### MongoDB
- Unstructured data
- Data ingestion logs
- AI analytics cache
- User sessions

## Middleware

### Logging Middleware
- Logs all requests and responses
- Includes processing time
- Logs to both console and file

### Security Headers Middleware
- Adds security headers to responses
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security header

## Error Handling

Custom exceptions:
- `AppException`: Base exception
- `NotFoundError`: Resource not found (404)
- `ValidationError`: Validation failed (422)
- `AuthenticationError`: Authentication failed (401)
- `AuthorizationError`: Insufficient permissions (403)
- `DatabaseError`: Database operation failed (500)

All exceptions return consistent JSON format:
```json
{
    "error": "Error message",
    "details": {},
    "status_code": 404
}
```

## Configuration

Configuration managed via `config.py` using Pydantic Settings:
- Database connections
- JWT settings
- Security keys
- API endpoints
- Schedules

Environment variables override defaults.

## Testing

Each service should have:
- Unit tests for business logic
- Integration tests for API endpoints
- Mock database for testing

## Future Enhancements

- GraphQL API option
- WebSocket support for real-time updates
- Rate limiting
- API versioning strategy
- Caching layer (Redis)
- Background task queue (Celery)
- Full database models with SQLAlchemy
- Database migrations with Alembic
