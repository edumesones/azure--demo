# DataCatalog AI

Intelligent data catalog with RAG-powered natural language querying.

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)

### Local Development

1. **Clone and install dependencies:**

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

2. **Configure environment:**

```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Run the server:**

```bash
uvicorn src.api.main:app --reload
```

4. **Access the API:**
   - API Docs: http://localhost:8000/api/docs
   - Health Check: http://localhost:8000/api/v1/health

### Using Docker

```bash
cd docker
docker-compose up -d
```

## API Endpoints

### Health
- `GET /api/v1/health` - Health check
- `GET /api/v1/ready` - Readiness check
- `GET /api/v1/metrics` - Prometheus metrics

### Authentication
- `POST /api/v1/auth/token` - Login (OAuth2 password flow)
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user

## Default Users (Development)

| Email | Password | Role |
|-------|----------|------|
| admin@datacatalog.ai | admin123secure | admin |
| editor@datacatalog.ai | editor123secure | editor |
| viewer@datacatalog.ai | viewer123secure | viewer |

## Testing

```bash
pytest tests/ -v
```

## Project Structure

```
src/
├── api/
│   ├── main.py          # FastAPI application factory
│   ├── dependencies.py  # Dependency injection
│   ├── middleware.py    # Request logging, security headers
│   └── routers/
│       ├── auth.py      # Authentication endpoints
│       └── health.py    # Health check endpoints
├── core/
│   ├── config.py        # Pydantic settings
│   ├── security.py      # JWT & password utilities
│   └── exceptions.py    # Custom exceptions
└── models/
    └── schemas.py       # Pydantic schemas
```

## License

MIT
