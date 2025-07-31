import uuid, shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from app.core.config import settings
from app.services.pdf_encrypt import encrypt_pdf

router = APIRouter()

@router.post("/encrypt")
async def encrypt(file: UploadFile = File(...), password: str = File(...)):
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    uid = uuid.uuid4().hex
    src = upload_dir / f"{uid}_{file.filename}"
    dst = src.with_stem(src.stem + "_encrypted")

    with open(src, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    encrypt_pdf(src, dst, password)
    return {"url": f"/api/v1/download/{dst.name}"}