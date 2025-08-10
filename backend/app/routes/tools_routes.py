from __future__ import annotations
from flask import Blueprint, request, jsonify
from ..services import notes_service
from errors import APIError

bp = Blueprint("tools", __name__, url_prefix="/tools")


@bp.post("/create_note")
def create_note():
    """Create a note from the chat/tool call.
    Body JSON: {"title": "...", "content": "..."}
    """
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    if not title or not content:
        raise APIError("Both 'title' and 'content' are required", 400)
    out = notes_service.create_note(title, content)
    return jsonify(out), 201


@bp.get("/notes")
def list_notes():
    """Helper endpoint to quickly verify persistence from Insomnia."""
    return jsonify(notes_service.list_notes()), 200