from __future__ import annotations
from flask import Blueprint, request, jsonify
from ..services.chunk_service import build_chunks_for_doc
from errors.exceptions import APIError

bp = Blueprint("chunk", __name__, url_prefix="/chunks")


@bp.post("/build")
def build_chunks():
    data = request.get_json(silent=True) or {}
    
    doc_id = data.get("doc_id")
    if not doc_id:
        raise APIError("Falta 'doc_id' en el cuerpo JSON", 400)
    stats = build_chunks_for_doc(int(doc_id))
    return jsonify({"doc_id": int(doc_id), "chunks": stats.count, "approx_tokens": stats.total_tokens}), 201