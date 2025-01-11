import pandas as pd
from typing import Dict, Any
from ..base import InvoiceParserBase
from ..utils.logger import setup_logger

logger = setup_logger()

class ExcelParser(InvoiceParserBase):
    """Parser implementation for Excel files"""

    def __init__(self, extraction_option: str = "auto", delimiter: str = None, template: str = None):
        super().__init__()
        self.extraction_option = extraction_option
        self.delimiter = delimiter
        self.template = template

    async def _process_file(self, file_path: str) -> Dict[str, Any]:
        """Process Excel file and extract invoice data"""
        logger.info(f"Processing Excel file: {file_path}, extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
        try:
            df = pd.read_excel(file_path)
            text = df.to_string()
            data = self.extract_invoice_data(text)
            return data
        except Exception as e:
            logger.error(f"Error processing Excel file: {str(e)}")
            raise

    def extract_invoice_data(self, text: str) -> Dict[str, Any]:
        """Extract invoice data from text"""
        logger.debug(f"Extracting data from Excel text with extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
        try:
            if self.extraction_option == "template":
                # If the extraction option is set to "template", this branch will handle template-based extraction.
                # Currently, template-based extraction is not implemented.
                return {"message": "Template-based extraction not implemented yet"}
            elif self.delimiter:
                # If a delimiter is specified, the code attempts to split the text based on this delimiter.
                # This approach assumes that the invoice data fields are separated by the provided delimiter.
                lines = text.split(self.delimiter)
                return {
                    "invoice_number": lines[0].strip(),
                    "date": lines[1].strip(),
                    "total_amount": float(lines[2].strip().replace("$", "")),
                    "vendor_name": lines[3].strip(),
                }
            else:
                # If no specific extraction option or delimiter is provided, the code attempts to extract data
                # based on predefined column names. It uses pandas' `get` method to retrieve data from
                # columns named "Invoice Number", "Date", "Total Amount", and "Vendor Name". The `[None]`
                # argument provides a default value if the column is not found.
                invoice_number = df.get("Invoice Number", [None])[0]
                date = df.get("Date", [None])[0]
                total_amount = df.get("Total Amount", [None])[0]
                vendor_name = df.get("Vendor Name", [None])[0]
                return {
                    "invoice_number": invoice_number,
                    "date": date,
                    "total_amount": total_amount,
                    "vendor_name": vendor_name,
                }
        except Exception as e:
            logger.error(f"Data extraction error: {str(e)}")
            raise
addPreferredDiff: true
import pandas as pd
from typing import Dict, Any
from ..base import InvoiceParserBase
from ..utils.logger import setup_logger

logger = setup_logger()

class ExcelParser(InvoiceParserBase):
    """Parser implementation for Excel files"""

    def __init__(self, extraction_option: str = "auto", delimiter: str = None, template: str = None):
        super().__init__()
        self.extraction_option = extraction_option
        self.delimiter = delimiter
        self.template = template

    async def _process_file(self, file_path: str) -> Dict[str, Any]:
        """Process Excel file and extract invoice data"""
        logger.info(f"Processing Excel file: {file_path}, extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
        try:
            df = pd.read_excel(file_path)
            text = df.to_string()
            data = self.extract_invoice_data(text)
            return data
        except Exception as e:
            logger.error(f"Error processing Excel file: {str(e)}")
            raise

    def extract_invoice_data(self, text: str) -> Dict[str, Any]:
        """Extract invoice data from text"""
        logger.debug(f"Extracting data from Excel text with extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
        try:
            if self.extraction_option == "template":
                return {"message": "Template-based extraction not implemented yet"}
            elif self.delimiter:
                # This is a simplistic approach and might need more robust handling
                lines = text.split(self.delimiter)
                return {
                    "invoice_number": lines[0].strip(),
                    "date": lines[1].strip(),
                    "total_amount": float(lines[2].strip().replace("$", "")),
                    "vendor_name": lines[3].strip(),
                }
            else:
                # Basic parsing logic based on column names (example)
                invoice_number = df.get("Invoice Number", [None])[0]
                date = df.get("Date", [None])[0]
                total_amount = df.get("Total Amount", [None])[0]
                vendor_name = df.get("Vendor Name", [None])[0]
                return {
                    "invoice_number": invoice_number,
                    "date": date,
                    "total_amount": total_amount,
                    "vendor_name": vendor_name,
                }
        except Exception as e:
            logger.error(f"Data extraction error: {str(e)}")
            raise
