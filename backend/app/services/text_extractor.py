import io
from pathlib import Path
from typing import Union


def extract_text_from_file(file_path: Union[str, Path]) -> str:
    """Extracts raw text from a text file, PDF, or DOCX on disk."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    ext = path.suffix.lower()

    if ext == ".txt":
        return path.read_text(encoding="utf-8", errors="replace")

    elif ext == ".pdf":
        try:
            import pdfplumber
            text_parts = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    txt = page.extract_text()
                    if txt:
                        text_parts.append(txt)
            return "\n\n".join(text_parts)
        except ImportError:
            # Fallback if pdfplumber not installed
            return f"[PDF raw extraction fallback for {path.name}]"

    elif ext in [".docx", ".doc"]:
        try:
            import docx
            doc = docx.Document(path)
            return "\n".join([p.text for p in doc.paragraphs if p.text])
        except ImportError:
            return f"[DOCX raw extraction fallback for {path.name}]"

    else:
        # Default try utf-8 text
        return path.read_text(encoding="utf-8", errors="replace")


def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    """Extracts raw text from in-memory bytes of uploaded file."""
    ext = Path(filename).suffix.lower()

    if ext == ".txt":
        return file_bytes.decode("utf-8", errors="replace")

    elif ext == ".pdf":
        try:
            import pdfplumber
            text_parts = []
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    txt = page.extract_text()
                    if txt:
                        text_parts.append(txt)
            return "\n\n".join(text_parts)
        except Exception as e:
            return f"Error extracting PDF: {e}"

    elif ext in [".docx", ".doc"]:
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            return "\n".join([p.text for p in doc.paragraphs if p.text])
        except Exception as e:
            return f"Error extracting DOCX: {e}"

    else:
        return file_bytes.decode("utf-8", errors="replace")
