"""
Middleware initialization for the backend application.
"""

from .auth_middleware import auth_middleware

__all__ = ['auth_middleware']