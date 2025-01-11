from typing import Dict, Any
from pdfminer.high_level import extract_text
from ..base import InvoiceParserBase
from ..utils.logger import setup_logger

logger = setup_logger()

class PDFParser(InvoiceParserBase):
    """Parser implementation for PDF files"""

    def __init__(self, extraction_option: str = "auto", delimiter: str = None, template: str = None):
        super().__init__()
        self.extraction_option = extraction_option
        self.delimiter = delimiter
        self.template = template

    async def _process_file(self, file_path: str) -> Dict[str, Any]:
        """Process PDF file and extract invoice data"""
        logger.info(f"Processing PDF file: {file_path}, extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
        try:
            text = extract_text(file_path)
            data = self.extract_invoice_data(text)
            return data
        except Exception as e:
            logger.error(f"Error processing PDF file: {str(e)}")
            raise

    def extract_invoice_data(self, text: str) -> Dict[str, Any]:
        """Extract invoice data from text"""
        logger.debug(f"Extracting data from PDF text with extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
        try:
            if self.extraction_option == "template":
                # If the extraction option is 'template', use a template-based extraction logic.
                # This is a placeholder and needs actual implementation.
                return {"message": "Template-based extraction not implemented yet"}
            elif self.delimiter:
                # If a delimiter is provided, split the text based on the delimiter.
                # This assumes a specific order of data fields separated by the delimiter.
                lines = text.split(self.delimiter)
                return {
                    "invoice_number": lines[0].strip(),
                    "date": lines[1].strip(),
                    "total_amount": float(lines[2].strip().replace("$", "")),
                    "vendor_name": lines[3].strip(),
                }
            else:
                # If no specific extraction option or delimiter is provided, perform basic parsing.
                # This assumes a newline-separated structure for basic invoice data.
                lines = text.split("\n")
                return {
                    "invoice_number": lines[0].strip(),
                    "date": lines[1].strip(),
                    "total_amount": float(lines[2].strip().replace("$", "")),
                    "vendor_name": lines[3].strip(),
                }
        except Exception as e:
            logger.error(f"Data extraction error: {str(e)}")
            raise
addPreferredDiff: true
from typing import Dict, Any
from pdfminer.high_level import extract_text
from ..base import InvoiceParserBase
from ..utils.logger import setup_logger

logger = setup_logger()

class PDFParser(InvoiceParserBase):
    """Parser implementation for PDF files"""

    def __init__(self, extraction_option: str = "auto", delimiter: str = None, template: str = None):
        super().__init__()
        self.extraction_option = extraction_option
        self.delimiter = delimiter
        self.template = template

    async def _process_file(self, file_path: str) -> Dict[str, Any]:
        """Process PDF file and extract invoice data"""
        logger.info(f"Processing PDF file: {file_path}, extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
        try:
            text = extract_text(file_path)
            data = self.extract_invoice_data(text)
            return data
        except Exception as e:
            logger.error(f"Error processing PDF file: {str(e)}")
            raise

    def extract_invoice_data(self, text: str) -> Dict[str, Any]:
        """Extract invoice data from text"""
        logger.debug(f"Extracting data from PDF text with extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
        try:
            if self.extraction_option == "template":
                # Implement template-based extraction logic here
                return {"message": "Template-based extraction not implemented yet"}
            elif self.delimiter:
                # Implement delimiter-based extraction logic here
                lines = text.split(self.delimiter)
                return {
                    "invoice_number": lines[0].strip(),
                    "date": lines[1].strip(),
                    "total_amount": float(lines[2].strip().replace("$", "")),
                    "vendor_name": lines[3].strip(),
                }
            else:
                # Basic parsing logic
                lines = text.split("\n")
                return {
                    "invoice_number": lines[0].strip(),
                    "date": lines[1].strip(),
                    "total_amount": float(lines[2].strip().replace("$", "")),
                    "vendor_name": lines[3].strip(),
                }
        except Exception as e:
            logger.error(f"Data extraction error: {str(e)}")
            raise
