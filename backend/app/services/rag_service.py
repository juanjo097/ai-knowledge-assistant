from __future__ import annotations
from typing import List, Dict
import numpy as np
from flask import current_app

from config.openai_client import get_client
from config.database import get_session
from ..repos import chunk_repo
from errors import APIError
from vectorstore import load_index

SYSTEM_PROMPT = (
    "You are an assistant that answers using only the provided CONTEXT. "
    "If the information is not in the context, clearly say it is not in the uploaded document. "
    "Cite the relevant fragment ids in your answer (e.g., [chunks: 3,5])."
)

def _embed_query(query: str) -> np.ndarray:
    settings = current_app.config["SETTINGS"]
    client = get_client(settings.OPENAI_API_KEY)
    resp = client.embeddings.create(model=settings.EMBEDDING_MODEL, input=[query])
    vec = np.array([resp.data[0].embedding], dtype=np.float32)
    return vec

def retrieve(doc_id: int, query: str, top_k: int) -> List[Dict]:
    """Return a list of {chunk_id, score, text}."""
    # 1) Embed the user query
    q = _embed_query(query)

    # 2) Load FAISS index and the chunk_id mapping
    try:
        index, chunk_ids = load_index(doc_id)
    except FileNotFoundError:
        raise APIError("No index exists for this document yet. Run /index/build first.", 400)

    # 3) Normalize and search (cosine via inner product)
    q = q.astype(np.float32)
    q /= (np.linalg.norm(q, axis=1, keepdims=True) + 1e-12)
    D, I = index.search(q, top_k)

    # 4) Map FAISS positions back to real chunk_ids
    pos_list = I[0].tolist()
    scores = D[0].tolist()
    chosen_ids = []
    for pos in pos_list:
        if pos < 0 or pos >= len(chunk_ids):
            continue
        chosen_ids.append(chunk_ids[pos])

    # 5) Fetch texts from the DB
    with get_session() as db:
        chunks = chunk_repo.get_by_ids(db, chosen_ids)
    # Keep the FAISS ranking order
    chunk_by_id = {c.id: c for c in chunks}

    results = []
    for pos, score in zip(pos_list, scores):
        if pos < 0 or pos >= len(chunk_ids):
            continue
        cid = chunk_ids[pos]
        c = chunk_by_id.get(cid)
        if not c:
            continue
        results.append({"chunk_id": cid, "score": float(score), "text": c.text})
    return results


def build_context(retrieved: List[Dict]) -> str:
    parts = []
    for r in retrieved:
        parts.append(f"[chunk {r['chunk_id']}]\n" + r["text"])  # simple separator
    return "\n\n---\n\n".join(parts)


def answer(doc_id: int, question: str) -> Dict:
    settings = current_app.config["SETTINGS"]
    client = get_client(settings.OPENAI_API_KEY)

    retrieved = retrieve(doc_id, question, settings.TOP_K)
    if not retrieved or (len(retrieved) > 0 and max(r["score"] for r in retrieved) < 0.1):
        return {"answer": "I can't find that information in the provided document.", "sources": []}

    context = build_context(retrieved)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION: {question}"},
    ]

    resp = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages,
        temperature=0.2,
    )
    text = resp.choices[0].message.content
    sources = [{"chunk_id": r["chunk_id"], "score": r["score"]} for r in retrieved]

    return {"answer": text, "sources": sources}