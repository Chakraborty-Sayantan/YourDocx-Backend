import pytesseract
from PIL import Image
from pathlib import Path

def extract_text_from_image(image_path: Path) -> str:
    return pytesseract.image_to_string(Image.open(image_path))