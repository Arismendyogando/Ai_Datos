from typing import Dict, Any, Optional
from google.cloud import vision
from google.cloud.vision import types
from ..base import InvoiceParserBase
from ..utils.logger import setup_logger
import hashlib
import json
import os

logger = setup_logger()

class ImageParser(InvoiceParserBase):
    """Parser implementation for image files (JPG, PNG)"""

    CACHE_DIR = ".ocr_cache"

    def __init__(self, extraction_option: str = "auto", delimiter: str = None, template: str = None):
        super().__init__()
        self.client = vision.ImageAnnotatorClient()
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        self.extraction_option = extraction_option
        self.delimiter = delimiter
        self.template = template

    async def _process_file(self, file_path: str) -> Dict[str, Any]:
        """Process image file and extract invoice data"""
        logger.info(f"Processing image file: {file_path}, extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
        try:
            cache_key = self._get_cache_key(file_path)
            cached_data = self._get_cached_result(cache_key)

            if cached_data:
                logger.debug("Using cached OCR result")
                return cached_data

            with open(file_path, "rb") as image_file:
                content = image_file.read()
                image = types.Image(content=content)

                response = self.client.document_text_detection(image=image)
                text = response.full_text_annotation.text
                data = self.extract_invoice_data(text)

                self._cache_result(cache_key, data)
                return data
        except Exception as e:
            logger.error(f"Error processing image file: {str(e)}")
            raise

    def _get_cache_key(self, file_path: str) -> str:
        """Generate cache key from file content"""
        with open(file_path, "rb") as f:
            # Generate a cache key by creating an MD5 hash of the file's content.
            return hashlib.md5(f.read()).hexdigest()

    def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached OCR result if exists"""
        cache_file = os.path.join(self.CACHE_DIR, f"{cache_key}.json")
        # Check if a cached result exists for the given cache key.
        if os.path.exists(cache_file):
            # If the cache file exists, load and return the cached data.
            with open(cache_file, "r") as f:
                return json.load(f)
        return None

    def _cache_result(self, cache_key: str, data: Dict[str, Any]) -> None:
        """Cache OCR result"""
        cache_file = os.path.join(self.CACHE_DIR, f"{cache_key}.json")
        # Cache the OCR result by saving it to a JSON file.
        with open(cache_file, "w") as f:
            json.dump(data, f)

    def extract_invoice_data(self, text: str) -> Dict[str, Any]:
        """Extract invoice data from text"""
        logger.debug(f"Extracting data from image text with extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
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
from typing import Dict, Any, Optional
from google.cloud import vision
from google.cloud.vision import types
from ..base import InvoiceParserBase
from ..utils.logger import setup_logger
import hashlib
import json
import os

logger = setup_logger()

class ImageParser(InvoiceParserBase):
    """Parser implementation for image files (JPG, PNG)"""

    CACHE_DIR = ".ocr_cache"

    def __init__(self, extraction_option: str = "auto", delimiter: str = None, template: str = None):
        super().__init__()
        self.client = vision.ImageAnnotatorClient()
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        self.extraction_option = extraction_option
        self.delimiter = delimiter
        self.template = template

    async def _process_file(self, file_path: str) -> Dict[str, Any]:
        """Process image file and extract invoice data"""
        logger.info(f"Processing image file: {file_path}, extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
        try:
            cache_key = self._get_cache_key(file_path)
            cached_data = self._get_cached_result(cache_key)

            if cached_data:
                logger.debug("Using cached OCR result")
                return cached_data

            with open(file_path, "rb") as image_file:
                content = image_file.read()
                image = types.Image(content=content)

                response = self.client.document_text_detection(image=image)
                text = response.full_text_annotation.text
                data = self.extract_invoice_data(text)

                self._cache_result(cache_key, data)
                return data
        except Exception as e:
            logger.error(f"Error processing image file: {str(e)}")
            raise

    def _get_cache_key(self, file_path: str) -> str:
        """Generate cache key from file content"""
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached OCR result if exists"""
        cache_file = os.path.join(self.CACHE_DIR, f"{cache_key}.json")
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                return json.load(f)
        return None

    def _cache_result(self, cache_key: str, data: Dict[str, Any]) -> None:
        """Cache OCR result"""
        cache_file = os.path.join(self.CACHE_DIR, f"{cache_key}.json")
        with open(cache_file, "w") as f:
            json.dump(data, f)

    def extract_invoice_data(self, text: str) -> Dict[str, Any]:
        """Extract invoice data from text"""
        logger.debug(f"Extracting data from image text with extraction_option: {self.extraction_option}, delimiter: {self.delimiter}, template: {self.template}")
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
