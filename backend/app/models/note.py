"""
Note model for storing user notes and annotations.
"""

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime

from .base import Base


class Note(Base):
    """Note model for storing user notes and annotations."""
    
    __tablename__ = "notes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}')>"
