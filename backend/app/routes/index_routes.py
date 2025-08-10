from __future__ import annotations
from flask import Blueprint, request, jsonify
from ..services.embedding_service import build_index_for_doc
from errors import APIError

bp = Blueprint("indexing", __name__, url_prefix="/index")


@bp.post("/build")
def build_index():
    data = request.get_json(silent=True) or {}
    doc_id = data.get("doc_id")
    if not doc_id:
        raise APIError("Falta 'doc_id'", 400)
    info = build_index_for_doc(int(doc_id))
    return jsonify(info), 201