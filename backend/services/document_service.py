from fastapi import UploadFile
from typing import Dict
import os
from backend.config import config
from backend.modules.invoice_processing.factory import create_processor
import uuid
import asyncio
import random

class DocumentService:
    @staticmethod
    async def upload(file: UploadFile) -> Dict[str, str]:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(config.UPLOAD_FOLDER, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"document_id": file_id, "filename": file.filename}

    @staticmethod
    async def process(document_id: str) -> Dict[str, str]:
        # Placeholder for document processing logic
        return {"status": f"Processing document with id: {document_id}"}

    @staticmethod
    async def get_status(document_id: str) -> Dict[str, str]:
        # Simulate fetching document processing status
        await asyncio.sleep(random.randint(1, 5))
        progress = random.randint(0, 100)
        status = "processing"
        if progress == 100:
            status = "completed"
        elif progress < 10:
            status = "pending"
        return {"status": status, "progress": progress}
