import uuid, shutil, json, os, datetime
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import fitz
from app.core.config import settings

router = APIRouter(tags=["redactor"])

UPLOAD_DIR = Path(settings.upload_dir)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = UPLOAD_DIR / "history.json"

# helpers -------------------------------------------------------------
def save_record(record: dict):
    record["date"] = datetime.datetime.utcnow().isoformat()
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    records = json.loads(HISTORY_FILE.read_text()) if HISTORY_FILE.exists() else []
    records.insert(0, record)
    HISTORY_FILE.write_text(json.dumps(records[:50], indent=2))

def extract_text(path: str) -> str:
    return "".join(page.extract_text() or "" for page in fitz.open(path))

def detect_pii(text: str):
    import re, spacy
    nlp = spacy.load("en_core_web_sm")
    ents = []
    for ent in nlp(text).ents:
        ents.append({"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char})
    return ents

def apply_boxes(src: str, dst: str, boxes: list):
    doc = fitz.open(src)
    for b in boxes:
        rect = fitz.Rect(b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"])
        page = doc[b["page"] - 1]
        page.add_redact_annot(rect, fill=(0, 0, 0))
        page.apply_redactions()
    doc.save(dst)
    doc.close()

# endpoints -----------------------------------------------------------
@router.post("/redact/auto")
async def auto_redact(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    src = UPLOAD_DIR / f"{file_id}_{file.filename}"
    dst = src.with_stem(src.stem + "_auto")

    with open(src, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text(str(src))
    entities = detect_pii(text)
    boxes = [{"x": 100, "y": 200 + i * 25, "w": 150, "h": 20, "page": 1} for i, _ in enumerate(entities)]
    apply_boxes(str(src), str(dst), boxes)

    record = {"id": file_id, "original_name": file.filename, "url": f"/api/v1/download/{dst.name}"}
    save_record(record)
    return {"url": record["url"]}

@router.post("/redact/manual")
async def manual_redact(
    file: UploadFile = File(...),
    boxes: str = Form(...),  # JSON list [{"x":..,"y":..,"w":..,"h":..,"page":..}]
):
    file_id = str(uuid.uuid4())
    src = UPLOAD_DIR / f"{file_id}_{file.filename}"
    dst = src.with_stem(src.stem + "_manual")

    with open(src, "wb") as f:
        shutil.copyfileobj(file.file, f)

    apply_boxes(str(src), str(dst), json.loads(boxes))
    save_record({"id": file_id, "original_name": file.filename, "url": f"/api/v1/download/{dst.name}"})
    return {"url": f"/api/v1/download/{dst.name}"}

@router.get("/download/{filename}")
def download(filename: str):
    path = UPLOAD_DIR / filename
    if not path.exists():
        raise HTTPException(404, "File not found")
    return FileResponse(path, media_type="application/pdf")

@router.get("/preview/{filename}")
def preview(filename: str, page: int = 1, dpi: int = 200):
    path = UPLOAD_DIR / filename
    if not path.exists():
        raise HTTPException(404, "File not found")
    import io
    doc = fitz.open(path)
    pix = doc[page - 1].get_pixmap(dpi=dpi)
    return io.BytesIO(pix.tobytes("png"))

@router.get("/history")
def history(limit: int = 50):
    return json.loads(HISTORY_FILE.read_text()) if HISTORY_FILE.exists() else []

@router.delete("/history/{record_id}")
def delete_record(record_id: str):
    records = json.loads(HISTORY_FILE.read_text()) if HISTORY_FILE.exists() else []
    new = [r for r in records if r["id"] != record_id]
    HISTORY_FILE.write_text(json.dumps(new))
    return {"ok": True}