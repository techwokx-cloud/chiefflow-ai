import io
from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except Exception:
        return ""


def extract_text_from_upload(filename: str, file_bytes: bytes) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    # .txt, .eml, .md and other plain-text-ish formats
    try:
        return file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return ""
