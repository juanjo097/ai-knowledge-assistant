from __future__ import annotations
from config.database import get_session
from ..models import Note

def create_note(title: str, content: str) -> dict:
    """Persist a note and return a minimal representation.
    Keeping it tiny for the MVP.
    """
    with get_session() as db:
        note = Note(title=title, content=content)
        db.add(note)
        db.commit()
        db.refresh(note)
        return {"id": note.id, "title": note.title}


def list_notes() -> list[dict]:
    """List recent notes (id, title, created_at)."""
    with get_session() as db:
        rows = db.query(Note).order_by(Note.created_at.desc()).all()
        return [
            {"id": n.id, "title": n.title, "created_at": n.created_at.isoformat()}
            for n in rows
        ]