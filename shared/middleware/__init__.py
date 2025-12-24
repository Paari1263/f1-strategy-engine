"""Middleware package"""
from .error_handler import (
    APIError,
    FastF1Error,
    SessionNotAvailableError,
    DataNotFoundError,
    register_error_handlers
)

__all__ = [
    "APIError",
    "FastF1Error",
    "SessionNotAvailableError",
    "DataNotFoundError",
    "register_error_handlers"
]
