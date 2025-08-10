"""
Simple custom exceptions for the AI Knowledge Assistant API.
"""


class APIError(Exception):
    """Base exception for all API errors."""
    
    def __init__(self, message: str, status_code: int = 500, extra: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.extra = extra or {}


class ValidationError(APIError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class NotFoundError(APIError):
    """Raised when a requested resource is not found."""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=404)

class FileTooLargeError(APIError):
    """Raised when a file is too large."""
    
    def __init__(self, message: str):
        super().__init__(message, status_code=413)