from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from backend.services.export_service import ExportService
from backend.utils.validators import DataValidator

router = APIRouter(prefix="/api/export")

@router.post("/excel")
async def export_excel(data: dict):
    try:
        DataValidator.validate_export_data(data)
        result = await ExportService.export_excel(data)
        return {"success": True, "file_url": result}
    except ValidationError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, "Error en exportación")

@router.post("/sheets")
async def export_sheets(data: dict):
    try:
        DataValidator.validate_export_data(data)
        result = await ExportService.export_sheets(data)
        return {"success": True, "file_url": result}
    except ValidationError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, "Error en exportación a Sheets")
