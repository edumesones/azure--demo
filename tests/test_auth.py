"""Tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.core.security import security_service


class TestAuthEndpoints:
    """Test class for authentication endpoints."""

    def test_login_with_valid_credentials(self, test_client: TestClient) -> None:
        """Test login with valid admin credentials."""
        response = test_client.post(
            "/api/v1/auth/token",
            data={
                "username": "admin@datacatalog.ai",
                "password": "admin123secure",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data

    def test_login_with_invalid_password(self, test_client: TestClient) -> None:
        """Test login with wrong password returns 401."""
        response = test_client.post(
            "/api/v1/auth/token",
            data={
                "username": "admin@datacatalog.ai",
                "password": "wrongpassword",
            },
        )

        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    def test_login_with_invalid_email(self, test_client: TestClient) -> None:
        """Test login with non-existent email returns 401."""
        response = test_client.post(
            "/api/v1/auth/token",
            data={
                "username": "nonexistent@datacatalog.ai",
                "password": "anypassword",
            },
        )

        assert response.status_code == 401

    def test_refresh_token_with_valid_token(
        self, test_client: TestClient
    ) -> None:
        """Test refreshing access token with valid refresh token."""
        # First login to get tokens
        login_response = test_client.post(
            "/api/v1/auth/token",
            data={
                "username": "admin@datacatalog.ai",
                "password": "admin123secure",
            },
        )
        refresh_token = login_response.json()["refresh_token"]

        # Use refresh token
        response = test_client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_refresh_token_with_invalid_token(
        self, test_client: TestClient
    ) -> None:
        """Test refreshing with invalid token returns 401."""
        response = test_client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid-token"},
        )

        assert response.status_code == 401

    def test_refresh_token_with_access_token(
        self, test_client: TestClient
    ) -> None:
        """Test that access token cannot be used for refresh."""
        # Login to get access token
        login_response = test_client.post(
            "/api/v1/auth/token",
            data={
                "username": "admin@datacatalog.ai",
                "password": "admin123secure",
            },
        )
        access_token = login_response.json()["access_token"]

        # Try to use access token for refresh (should fail)
        response = test_client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": access_token},
        )

        assert response.status_code == 401


class TestSecurityService:
    """Test class for security service functions."""

    def test_password_hashing(self) -> None:
        """Test password hashing and verification."""
        password = "mysecurepassword123"
        hashed = security_service.hash_password(password)

        assert hashed != password
        assert security_service.verify_password(password, hashed)

    def test_password_verification_fails_for_wrong_password(self) -> None:
        """Test that wrong password fails verification."""
        password = "correctpassword"
        wrong_password = "wrongpassword"
        hashed = security_service.hash_password(password)

        assert not security_service.verify_password(wrong_password, hashed)

    def test_access_token_creation(self) -> None:
        """Test access token creation."""
        data = {"sub": "user-123", "email": "test@example.com", "role": "editor"}
        token = security_service.create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_access_token_verification(self) -> None:
        """Test access token verification."""
        data = {"sub": "user-123", "email": "test@example.com", "role": "editor"}
        token = security_service.create_access_token(data)

        payload = security_service.verify_token(token, "access")

        assert payload["sub"] == "user-123"
        assert payload["email"] == "test@example.com"
        assert payload["type"] == "access"

    def test_refresh_token_creation_and_verification(self) -> None:
        """Test refresh token creation and verification."""
        data = {"sub": "user-123", "email": "test@example.com", "role": "editor"}
        token = security_service.create_refresh_token(data)

        payload = security_service.verify_token(token, "refresh")

        assert payload["sub"] == "user-123"
        assert payload["type"] == "refresh"

    def test_token_type_mismatch_raises_error(self) -> None:
        """Test that verifying token with wrong type raises error."""
        from src.core.exceptions import InvalidTokenError

        data = {"sub": "user-123", "email": "test@example.com", "role": "editor"}
        access_token = security_service.create_access_token(data)

        with pytest.raises(InvalidTokenError):
            security_service.verify_token(access_token, "refresh")
