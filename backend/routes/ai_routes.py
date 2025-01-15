from fastapi import APIRouter, UploadFile
from services.document_service import DocumentService

router = APIRouter()

@router.post("/documents/analyze/{document_id}")
async def analyze_document(document_id: str):
    return await DocumentService.process(document_id)
