from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path

def encrypt_pdf(src: Path, dst: Path, password: str) -> None:
    reader = PdfReader(str(src))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)
    writer.write(str(dst))

def decrypt_pdf(src: Path, dst: Path, password: str) -> None:
    reader = PdfReader(str(src))
    if reader.is_encrypted:
        reader.decrypt(password)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.write(str(dst))