"""
Repository module for data access layer.

This module contains repository classes that handle database operations
and data persistence for the AI Knowledge Assistant.
"""

from .document_repo import get_by_checksum as document_get_by_checksum, create as document_create
from .chunk_repo import exists_for_doc as chunks_exist_for_doc, list_by_doc as chunks_list_by_doc, bulk_insert as chunks_bulk_insert

__all__ = [
    "document_get_by_checksum",
    "document_create",
    "chunks_exist_for_doc",
    "chunks_list_by_doc",
    "chunks_bulk_insert",
]