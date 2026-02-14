"""
Custom exceptions and error handlers
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger
from typing import Optional


class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 500, details: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppException):
    """Resource not found exception"""
    def __init__(self, resource: str, identifier: Optional[str] = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, status_code=404)


class ValidationError(AppException):
    """Validation error exception"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, status_code=422, details=details)


class AuthenticationError(AppException):
    """Authentication error exception"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(AppException):
    """Authorization error exception"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class DatabaseError(AppException):
    """Database error exception"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=500)


# Exception handlers
async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions"""
    logger.error(f"Application error: {exc.message} - {exc.details}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
            "status_code": exc.status_code
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions"""
    errors = exc.errors()
    logger.warning(f"Validation error: {errors}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "details": errors,
            "status_code": 422
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.exception(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": {"message": str(exc)} if str(exc) else {},
            "status_code": 500
        }
    )
