"""
Base model configuration for SQLAlchemy 2.0.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass
