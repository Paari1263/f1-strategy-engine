"""
Error handling middleware for FastAPI application
Provides consistent error responses across all engines
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback
from typing import Union

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Base exception for API errors"""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class FastF1Error(APIError):
    """Exception for FastF1 library errors"""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, details: dict = None):
        super().__init__(message, status_code, details)


class SessionNotAvailableError(APIError):
    """Exception when FastF1 session is not available"""
    def __init__(self, message: str = "Session data not available", details: dict = None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, details)


class DataNotFoundError(APIError):
    """Exception when requested data is not found"""
    def __init__(self, message: str = "Requested data not found", details: dict = None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, details)


async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle custom API errors"""
    logger.error(f"API Error: {exc.message}", extra={
        "path": request.url.path,
        "status_code": exc.status_code,
        "details": exc.details
    })
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "type": exc.__class__.__name__,
                "details": exc.details,
                "path": request.url.path
            }
        }
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors"""
    logger.warning(f"Validation error: {exc.errors()}", extra={"path": request.url.path})
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Invalid request data",
                "type": "ValidationError",
                "details": exc.errors(),
                "path": request.url.path
            }
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}", extra={"path": request.url.path})
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "HTTPException",
                "details": {},
                "path": request.url.path
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""
    logger.error(
        f"Unexpected error: {str(exc)}",
        extra={
            "path": request.url.path,
            "traceback": traceback.format_exc()
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "An unexpected error occurred",
                "type": "InternalServerError",
                "details": {"error": str(exc)} if logger.level <= logging.DEBUG else {},
                "path": request.url.path
            }
        }
    )


def register_error_handlers(app):
    """Register all error handlers with FastAPI app"""
    app.add_exception_handler(APIError, api_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
