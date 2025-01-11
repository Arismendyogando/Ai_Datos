import re
import mimetypes
from typing import Dict, Any
from pathlib import Path
from ..utils.logger import setup_logger

logger = setup_logger()

class FileValidator:
    """Class for file validation operations"""
    
    ALLOWED_MIME_TYPES = {
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
        'application/pdf',
        'image/jpeg',
        'image/png'
    }
    
    @classmethod
    def validate_mime_type(cls, file_path: str) -> bool:
        """Validate file MIME type"""
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type not in cls.ALLOWED_MIME_TYPES:
            logger.error(f"Invalid MIME type: {mime_type}")
            return False
        return True
        
    @classmethod
    def sanitize_input(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize input data"""
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = re.sub(r'[^\w\s\-.,]', '', value)
            else:
                sanitized[key] = value
        return sanitized
        
    @classmethod
    def validate_file_path(cls, file_path: str) -> bool:
        """Validate file path security"""
        try:
            path = Path(file_path)
            return path.exists() and path.is_file()
        except Exception:
            return False
