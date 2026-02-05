"""Health check router for monitoring and observability."""

from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from src.core.config import settings
from src.models.schemas import HealthCheck, HealthStatus, ReadinessCheck

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """
    Basic health check endpoint.

    Returns application health status for load balancers and monitoring.
    """
    return HealthCheck(
        status=HealthStatus.HEALTHY,
        version=settings.app_version,
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/ready", response_model=ReadinessCheck)
async def readiness_check() -> ReadinessCheck:
    """
    Readiness check endpoint.

    Returns detailed readiness status including dependency checks.
    Used by Kubernetes/orchestrators to determine if service can accept traffic.
    """
    checks = {
        "config_loaded": True,
        # Future checks will be added here:
        # "database": check_database_connection(),
        # "vector_store": check_vector_store_connection(),
        # "cache": check_redis_connection(),
    }

    all_healthy = all(checks.values())

    return ReadinessCheck(
        status=HealthStatus.HEALTHY if all_healthy else HealthStatus.UNHEALTHY,
        checks=checks,
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/metrics", response_class=PlainTextResponse)
async def metrics() -> str:
    """
    Prometheus metrics endpoint.

    Returns metrics in Prometheus text format.
    """
    # Basic metrics for MVP - will be enhanced with prometheus_client in future
    metrics_output = []

    # Application info metric
    metrics_output.append(
        f'# HELP app_info Application information\n'
        f'# TYPE app_info gauge\n'
        f'app_info{{version="{settings.app_version}",app_name="{settings.app_name}"}} 1'
    )

    # Health status metric (1 = healthy, 0 = unhealthy)
    metrics_output.append(
        f'# HELP app_health_status Application health status\n'
        f'# TYPE app_health_status gauge\n'
        f'app_health_status 1'
    )

    return "\n\n".join(metrics_output)
