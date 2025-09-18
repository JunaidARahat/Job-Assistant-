from pathlib import Path
from typing import List
try:
    import PyPDF2
except Exception:
    PyPDF2 = None

def extract_text_from_pdf(path: str) -> str:
    if PyPDF2 is None:
        return ''
    text_parts = []
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text() or ''
            text_parts.append(page_text)
    return '\n'.join(text_parts)

def load_text_file(path: str) -> str:
    return Path(path).read_text(encoding='utf-8')

def chunk_text(text: str, chunk_size: int = 250, overlap: int = 50) -> List[str]:
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = ' '.join(tokens[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks
