"""
Configuration settings for the AI Knowledge Assistant.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List


# Default configuration values
DEFAULT_DB_URL = "sqlite:///./data/app.db"
DEFAULT_DATA_DIR = "./data"
DEFAULT_CORS_ORIGINS = "*"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_LLM_MODEL = "gpt-4o-mini"
DEFAULT_TOP_K = 5
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 120
DEFAULT_MAX_UPLOAD_MB = 5
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_ALLOWED_EXT = ["txt", "csv"]


@dataclass
class Settings:
    """Application settings loaded from environment variables."""
    
    # API Configuration
    OPENAI_API_KEY: str | None
    
    # Database Configuration
    DB_URL: str
    DATA_DIR: str
    
    # CORS Configuration
    CORS_ORIGINS: str
    
    # AI Model Configuration
    EMBEDDING_MODEL: str
    LLM_MODEL: str
    
    # RAG Configuration
    TOP_K: int
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    
    # File Upload Configuration
    MAX_UPLOAD_MB: int
    ALLOWED_EXT: List[str]
    
    # Logging Configuration
    LOG_LEVEL: str
    
    @classmethod
    def from_env(cls) -> "Settings":
        """Create Settings instance from environment variables."""
        # Ensure data directory exists
        data_dir = os.getenv("DATA_DIR", DEFAULT_DATA_DIR)
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        
        # Parse allowed extensions
        allowed_ext_raw = os.getenv("ALLOWED_EXT", ",".join(DEFAULT_ALLOWED_EXT))
        allowed_ext = [ext.strip().lower() for ext in allowed_ext_raw.split(",") if ext.strip()]
        
        return cls(
            OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
            DB_URL=os.getenv("DB_URL", DEFAULT_DB_URL),
            DATA_DIR=data_dir,
            CORS_ORIGINS=os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS),
            EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
            LLM_MODEL=os.getenv("LLM_MODEL", DEFAULT_LLM_MODEL),
            TOP_K=int(os.getenv("TOP_K", str(DEFAULT_TOP_K))),
            CHUNK_SIZE=int(os.getenv("CHUNK_SIZE", str(DEFAULT_CHUNK_SIZE))),
            CHUNK_OVERLAP=int(os.getenv("CHUNK_OVERLAP", str(DEFAULT_CHUNK_OVERLAP))),
            MAX_UPLOAD_MB=int(os.getenv("MAX_UPLOAD_MB", str(DEFAULT_MAX_UPLOAD_MB))),
            LOG_LEVEL=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL),
            ALLOWED_EXT=allowed_ext,
        )
    
    @property
    def max_content_length_bytes(self) -> int:
        """Convert MAX_UPLOAD_MB to bytes."""
        return self.MAX_UPLOAD_MB * 1024 * 1024