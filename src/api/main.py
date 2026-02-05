"""FastAPI application factory and configuration."""

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware
from src.api.routers import auth, health, search
from src.core.config import settings


def configure_logging() -> None:
    """Configure structlog for JSON logging."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            (
                structlog.processors.JSONRenderer()
                if settings.log_format == "json"
                else structlog.dev.ConsoleRenderer()
            ),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            structlog.stdlib._NAME_TO_LEVEL[settings.log_level.lower()]
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def create_application() -> FastAPI:
    """
    Application factory for creating FastAPI instance.

    Returns:
        Configured FastAPI application
    """
    # Configure logging
    configure_logging()

    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Intelligent data catalog with RAG-powered natural language querying",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom middleware (order matters - last added is first executed)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    # Include routers
    app.include_router(health.router, prefix="/api/v1")
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(search.router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup_event() -> None:
        """Application startup tasks."""
        logger = structlog.get_logger(__name__)
        logger.info(
            "application_startup",
            app_name=settings.app_name,
            version=settings.app_version,
            debug=settings.debug,
        )

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        """Application shutdown tasks."""
        logger = structlog.get_logger(__name__)
        logger.info("application_shutdown")

    return app


# Create application instance
app = create_application()


# Entry point for running with uvicorn directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
