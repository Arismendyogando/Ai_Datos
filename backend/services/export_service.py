from typing import Dict
import pandas as pd
from datetime import datetime

class ExportService:
    @staticmethod
    async def export_excel(data: Dict):
        df = pd.DataFrame(data)
        file_path = f"exports/export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(file_path)
        return file_path

    @staticmethod
    async def export_sheets(data: Dict):
        # Implementación de exportación a Google Sheets
        pass
