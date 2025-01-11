from .parsers.image_parser import ImageParser
from .parsers.pdf_parser import PDFParser
from .parsers.excel_parser import ExcelParser
from ..base import DocumentProcessor
from typing import Dict, Any
import mimetypes

class ParserFactory:
    """Factory class for creating appropriate parsers based on file type"""

    @staticmethod
    def create_parser(file_path: str, extraction_option: str = "auto", delimiter: str = None, template: str = None) -> DocumentProcessor:
        """Create and return appropriate parser based on file type"""
        mime_type, _ = mimetypes.guess_type(file_path)

        if mime_type is None:
            raise ValueError("Could not determine file type")

        if mime_type.startswith('image/'):
            return ImageParser(extraction_option=extraction_option, delimiter=delimiter, template=template)
        elif mime_type == 'application/pdf':
            return PDFParser(extraction_option=extraction_option, delimiter=delimiter, template=template)
        elif mime_type in ['application/vnd.ms-excel',
                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            return ExcelParser(extraction_option=extraction_option, delimiter=delimiter, template=template)
        else:
            raise ValueError(f"Unsupported file type: {mime_type}")
