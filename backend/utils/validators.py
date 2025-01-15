from typing import Dict
from pydantic import ValidationError

class DataValidator:
    @staticmethod
    def validate_export_data(data: Dict):
        if not data:
            raise ValidationError("No hay datos para exportar")
        if not isinstance(data, dict):
            raise ValidationError("Formato de datos inválido")
        return data
