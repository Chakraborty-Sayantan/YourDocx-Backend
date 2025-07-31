import uuid
from pathlib import Path
from fastapi import HTTPException, UploadFile

def validate_pdf(file: UploadFile) -> str:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDFs accepted")
    file_id = uuid.uuid4().hex
    return file_id