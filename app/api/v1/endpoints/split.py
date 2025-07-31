import uuid, shutil, json
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings

router = APIRouter()

@router.post("/split")
async def split(file: UploadFile = File(...), ranges: str = File(...)):
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    uid = uuid.uuid4().hex
    src = upload_dir / f"{uid}_{file.filename}"
    with open(src, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ranges_list = json.loads(ranges)  # e.g. [[1,3],[4,6]]
    from app.services.pdf_split import split_pdf
    parts = split_pdf(src, upload_dir, ranges_list)

    return {"zip_url": f"/api/v1/download/{Path(parts[0]).stem}_split.zip"}