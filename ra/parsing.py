from __future__ import annotations
from typing import IO
import io, re
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None
try:
    import docx  # python-docx
except Exception:
    docx = None

def _read_bytes(fileobj: IO[bytes]) -> bytes:
    if hasattr(fileobj, "getvalue"):
        return fileobj.getvalue()
    return fileobj.read()

def extract_text_pdf(raw: bytes) -> str:
    if fitz is None:
        raise RuntimeError("PyMuPDF not installed. Install 'pymupdf' to extract PDF text.")
    text_parts = []
    with fitz.open(stream=raw, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text("text"))
    return "\n".join(text_parts)

def extract_text_docx(raw: bytes) -> str:
    if docx is None:
        raise RuntimeError("python-docx not installed. Install 'python-docx' to extract DOCX text.")
    bio = io.BytesIO(raw)
    d = docx.Document(bio)
    return "\n".join(p.text for p in d.paragraphs)

def extract_text_from_file(uploaded) -> str:
    name = (uploaded.name or "").lower()
    raw = _read_bytes(uploaded)
    if name.endswith(".pdf"):
        return extract_text_pdf(raw)
    if name.endswith(".docx"):
        return extract_text_docx(raw)
    try:
        return raw.decode("utf-8", errors="ignore")
    except Exception:
        return str(raw)

_WHITESPACE_RE = re.compile(r"\s+")
def clean_text(s: str) -> str:
    s = s.replace("\x00", " ")
    s = _WHITESPACE_RE.sub(" ", s).strip()
    return s
