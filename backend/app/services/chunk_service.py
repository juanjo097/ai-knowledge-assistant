from __future__ import annotations
from dataclasses import dataclass
import os
from flask import current_app
from config.database import get_session
from ..models import Chunk
from errors.exceptions import APIError
from ..repos import chunk_repo


@dataclass
class ChunkStats:
    count: int
    total_tokens: int


def _split_text(text: str, size: int, overlap: int) -> list[tuple[str, int, int]]:
    """Splits `text` into fragments by CHARACTERS with overlap.
    MVP: for simplicity; later we can switch to real tokens.
    Returns a list of (fragment, start, end).
    """
    n = len(text)
    chunks = []
    i = 0
    while i < n:
        j = min(i + size, n)
        fragment = text[i:j]
        chunks.append((fragment, i, j))
        if j == n:
            break
        i = max(0, j - overlap)
    return chunks


def build_chunks_for_doc(doc_id: int) -> ChunkStats:
    settings = current_app.config["SETTINGS"]
    path = os.path.join(settings.DATA_DIR, "docs", f"{doc_id}.txt")
    if not os.path.exists(path):
        raise APIError(f"Normalized document not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    parts = _split_text(text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)

    with get_session() as db:
        if chunk_repo.exists_for_doc(db, doc_id):
            # Avoid duplicates if already processed before
            existing = chunk_repo.list_by_doc(db, doc_id)
            total_tokens = sum(len(c.text.split()) for c in existing)
            return ChunkStats(count=len(existing), total_tokens=total_tokens)

        rows: list[Chunk] = []
        total_tokens = 0
        for idx, (frag, start, end) in enumerate(parts):
            token_count = len(frag.split())  # approximation by words
            total_tokens += token_count
            rows.append(
                Chunk(doc_id=doc_id, order=idx, text=frag, start=start, end=end, token_count=token_count)
            )
        chunk_repo.bulk_insert(db, rows)

    return ChunkStats(count=len(parts), total_tokens=total_tokens)