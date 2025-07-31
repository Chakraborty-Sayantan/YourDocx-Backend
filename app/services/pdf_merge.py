from PyPDF2 import PdfMerger
from pathlib import Path

def merge_pdfs(src_list: list[Path], dst: Path) -> None:
    merger = PdfMerger()
    for s in src_list:
        merger.append(str(s))
    merger.write(str(dst))
    merger.close()