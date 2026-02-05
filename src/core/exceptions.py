"""Custom exceptions for the application."""

from fastapi import HTTPException, status


class DataCatalogException(Exception):
    """Base exception for DataCatalog AI."""

    def __init__(self, message: str = "An error occurred"):
        self.message = message
        super().__init__(self.message)


class AuthenticationError(DataCatalogException):
    """Authentication related errors."""

    pass


class InvalidTokenError(AuthenticationError):
    """Invalid JWT token."""

    pass


class TokenExpiredError(AuthenticationError):
    """JWT token has expired."""

    pass


class InvalidCredentialsError(AuthenticationError):
    """Invalid username or password."""

    pass


class InsufficientPermissionsError(DataCatalogException):
    """User doesn't have required permissions."""

    pass


# HTTP Exception factories for common errors
def credentials_exception() -> HTTPException:
    """Create a 401 Unauthorized exception."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def invalid_credentials_exception() -> HTTPException:
    """Create a 401 exception for invalid credentials."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def token_expired_exception() -> HTTPException:
    """Create a 401 exception for expired token."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden_exception(detail: str = "Insufficient permissions") -> HTTPException:
    """Create a 403 Forbidden exception."""
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )
