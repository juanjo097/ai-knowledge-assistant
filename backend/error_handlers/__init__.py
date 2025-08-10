"""
Simple error handlers for the AI Knowledge Assistant API.
"""

from .exceptions import APIError, ValidationError, NotFoundError, FileTooLargeError
from .handlers import register_error_handlers

__all__ = [
    'APIError',
    'ValidationError', 
    'NotFoundError',
    'FileTooLargeError',
    'register_error_handlers'
]
