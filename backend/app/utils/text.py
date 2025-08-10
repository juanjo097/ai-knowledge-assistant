from __future__ import annotations
import re
import unicodedata
import hashlib


_WHITESPACE_RE = re.compile(r"[ \t\x0b\x0c\r]+")
_MULTINEWLINE_RE = re.compile(r"\n{3,}")


def normalize_text(text: str) -> str:
    """Normalizes text to make it consistent before chunking/embedding.
    - Unicode to NFKC
    - Normalizes line breaks to \n
    - Collapses repeated spaces and tabs, keeps \n as paragraph separator
    - Reduces multiple consecutive \n to maximum 2
    - Trims spaces on both sides of each line
    """
    if not text:
        return ""
    t = unicodedata.normalize("NFKC", text)
    # Normalize line breaks \r\n, \r -> \n
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse multiple spaces/tabs but keep line breaks
    t = _WHITESPACE_RE.sub(" ", t)
    # Trim spaces on both sides of each line
    t = "\n".join(line.strip() for line in t.split("\n"))
    # Limit consecutive line breaks to 2 (to not lose paragraph separation)
    t = _MULTINEWLINE_RE.sub("\n\n", t)
    return t.strip()


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()