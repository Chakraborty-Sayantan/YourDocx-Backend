from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path

def split_pdf(src: Path, dst_dir: Path, ranges: list[tuple[int, int]]) -> list[Path]:
    reader = PdfReader(str(src))
    out_files = []
    for i, (start, end) in enumerate(ranges):
        writer = PdfWriter()
        for p in range(start - 1, end):
            writer.add_page(reader.pages[p])
        out = dst_dir / f"part_{i + 1}.pdf"
        writer.write(str(out))
        out_files.append(out)
    return out_files