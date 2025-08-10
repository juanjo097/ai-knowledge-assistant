from __future__ import annotations
from flask import Blueprint, request, jsonify
from ..services.ingestion_service import ingest_file

bp = Blueprint("upload", __name__, url_prefix="/upload")


@bp.post("")
def upload():
    file = request.files.get("file")
    result = ingest_file(file)
    return jsonify(result), 201