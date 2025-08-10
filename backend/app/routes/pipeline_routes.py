from __future__ import annotations
from flask import Blueprint, request, jsonify
from ..services import pipeline_service

bp = Blueprint("pipeline", __name__, url_prefix="/pipeline")


@bp.post("/ingest")
def ingest():
    """Multipart endpoint that runs the full pipeline in one request.
    Body: multipart/form-data with a single field 'file'.
    Returns: { doc_id, upload, chunks, index }
    """
    storage = request.files.get("file")
    out = pipeline_service.ingest_and_index(storage)
    return jsonify(out), 201


@bp.post("/process/<int:doc_id>")
def process(doc_id: int):
    """Process an existing document id (chunk + index).
    Useful when the file is already uploaded or to rebuild with new params.
    """
    out = pipeline_service.process_existing(int(doc_id))
    return jsonify(out), 200