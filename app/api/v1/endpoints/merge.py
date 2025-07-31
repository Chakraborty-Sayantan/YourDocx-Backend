import uuid, shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from app.services.pdf_merge import merge_pdfs
from app.core.config import settings

router = APIRouter()

@router.post("/merge")
async def merge(files: list[UploadFile] = File(...)):
    uid = uuid.uuid4().hex
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    src_paths = []
    for f in files:
        dest = upload_dir / f"{uid}_{f.filename}"
        with open(dest, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)
        src_paths.append(dest)

    out = upload_dir / f"{uid}_merged.pdf"
    merge_pdfs(src_paths, out)
    return {"url": f"/api/v1/download/{out.name}"}