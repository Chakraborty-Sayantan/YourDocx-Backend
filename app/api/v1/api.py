from fastapi import APIRouter
from app.api.v1.endpoints import (
    redactor,
    merge,
    split,
    watermark,
    encrypt,
    ocr,
)

api_router = APIRouter()

api_router.include_router(redactor.router, tags=["tools"])
api_router.include_router(merge.router,    tags=["tools"])
api_router.include_router(split.router,    tags=["tools"])
api_router.include_router(watermark.router,tags=["tools"])
api_router.include_router(encrypt.router,  tags=["tools"])
api_router.include_router(ocr.router,      tags=["tools"])
