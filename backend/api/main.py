from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import os
import logging
from pathlib import Path
from datetime import datetime

from backend.config import config
from backend.services.invoice_parser import InvoiceParser
from backend.services.ai_service import AIService
from api import export
from api import documents

# Configuración del logging
logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Extracción de Datos de Facturas",
    description="API para extraer datos estructurados de facturas utilizando Gemini AI",
    version="1.0.0"
)

# Configuración de CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización de servicios
invoice_parser = InvoiceParser()
ai_service = AIService()

app.include_router(export.router)
app.include_router(documents.router)

@app.post("/ai/analyze/{document_id}")
async def analyze_document(document_id: str):
    """
    Analiza un documento utilizando el servicio de IA.
    """
    return ai_service.analyze_document(document_id)

@app.post("/ai/query")
async def process_query(query: Dict[str, Any], context: Dict[str, Any]):
    """
    Procesa una consulta utilizando el servicio de IA.
    """
    return ai_service.process_query(query, context)

@app.get("/health")
async def health_check():
    """
    Endpoint para verificar la salud de la API.

    Propósito:
        Permite a los clientes verificar si la API está en funcionamiento.

    Parámetros:
        Ninguno.

    Estructura de la respuesta:
        - Código de estado 200:
            - Retorna un JSON con el estado 'healthy' y la marca de tiempo actual en formato ISO.
    """
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
