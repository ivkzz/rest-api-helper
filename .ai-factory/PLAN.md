# Plan - REST API Directory

## Settings
- **Testing**: Yes (pytest)
- **Logging**: Verbose
- **Docs**: Yes (Swagger/Redoc)
- **Database**: PostgreSQL (standard)
- **Geosearch**: SQL formulas (Haversine for radius, comparison for box)
- **Auth**: Static API Key (`X-API-Key`)

## Tasks

### Phase 1: Environment & Setup
1. Initialize Project Structure (`src/`, `alembic/`, `tests/`)
2. Setup `docker-compose.yml` with PostgreSQL and PostGIS
3. Configuration management (environment variables)

### Phase 2: Database Layer
1. Define SQLAlchemy Models (Building, Activity, Organization, Phone)
2. Setup Alembic and create initial migration
3. Implement a seed script to populate the database with test data

### Phase 3: Core API
1. Implement FastAPI application and routing
2. Setup Dependency Injection for database sessions
3. Implement X-API-Key authentication middleware

### Phase 4: Business Logic & Endpoints
1. Implement Organizations list in a specific building
2. Implement Organizations list by activity
3. Implement Geographic search (Radius/Bounding Box)
4. Implement Organization by ID
5. Implement Recursive Activity Search (max 3 levels)
6. Implement Organization search by name

### Phase 5: Testing & Polishing
1. Write unit tests for API endpoints
2. Verify all requirements and constraints
3. Final documentation update
