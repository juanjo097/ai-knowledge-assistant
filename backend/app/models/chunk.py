"""
Chunk model for storing document text fragments.
"""

from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, DateTime, ForeignKey, Index

from .base import Base

if TYPE_CHECKING:
    from .document import Document


class Chunk(Base):
    """Chunk model for storing document text fragments."""
    
    __tablename__ = "chunks"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    doc_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    order: Mapped[int] = mapped_column(Integer)  # chunk index within document
    text: Mapped[str] = mapped_column(Text)
    start: Mapped[int] = mapped_column(Integer)  # character offset (approximate)
    end: Mapped[int] = mapped_column(Integer)
    token_count: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document: Mapped["Document"] = relationship(back_populates="chunks")
    
    # Composite index for efficient document chunk retrieval
    __table_args__ = (
        Index("ix_chunks_doc_order", "doc_id", "order"),
    )
    
    def __repr__(self):
        return f"<Chunk(id={self.id}, doc_id={self.doc_id}, order={self.order})>"
