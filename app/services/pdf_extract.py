from PyPDF2 import PdfReader

def extract_text(path: str) -> str:
    reader = PdfReader(path)
    return "".join(page.extract_text() or "" for page in reader.pages)