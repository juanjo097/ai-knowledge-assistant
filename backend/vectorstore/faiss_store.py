from __future__ import annotations
import os
import json
from typing import Tuple, List

import faiss
import numpy as np
from flask import current_app


def _paths(doc_id: int) -> Tuple[str, str]:
    base = os.path.join(current_app.config["SETTINGS"].DATA_DIR, "indexes")
    os.makedirs(base, exist_ok=True)
    return (
        os.path.join(base, f"{doc_id}.faiss"),
        os.path.join(base, f"{doc_id}.meta.json"),
    )


def save_index(doc_id: int, vectors: np.ndarray, chunk_ids: List[int]) -> None:
    """Guarda un índice FAISS (cosine via inner product sobre vectores normalizados)."""
    if vectors.ndim != 2:
        raise ValueError("vectors debe ser 2D: (n, d)")

    # Normalizamos para usar similitud coseno con IndexFlatIP
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    vecs = (vectors / norms).astype(np.float32)

    d = vecs.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(vecs)

    idx_path, meta_path = _paths(doc_id)
    faiss.write_index(index, idx_path)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({"chunk_ids": chunk_ids}, f)


def load_index(doc_id: int) -> Tuple[faiss.IndexFlatIP, List[int]]:
    idx_path, meta_path = _paths(doc_id)
    if not (os.path.exists(idx_path) and os.path.exists(meta_path)):
        raise FileNotFoundError("No existe índice FAISS para este documento")
    index = faiss.read_index(idx_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return index, meta["chunk_ids"]


def search(doc_id: int, query_vec: np.ndarray, top_k: int) -> tuple[np.ndarray, np.ndarray]:
    index, _ = load_index(doc_id)
    if query_vec.ndim == 1:
        query_vec = query_vec.reshape(1, -1)

    # Normaliza query para coseno
    q = query_vec.astype(np.float32)
    q /= (np.linalg.norm(q, axis=1, keepdims=True) + 1e-12)

    D, I = index.search(q, top_k)
    return D, I