from __future__ import annotations
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

_engine = None
Session = None


def _sqlite_connect_args(db_url: str) -> dict:
    if db_url.startswith("sqlite"):  # sqlite:///./data/app.db
        return {"check_same_thread": False}
    return {}


def init_db(app) -> None:
    """Initialize the engine and global session.
    - Creates tables if they don't exist.
    - Applies useful PRAGMAs for SQLite.
    - Registers teardown to close sessions per request.
    """
    from .config import Settings
    from app.models import Base  # import after to avoid cycles

    settings: Settings = app.config["SETTINGS"]

    global _engine, Session
    _engine = create_engine(
        settings.DB_URL,
        future=True,
        echo=False,
        connect_args=_sqlite_connect_args(settings.DB_URL),
    )

    # Useful PRAGMAs for SQLite
    if settings.DB_URL.startswith("sqlite"):
        with _engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys = ON"))
            conn.execute(text("PRAGMA journal_mode = WAL"))
            conn.commit()

    # Create tables
    Base.metadata.create_all(_engine)

    # Per-request session
    Session = scoped_session(
        sessionmaker(bind=_engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)
    )

    @app.teardown_appcontext
    def remove_session(exc: Optional[BaseException] = None):
        if Session is not None:
            Session.remove()


def get_session():
    """Gets the current session (scoped). Use with `with get_session() as s:` if desired.
    Note: in Flask, removal is handled in `teardown_appcontext`.
    """
    if Session is None:
        raise RuntimeError("DB not initialized. Call init_db(app) in create_app().")
    return Session()