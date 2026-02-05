"""Tests for health check endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test class for health check endpoints."""

    def test_health_check_returns_200(self, test_client: TestClient) -> None:
        """Test that /health endpoint returns 200 OK."""
        response = test_client.get("/api/v1/health")

        assert response.status_code == 200

    def test_health_check_returns_healthy_status(
        self, test_client: TestClient
    ) -> None:
        """Test that /health endpoint returns healthy status."""
        response = test_client.get("/api/v1/health")
        data = response.json()

        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data

    def test_readiness_check_returns_200(self, test_client: TestClient) -> None:
        """Test that /ready endpoint returns 200 OK."""
        response = test_client.get("/api/v1/ready")

        assert response.status_code == 200

    def test_readiness_check_includes_checks(
        self, test_client: TestClient
    ) -> None:
        """Test that /ready endpoint includes dependency checks."""
        response = test_client.get("/api/v1/ready")
        data = response.json()

        assert data["status"] == "healthy"
        assert "checks" in data
        assert data["checks"]["config_loaded"] is True
        assert "timestamp" in data

    def test_metrics_endpoint_returns_200(self, test_client: TestClient) -> None:
        """Test that /metrics endpoint returns 200 OK."""
        response = test_client.get("/api/v1/metrics")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"

    def test_metrics_endpoint_returns_prometheus_format(
        self, test_client: TestClient
    ) -> None:
        """Test that /metrics endpoint returns Prometheus format."""
        response = test_client.get("/api/v1/metrics")
        content = response.text

        assert "app_info" in content
        assert "app_health_status" in content
        assert "# HELP" in content
        assert "# TYPE" in content
