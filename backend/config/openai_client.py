from __future__ import annotations
from openai import OpenAI


def get_client(api_key: str) -> OpenAI:
    """Devuelve un cliente de OpenAI. Separamos esto para facilitar test/mocks."""
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY en el entorno")
    return OpenAI(api_key=api_key)