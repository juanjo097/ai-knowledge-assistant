from __future__ import annotations
from flask import Blueprint, request, jsonify
from ..services.rag_service import answer
from errors import APIError

bp = Blueprint("chat", __name__, url_prefix="/chat")


@bp.post("")
def chat():
    data = request.get_json(silent=True) or {}
    doc_id = data.get("doc_id")
    message = data.get("message")
    if not doc_id or not message:
        raise APIError("Missing 'doc_id' and/or 'message'", 400)
    out = answer(int(doc_id), str(message))
    return jsonify(out), 200
