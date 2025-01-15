from fastapi import APIRouter, UploadFile, HTTPException, Depends
from typing import List, Dict
from backend.services.document_service import DocumentService

router = APIRouter(prefix="/api/documents")

@router.post("/upload/")
async def upload_document(file: UploadFile):
    return await DocumentService.upload(file)

@router.post("/{doc_id}/process/")
async def process_document(doc_id: str):
    return await DocumentService.process(doc_id)

@router.get("/{doc_id}/status/")
async def get_processing_status(doc_id: str):
    return await DocumentService.get_status(doc_id)
