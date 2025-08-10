from __future__ import annotations
from typing import List
import numpy as np
from flask import current_app

from config.database import get_session
from config.openai_client import get_client
from ..repos import chunk_repo
from errors import APIError
from vectorstore import faiss_store


def _batched(items: List[str], size: int = 96):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def embed_texts(texts: list[str]) -> np.ndarray:
    settings = current_app.config["SETTINGS"]
    client = get_client(settings.OPENAI_API_KEY)

    vecs: list[list[float]] = []
    for batch in _batched(texts, 96):
        resp = client.embeddings.create(model=settings.EMBEDDING_MODEL, input=batch)
        for item in resp.data:
            vecs.append(item.embedding)
    return np.array(vecs, dtype=np.float32)


def build_index_for_doc(doc_id: int) -> dict:
    """Takes the document's chunks, generates embeddings, and builds a FAISS index."""
    with get_session() as db:
        chunks = chunk_repo.list_by_doc(db, doc_id)
    if not chunks:
        raise APIError("The document has no chunks. Please run /chunks/build first.", 400)

    texts = [c.text for c in chunks]
    vectors = embed_texts(texts)

    # Map positions to actual chunk ids
    chunk_ids = [c.id for c in chunks]

    faiss_store.save_index(doc_id, vectors, chunk_ids)
    return {"doc_id": doc_id, "chunks": len(chunks), "dim": int(vectors.shape[1])}
