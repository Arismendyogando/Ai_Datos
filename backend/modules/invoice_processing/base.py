from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
from .utils.logger import setup_logger
from .validations import FileValidator

logger = setup_logger()

class DocumentProcessor(ABC):
    """Base class for document processing"""
    
    @abstractmethod
    async def process(self, file_path: str) -> Dict[str, Any]:
        """Process a document and return extracted data"""
        pass

class InvoiceParserBase(DocumentProcessor):
    """Base class for invoice parsing functionality"""
    
    def __init__(self):
        self._setup_environment()
        self.validator = FileValidator()
        
    def _setup_environment(self):
        """
        Setup the environment for invoice processing. 
        This can include loading configurations, initializing resources, etc.
        """
        pass
        
    async def process(self, file_path: str) -> Dict[str, Any]:
        """Process invoice file and return structured data"""
        if not self.validator.validate_file_path(file_path):
            raise ValueError(f"Invalid file path: {file_path}")
            
        if not self.validator.validate_mime_type(file_path):
            raise ValueError("Unsupported file type")
            
        try:
            data = await self._process_file(file_path)
            return self.validator.sanitize_input(data)
        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            raise
            
    @abstractmethod
    async def _process_file(self, file_path: str) -> Dict[str, Any]:
        """Internal method for file processing"""
        pass
        
    def validate_invoice_data(self, data: Dict[str, Any]) -> bool:
        """Validate extracted invoice data"""
        required_fields = [
            'invoice_number',
            'date',
            'total_amount',
            'vendor_name'
        ]
        return all(data.get(field) is not None for field in required_fields)
