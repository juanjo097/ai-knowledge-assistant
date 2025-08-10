"""
Repository module for data access layer.

This module contains repository classes that handle database operations
and data persistence for the AI Knowledge Assistant.
"""

from . import document_repo, chunk_repo

__all__ = [
    'document_repo',
    'chunk_repo'
]
