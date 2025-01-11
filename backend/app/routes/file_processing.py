from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Body
from google.oauth2 import service_account
from googleapiclient.discovery import build
from backend.modules.invoice_processing.factory import ParserFactory
from backend.config import Config
import shutil
import os
import tempfile

router = APIRouter()
config = Config()

def get_gdrive_service():
    creds = service_account.Credentials.from_service_account_file(
        config.GOOGLE_CREDENTIALS_PATH, scopes=['https://www.googleapis.com/auth/drive.readonly'])
    return build('drive', 'v3', credentials=creds)

@router.post("/upload/google-drive")
async def process_google_drive_file(fileId: str = Body(..., embed=True)):
    """Process a file uploaded from Google Drive."""
    try:
        drive_service = get_gdrive_service()
        file_metadata = drive_service.files().get(fileId=fileId, fields='name, mimeType').execute()
        filename = file_metadata.get('name')
        mime_type = file_metadata.get('mimeType')

        # Download the file content
        request = drive_service.files().get_media(fileId=fileId)
        file_content = request.execute()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
            tmp_file.write(file_content)
            temp_file_path = tmp_file.name

        # Process the file
        parser = ParserFactory.create_parser(file_content, 'auto') # Adjust extraction_option as needed
        data = await parser._process_file(temp_file_path)

        return {"filename": filename, "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path:
            os.unlink(temp_file_path)

@router.post("/upload")
async def process_files(
    files: List[UploadFile] = File(...),
    extraction_option: str = Form("auto"),
    delimiter: str = Form(None),
    template: str = Form(None),
):
    """Upload multiple local files for processing."""
    results = []
    for file in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            temp_file_path = tmp_file.name

        try:
            parser = ParserFactory.create_parser(file, extraction_option, delimiter, template)
            data = await parser._process_file(temp_file_path)
            results.append(
                {
                    "filename": file.filename,
                    "data": data,
                    "extraction_option": extraction_option,
                    "delimiter": delimiter,
                    "template": template,
                }
            )
        except ValueError as ve:
            os.unlink(temp_file_path)
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            os.unlink(temp_file_path)
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            os.unlink(temp_file_path)

    return results
