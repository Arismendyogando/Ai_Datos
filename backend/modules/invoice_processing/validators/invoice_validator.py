from typing import Dict, Any
import re
from datetime import datetime
from ..base import InvoiceParserBase
import logging
import magic
from io import BytesIO
from html import escape

logger = logging.getLogger(__name__)

class InvoiceValidator:
    """Class for validating invoice data with enhanced security"""
    
    ALLOWED_MIME_TYPES = {
        'application/pdf',
        'image/jpeg',
        'image/png',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    def __init__(self):
        self.mime = magic.Magic(mime=True)
    
    def validate_invoice_number(self, invoice_number: str) -> bool:
        """Validate and sanitize invoice number format"""
        if not invoice_number:
            return False
            
        # Sanitize input
        invoice_number = escape(invoice_number.strip())
        
        # Validate format
        return bool(re.match(r'^[A-Z]{2}-\d{4}-\d{6}$', invoice_number))
        
    def validate_date(self, date_str: str) -> bool:
        """Validate and sanitize date format (YYYY-MM-DD)"""
        try:
            # Sanitize input
            date_str = escape(date_str.strip())
            
            # Validate format
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
            
    def validate_amount(self, amount: str) -> bool:
        """Validate and sanitize amount format"""
        try:
            # Sanitize input
            amount = escape(amount.strip())
            
            # Validate format
            float(amount)
            return True
        except ValueError:
            return False
            
    def validate_vendor_name(self, vendor_name: str) -> bool:
        """Validate and sanitize vendor name format"""
        if not vendor_name:
            return False
            
        # Sanitize input
        vendor_name = escape(vendor_name.strip())
        
        # Validate length and content
        return len(vendor_name) > 2 and bool(re.match(r'^[a-zA-Z0-9\s\-\.]+$', vendor_name))
        
    def validate_file(self, file_data: bytes) -> bool:
        """Validate uploaded file type and content"""
        if len(file_data) > self.MAX_FILE_SIZE:
            return False
            
        # Verify MIME type
        mime_type = self.mime.from_buffer(file_data)
        if mime_type not in self.ALLOWED_MIME_TYPES:
            return False
            
        return True
        
    def validate_all(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all invoice fields with enhanced security and return validation results"""
        return {
            'invoice_number': self.validate_invoice_number(data.get('invoice_number')),
            'date': self.validate_date(data.get('date')),
            'total_amount': self.validate_amount(data.get('total_amount')),
            'vendor_name': self.validate_vendor_name(data.get('vendor_name')),
            'file_valid': self.validate_file(data.get('file_data', b'')) if 'file_data' in data else True
        }
