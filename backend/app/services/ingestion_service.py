from __future__ import annotations
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import io
import csv
import os  
from flask import current_app

from config.database import get_session
from app.utils.text import normalize_text, sha256_hex
from app.repos import document_repo
from errors.exceptions import APIError


def _allowed(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in set(current_app.config["SETTINGS"].ALLOWED_EXT)


def _parse_file_to_text(storage: FileStorage) -> tuple[str, str]:
    filename = storage.filename or "upload"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    raw = storage.stream.read()
    # Intenta decodificar en UTF-8, luego latin-1 como fallback
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError:
        content = raw.decode("latin-1", errors="ignore")

    if ext == "csv":
        reader = csv.reader(io.StringIO(content))
        lines = []
        for row in reader:
            cells = [c.strip() for c in row]
            if any(cells):
                lines.append(" | ".join(cells))
        text = "\n".join(lines)
        return normalize_text(text), "text/csv"

    # default = txt
    return normalize_text(content), "text/plain"


def ingest_file(storage: FileStorage) -> dict:
    """Valida y persiste el documento normalizado.
    Devuelve {doc_id, filename, mime, reused, stats}.
    """
    settings = current_app.config["SETTINGS"]

    if not storage or not storage.filename:
        raise APIError("Archivo no proporcionado", 400)

    filename = secure_filename(storage.filename)
    if not _allowed(filename):
        raise APIError(
            f"Extensión no permitida. Permitidas: {settings.ALLOWED_EXT}", 400
        )

    text, mime = _parse_file_to_text(storage)
    if not text.strip():
        raise APIError("El archivo está vacío tras normalización", 400)

    checksum = sha256_hex(text)

    with get_session() as db:
        existing = document_repo.get_by_checksum(db, checksum)
        if existing:
            doc, reused = existing, True
        else:
            doc = document_repo.create(db, filename=filename, mime=mime, checksum=checksum)
            reused = False

    # Persistir contenido normalizado a disco
    docs_dir = os.path.join(settings.DATA_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    path = os.path.join(docs_dir, f"{doc.id}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    lines = text.count("\n") + 1
    chars = len(text)

    return {
        "doc_id": doc.id,
        "filename": filename,
        "mime": mime,
        "reused": reused,
        "stats": {"lines": lines, "chars": chars},
    }