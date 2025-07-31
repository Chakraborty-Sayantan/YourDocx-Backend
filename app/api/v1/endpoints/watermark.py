import uuid, shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from app.core.config import settings
from app.services.pdf_watermark import add_watermark

router = APIRouter()

@router.post("/watermark")
async def watermark(file: UploadFile = File(...), text: str = File(...)):
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    uid = uuid.uuid4().hex
    src = upload_dir / f"{uid}_{file.filename}"
    dst = src.with_stem(src.stem + "_watermarked")

    with open(src, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    add_watermark(src, dst, text)
    return {"url": f"/api/v1/download/{dst.name}"}