from __future__ import annotations
from sqlalchemy.orm import Session
from ..models import Document


def get_by_checksum(db: Session, checksum: str) -> Document | None:
    return db.query(Document).filter_by(checksum=checksum).first()


def create(db: Session, *, filename: str, mime: str, checksum: str) -> Document:
    doc = Document(filename=filename, mime=mime, checksum=checksum)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc