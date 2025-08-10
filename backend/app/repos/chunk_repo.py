from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models import Chunk


def exists_for_doc(db: Session, doc_id: int) -> bool:
    return db.query(Chunk).filter_by(doc_id=doc_id).first() is not None


def list_by_doc(db: Session, doc_id: int) -> list[Chunk]:
    stmt = select(Chunk).where(Chunk.doc_id == doc_id).order_by(Chunk.order)
    return list(db.execute(stmt).scalars())


def bulk_insert(db: Session, rows: list[Chunk]):
    db.add_all(rows)
    db.commit()