from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path

def add_watermark(src: Path, dst: Path, text: str) -> None:
    reader = PdfReader(str(src))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.write(str(dst))