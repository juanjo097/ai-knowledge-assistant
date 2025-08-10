from __future__ import annotations
from werkzeug.datastructures import FileStorage
from . import ingestion_service, chunk_service, embedding_service
from errors import APIError


def ingest_and_index(storage: FileStorage) -> dict:
    """One-shot pipeline: upload -> normalize -> store -> chunk -> embed -> FAISS index.
    Returns a compact summary for the frontend to keep state.
    """
    if not storage:
        raise APIError("Missing file in form-data field 'file'", 400)

    upload_meta = ingestion_service.ingest_file(storage)
    doc_id = int(upload_meta["doc_id"])  # guaranteed by ingest

    chunk_stats = chunk_service.build_chunks_for_doc(doc_id)
    index_info = embedding_service.build_index_for_doc(doc_id)

    return {
        "doc_id": doc_id,
        "upload": upload_meta,
        "chunks": {
            "count": chunk_stats.count,
            "approx_tokens": chunk_stats.total_tokens,
        },
        "index": index_info,
    }


def process_existing(doc_id: int) -> dict:
    """Rebuild chunks and index for an already ingested document.
    Useful when tweaking CHUNK_SIZE/OVERLAP or re-indexing.
    """
    chunk_stats = chunk_service.build_chunks_for_doc(doc_id)
    index_info = embedding_service.build_index_for_doc(doc_id)
    return {
        "doc_id": doc_id,
        "chunks": {
            "count": chunk_stats.count,
            "approx_tokens": chunk_stats.total_tokens,
        },
        "index": index_info,
    }