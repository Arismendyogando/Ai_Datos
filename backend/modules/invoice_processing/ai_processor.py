from typing import Dict
from .parsers import ExcelParser, PDFParser, ImageParser  # Import the parsers

class DocumentProcessor:
    async def extract_data(self, file_path: str, document_type: str) -> Dict:
        if document_type == "excel":
            return await ExcelParser.parse(file_path)
        elif document_type == "pdf":
            return await PDFParser.parse(file_path)
        elif document_type == "image":
            return await ImageParser.parse(file_path)
        else:
            raise ValueError(f"Unsupported document type: {document_type}")

    async def apply_template(self, data: Dict, template_id: str) -> Dict:
        # Aquí la lógica para aplicar plantillas a los datos extraídos
        # Esto podría implicar transformar o enriquecer los datos
        return data
