"""
Configuration package for the AI Knowledge Assistant backend.
"""

from .config import Settings
from .openai_client import OpenAI

__all__ = ['Settings', 'OpenAI']
