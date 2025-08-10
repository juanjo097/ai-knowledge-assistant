"""
Document model for storing uploaded files and their metadata.
"""

from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .chunk import Chunk


class Document(Base):
    """Document model for storing file uploads and metadata."""
    
    __tablename__ = "documents"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255))
    mime: Mapped[str] = mapped_column(String(100))
    checksum: Mapped[str] = mapped_column(String(64), index=True)  # sha256 hex of normalized content
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    user: Mapped["User | None"] = relationship(back_populates="documents")
    
    chunks: Mapped[List["Chunk"]] = relationship(
        back_populates="document", cascade="all, delete-orphan", passive_deletes=True
    )
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', user_id={self.user_id})>"
