import uuid, shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from app.core.config import settings
from app.services.ocr_service import extract_text_from_image

router = APIRouter()

@router.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    uid = uuid.uuid4().hex
    src = upload_dir / f"{uid}_{file.filename}"
    with open(src, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_image(src)
    return {"text": text}