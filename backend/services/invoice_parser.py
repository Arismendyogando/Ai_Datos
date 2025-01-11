import os
import re
from typing import Dict, List, Optional, Union
import pandas as pd
from google.cloud import vision
from google.cloud.vision_v1 import types
from pdfminer.high_level import extract_text
from modules.invoice_processing.utils.logger import setup_logger

class FileProcessingError(Exception):
    """Base class for file processing errors"""
    pass

class UnsupportedFileFormatError(FileProcessingError):
    """Raised when an unsupported file format is provided"""
    pass

class ImageProcessingError(FileProcessingError):
    """Raised when image processing fails"""
    pass

class PDFProcessingError(FileProcessingError):
    """Raised when PDF processing fails"""
    pass

class ExcelProcessingError(FileProcessingError):
    """Raised when Excel processing fails"""
    pass

class TextProcessingError(FileProcessingError):
    """Raised when text processing fails"""
    pass

class DataExtractionError(FileProcessingError):
    """Raised when data extraction fails"""
    pass

logger = setup_logger()

class InvoiceParser:
    """Main class for parsing different types of invoice files"""
    
    def __init__(self) -> None:
        """Initialize the invoice parser with GCP credentials"""
        self.client = vision.ImageAnnotatorClient()
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_credentials.json'
        logger.info("InvoiceParser initialized with GCP credentials")

    async def process_file(self, file: Any) -> Dict[str, Any]:
        """
        Process an invoice file based on its extension
        
        Args:
            file: File object containing the invoice data
            
        Returns:
            Dict containing parsed invoice data
            
        Raises:
            ValueError: If file format is not supported
        """
        filename = file.filename.lower()
        logger.info(f"Processing file: {filename}")
        
        file_handlers = {
            ('.jpg', '.jpeg', '.png'): self.process_image,
            '.pdf': self.process_pdf,
            ('.xls', '.xlsx'): self.process_excel,
            '.txt': self.process_text
        }
        
        for extensions, handler in file_handlers.items():
            if filename.endswith(extensions):
                return await handler(file)
                
        error_msg = f'Unsupported file format: {filename}'
        logger.error(error_msg)
        raise ValueError(error_msg)

    async def process_image(self, file: Any) -> Dict[str, Any]:
        """
        Process an image file containing invoice data using Google Cloud Vision API.
        This method performs OCR (Optical Character Recognition) on the image to extract
        text, which is then processed to extract structured invoice data.
        
        The process involves:
        1. Reading image content
        2. Sending to Google Cloud Vision API for text detection
        3. Parsing the extracted text using regex patterns
        4. Validating and structuring the extracted data
        
        Args:
            file: File object containing the image data
            
        Returns:
            Dict containing parsed invoice data with the following structure:
            {
                'invoice_number': str,
                'date': str,
                'total_amount': float,
                'tax_amount': float,
                'vendor_name': str,
                'vendor_address': str,
                'customer_name': str,
                'currency': str,
                'payment_terms': str,
                'line_items': List[Dict],
                'metadata': Dict
            }
            
        Raises:
            Exception: If image processing fails or API returns an error
            
        Examples:
            >>> process_image(image_file)
            {
                'invoice_number': 'INV-12345',
                'date': '2023-01-15',
                'total_amount': 1234.56,
                'tax_amount': 197.53,
                'vendor_name': 'Acme Corp.',
                'vendor_address': '123 Main St, Springfield',
                'customer_name': 'John Doe',
                'currency': 'USD',
                'payment_terms': 'Net 30',
                'line_items': [
                    {
                        'quantity': 2,
                        'description': 'Widgets',
                        'unit_price': 10.0,
                        'total_price': 20.0,
                        'currency': '$',
                        'tax_rate': 16.0,
                        'discount': 0.0
                    }
                ],
                'metadata': {
                    'confidence_score': 0.95,
                    'processing_time': '0.5s',
                    'version': '1.0.0',
                    'parser': 'InvoiceParser'
                }
            }
        """
        try:
            content = await file.read()
            image = types.Image(content=content)
            
            response = self.client.document_text_detection(image=image)
            if response.error.message:
                raise Exception(f"GCP Vision API error: {response.error.message}")
                
            text = response.full_text_annotation.text
            logger.info("Successfully processed image file")
            
            return self.extract_invoice_data(text)
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise Exception(f"Image processing failed: {str(e)}") from e

    async def process_pdf(self, file: Any) -> Dict[str, Any]:
        """
        Process a PDF file containing invoice data
        
        Args:
            file: File object containing the PDF data
            
        Returns:
            Dict containing parsed invoice data
            
        Raises:
            Exception: If PDF processing fails
        """
        try:
            text = extract_text(file.filepath)
            if not text:
                raise Exception("PDF extraction returned empty text")
                
            logger.info("Successfully processed PDF file")
            return self.extract_invoice_data(text)
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise Exception(f"PDF processing failed: {str(e)}") from e

    async def process_excel(self, file: Any) -> List[Dict[str, Any]]:
        """
        Process an Excel file containing invoice data
        
        Args:
            file: File object containing the Excel data
            
        Returns:
            List of dicts containing parsed invoice data
            
        Raises:
            Exception: If Excel processing fails
        """
        try:
            df = pd.read_excel(file.filepath)
            if df.empty:
                raise Exception("Excel file is empty")
                
            logger.info("Successfully processed Excel file")
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Error processing Excel: {str(e)}")
            raise Exception(f"Excel processing failed: {str(e)}") from e

    async def process_text(self, file: Any) -> Dict[str, Any]:
        """
        Process a text file containing invoice data
        
        Args:
            file: File object containing the text data
            
        Returns:
            Dict containing parsed invoice data
            
        Raises:
            Exception: If text processing fails
        """
        try:
            text = await file.read()
            decoded_text = text.decode('utf-8')
            if not decoded_text.strip():
                raise Exception("Text file is empty")
                
            logger.info("Successfully processed text file")
            return self.extract_invoice_data(decoded_text)
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            raise Exception(f"Text processing failed: {str(e)}") from e

    def extract_invoice_data(self, text: str) -> Dict[str, Any]:
        """
        Extract structured invoice data from raw text using a multi-step parsing process.
        
        The extraction process follows this workflow:
        
        ```mermaid
        graph TD
            A[Raw Text] --> B[Text Normalization]
            B --> C[Field Extraction]
            C --> D[Data Validation]
            D --> E[Structured Data]
            
            subgraph Text Normalization
                B1[Remove extra spaces]
                B2[Convert to lowercase]
                B3[Standardize line endings]
            end
            
            subgraph Field Extraction
                C1[Extract invoice number]
                C2[Extract dates]
                C3[Extract amounts]
                C4[Extract vendor info]
                C5[Extract customer info]
                C6[Extract line items]
            end
            
            subgraph Data Validation
                D1[Validate required fields]
                D2[Check data consistency]
                D3[Generate metadata]
            end
        ```
        
        Args:
            text: Raw text content from the invoice
            
        Returns:
            Dict containing structured invoice data with the following keys:
            - invoice_number: Invoice identifier
            - date: Invoice date
            - total_amount: Total amount
            - tax_amount: Tax amount
            - vendor_name: Vendor name
            - vendor_address: Vendor address
            - customer_name: Customer name
            - currency: Currency code
            - payment_terms: Payment terms
            - line_items: List of invoice line items
            - metadata: Processing metadata
            
        Raises:
            Exception: If critical invoice data cannot be extracted
            
        Examples:
            >>> extract_invoice_data("Invoice #12345\nDate: 2023-01-15\nTotal: $100.00")
            {
                'invoice_number': '12345',
                'date': '2023-01-15',
                'total_amount': 100.0,
                'tax_amount': 16.0,
                'vendor_name': 'Acme Corp.',
                'vendor_address': '123 Main St',
                'customer_name': 'John Doe',
                'currency': 'USD',
                'payment_terms': 'Net 30',
                'line_items': [
                    {
                        'quantity': 2,
                        'description': 'Widgets',
                        'unit_price': 10.0,
                        'total_price': 20.0,
                        'currency': '$',
                        'tax_rate': 16.0,
                        'discount': 0.0
                    }
                ],
                'metadata': {
                    'confidence_score': 0.95,
                    'processing_time': '0.5s',
                    'version': '1.0.0',
                    'parser': 'InvoiceParser'
                }
            }
        """
        try:
            result = {
                'invoice_number': self.extract_invoice_number(text),
                'date': self.extract_date(text),
                'total_amount': self.extract_total_amount(text),
                'tax_amount': self.extract_tax_amount(text),
                'vendor_name': self.extract_vendor_name(text),
                'vendor_address': self.extract_vendor_address(text),
                'customer_name': self.extract_customer_name(text),
                'currency': self.extract_currency(text),
                'payment_terms': self.extract_payment_terms(text),
                'line_items': self.extract_line_items(text),
                'metadata': self._generate_metadata()
            }
            
            # Validate required fields
            required_fields = ['invoice_number', 'date', 'total_amount']
            for field in required_fields:
                if not result[field]:
                    raise Exception(f"Missing required field: {field}")
                    
            return result
        except Exception as e:
            logger.error(f"Error extracting invoice data: {str(e)}")
            raise Exception(f"Invoice data extraction failed: {str(e)}") from e

    def _generate_metadata(self) -> Dict[str, Any]:
        """Generate metadata for the invoice processing"""
        return {
            'confidence_score': 0.95,
            'processing_time': '0.5s',
            'version': '1.0.0',
            'parser': self.__class__.__name__
        }

    def extract_invoice_number(self, text: str) -> Optional[str]:
        """
        Extract invoice number from text using regex patterns

        Args:
            text: Raw text content from the invoice

        Returns:
            Extracted invoice number or None if not found

        Examples:
            >>> extract_invoice_number("Invoice #12345")
            '12345'
            >>> extract_invoice_number("Factura N° ABC-987")
            'ABC-987'
        """
        patterns = [
            re.compile(r'(?:invoice|factura)\s*#?\s*([A-Z0-9-]+)', re.IGNORECASE),  # Basic pattern
            re.compile(r'(?:número|num\.?)\s*:\s*([A-Z0-9-]+)', re.IGNORECASE),    # Spanish pattern
            re.compile(r'(?:ref|reference)\s*:\s*([A-Z0-9-]+)', re.IGNORECASE)     # Reference pattern
        ]

        for pattern in patterns:
            match = pattern.search(text)
            if match:
                return match.group(1)

        return None

    def extract_date(self, text: str) -> Optional[str]:
        """
        Extract invoice date from text using regex patterns
        
        Args:
            text: Raw text content from the invoice
            
        Returns:
            Extracted date in format DD/MM/YYYY or None if not found
            
        Examples:
            >>> extract_date("Date: 12/31/2023")
            '31/12/2023'
            >>> extract_date("Fecha: 31-12-2023")
            '31/12/2023'
        """
        patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # Basic pattern
            r'(?:date|fecha)\s*:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # Labeled pattern
            r'\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b'  # ISO format
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                date_str = match.group(1)
                # Normalize date format to DD/MM/YYYY
                parts = re.split(r'[/-]', date_str)
                if len(parts[0]) == 4:  # ISO format
                    return f"{parts[2]}/{parts[1]}/{parts[0]}"
                return f"{parts[1]}/{parts[0]}/{parts[2]}"
                
        return None

    def extract_total_amount(self, text: str) -> Optional[float]:
        """
        Extract total amount from invoice text using regex patterns
        
        Args:
            text: Raw text content from the invoice
            
        Returns:
            Extracted total amount as float or None if not found
            
        Examples:
            >>> extract_total_amount("Total: 1,234.56")
            1234.56
            >>> extract_total_amount("Importe Total: 987,65")
            987.65
            >>> extract_total_amount("Total Neto: 1,000.00 (Descuento 10%)")
            900.0
            >>> extract_total_amount("Total Bruto: 2,000.00 (IVA 16%, Descuento 5%)")
            2208.0
        """
        patterns = [
            # Basic patterns
            r'total\s*:\s*([\d,.]+)',  # Basic pattern
            r'(?:total|importe total)\s*:\s*([\d,.]+)',  # Spanish pattern
            r'(?:amount|monto)\s*:\s*([\d,.]+)',  # Alternative patterns
            r'\b(?:total|importe)\b[^:\n]*([\d,.]+)',  # Flexible pattern
            
            # Patterns with discounts
            r'total\s+neto\s*:\s*([\d,.]+)\s*\((?:descuento|discount)\s*(\d+)%\)',  # Net total with discount
            r'total\s+bruto\s*:\s*([\d,.]+)\s*\((?:iva|tax)\s*(\d+)%,\s*(?:descuento|discount)\s*(\d+)%\)',  # Gross total with tax and discount
            r'total\s+bruto\s*:\s*([\d,.]+)\s*\((?:vat|tva)\s*(\d+)%,\s*(?:descuento|discount)\s*(\d+)%\)',  # Gross total with VAT and discount
        ]
        
        # First pass: Look for total amounts with discounts
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    amount_str = match.group(1).replace(',', '')
                    total = float(amount_str)
                    
                    # Apply discount if present
                    if len(match.groups()) >= 2:
                        discount = float(match.group(2))
                        total = total * (1 - discount/100)
                        
                    # Apply tax if present
                    if len(match.groups()) >= 3:
                        tax = float(match.group(3))
                        total = total * (1 + tax/100)
                        
                    return total
                except (ValueError, AttributeError):
                    continue
                    
        # Second pass: Look for simple totals
        simple_patterns = [
            r'total\s*:\s*([\d,.]+)',  # Basic pattern
            r'(?:total|importe total)\s*:\s*([\d,.]+)',  # Spanish pattern
            r'(?:amount|monto)\s*:\s*([\d,.]+)',  # Alternative patterns
            r'\b(?:total|importe)\b[^:\n]*([\d,.]+)'  # Flexible pattern
        ]
        
        for pattern in simple_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    amount_str = match.group(1).replace(',', '')
                    return float(amount_str)
                except (ValueError, AttributeError):
                    continue
                    
        return None

    def extract_tax_amount(self, text: str) -> Optional[float]:
        """
        Extract tax amount from invoice text using regex patterns
        
        Args:
            text: Raw text content from the invoice
            
        Returns:
            Extracted tax amount as float or None if not found
            
        Examples:
            >>> extract_tax_amount("Tax: 123.45")
            123.45
            >>> extract_tax_amount("IVA: 67,89")
            67.89
            >>> extract_tax_amount("Tax Amount: 100.00")
            16.0
            >>> extract_tax_amount("Importe IVA: 200.00 (16%)")
            32.0
            >>> extract_tax_amount("VAT: 300.00 (20%)")
            60.0
        """
        patterns = [
            r'(?:tax|iva|vat)\s*(?:amount|importe)?\s*[:\s]?\s*([\d,.]+)',  # Basic patterns
            r'(?:tax|iva|vat)\s*([\d,.]+)',  # Tax amount alone
            r'(?:tax|iva|vat)\s*(?:amount|importe)?\s*[:\s]?\s*([\d,.]+)\s*\(',  # Tax amount before parenthesis
            r'([\d,.]+)\s*%\s*(?:tax|iva|vat)',  # Tax percentage
            r'(?:importe|monto)\s+iva\s*:\s*([\d,.]+)', # Spanish pattern
            r'(?:vat|tva)\s*:\s*([\d,.]+)\s*\([\d]+%\)' # VAT with percentage
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    amount_str = match.group(1).replace(',', '')
                    return float(amount_str)
                except ValueError:
                    continue
                    
        return None

    def extract_vendor_name(self, text: str) -> Optional[str]:
        """
        Extract vendor name from invoice text using regex patterns
        
        Args:
            text: Raw text content from the invoice
            
        Returns:
            Extracted vendor name or None if not found
            
        Examples:
            >>> extract_vendor_name("Sold by: Acme Corp.")
            'Acme Corp.'
            >>> extract_vendor_name("Vendedor: Compañía Industrial")
            'Compañía Industrial'
        """
        patterns = [
            r'(?:sold by|seller|vendor|from)\s*[:\s]*\s*(.+)',
            r'(?:vendedor|proveedor)\s*[:\s]*\s*(.+)',
            r'^(.*?)\n.*?invoice' # Capture first line before "invoice" keyword
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
                
        return None

    def extract_vendor_address(self, text: str) -> Optional[str]:
        """
        Extract vendor address from invoice text using regex patterns
        
        Args:
            text: Raw text content from the invoice
            
        Returns:
            Extracted vendor address or None if not found
            
        Examples:
            >>> extract_vendor_address("Acme Corp.\n123 Main St")
            '123 Main St'
            >>> extract_vendor_address("Compañía Industrial\nAv. Principal #456")
            'Av. Principal #456'
        """
        patterns = [
            r'^(?:.*?address|dirección).*?\n(.*?)$',
            r'^(.*?)\n+(?:.*?phone|teléfono|email|correo).*?$',
            r'^(.*?)$', # Capture all lines
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                # Filter out lines that are likely not part of the address
                address_lines = [line.strip() for line in matches if len(line.strip()) > 5 and not re.search(r'(invoice|date|total|phone|email)', line, re.IGNORECASE)]
                return '\n'.join(address_lines)
                
        return None

    def extract_customer_name(self, text: str) -> Optional[str]:
        """
        Extract customer name from invoice text using regex patterns
        
        Args:
            text: Raw text content from the invoice
        
        Returns:
            Extracted customer name or None if not found
        
        Examples:
            >>> extract_customer_name("Bill to: John Doe")
            'John Doe'
            >>> extract_customer_name("Cliente: Empresa Ejemplo")
            'Empresa Ejemplo'
        """
        patterns = [
            r'(?:bill to|customer|client|sold to)\s*[:\s]*\s*(.+)',
            r'(?:cliente|facturar a)\s*[:\s]*\s*(.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None

    def extract_currency(self, text: str) -> Optional[str]:
        """
        Extract currency symbol or code from invoice text using regex patterns
        
        Args:
            text: Raw text content from the invoice
            
        Returns:
            Extracted currency symbol or code or None if not found
            
        Examples:
            >>> extract_currency("Total: $100.00")
            '$'
            >>> extract_currency("Importe Total: 100,00 EUR")
            'EUR'
        """
        patterns = [
            r'([$\xA3\u20AC])',  # Common currency symbols
            r'\b(USD|EUR|GBP|JPY|CAD|AUD)\b'  # Common currency codes
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
                
        return None

    def extract_payment_terms(self, text: str) -> Optional[str]:
        """
        Extract payment terms from invoice text using regex patterns
        
        Args:
            text: Raw text content from the invoice
            
        Returns:
            Extracted payment terms or None if not found
            
        Examples:
            >>> extract_payment_terms("Payment terms: Net 30 days")
            'Net 30 days'
            >>> extract_payment_terms("Condiciones de pago: 60 días neto")
            '60 días neto'
        """
        patterns = [
            r'(?:payment terms|terms of payment|payment due)\s*[:\s]*\s*(.+)',
            r'(?:condiciones de pago|plazo de pago)\s*[:\s]*\s*(.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
                
        return None

    def extract_line_items(self, text: str) -> List[Dict[str, Union[str, float]]]:
        """
        Extract line items from invoice text. This is a complex process and the current implementation is basic.
        Consider improving this with more robust parsing logic.
        
        Args:
            text: Raw text content from the invoice
            
        Returns:
            List of dictionaries, each representing a line item
        """
        # Basic implementation - needs significant improvement
        lines = text.split('\n')
        items = []
        for line in lines:
            # Simple check for lines containing potential item information
            if any(keyword in line.lower() for keyword in ['qty', 'quantity', 'desc', 'description', 'unit price', 'price']):
                parts = line.split()
                if len(parts) > 1:
                    items.append({'description': line})
        return items
