from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict
import os
import logging
from pathlib import Path
from datetime import datetime

from backend.config import config
from backend.services.invoice_parser import InvoiceParser

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

# Inicialización del parser de facturas
invoice_parser = InvoiceParser()

@app.post("/upload", response_model=Dict[str, str])
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint para subir y procesar un archivo de factura.

    Propósito:
        Recibe un archivo, lo valida (tipo y tamaño) y lo envía al servicio de procesamiento de facturas.

    Parámetros:
        - file (UploadFile): El archivo a subir. Se espera que sea un archivo en el formulario 'multipart/form-data'.

    Estructura de la respuesta:
        - En caso de éxito (código de estado 200):
            - Retorna un JSON con los datos extraídos de la factura. La estructura exacta depende del contenido de la factura.
        - En caso de error:
            - Código de estado 400: Si no se proporciona ningún archivo o el tipo de archivo no está permitido.
            - Código de estado 413: Si el tamaño del archivo excede el límite permitido.
            - Código de estado 500: Si ocurre un error durante el procesamiento del archivo.
    """
    try:
        # Validar que se haya proporcionado un archivo
        if not file.filename:
            raise HTTPException(status_code=400, detail="No se proporcionó ningún archivo")
        
        # Verificar el tipo de archivo
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in config.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"El tipo de archivo {file_ext} no está permitido. Tipos soportados: {', '.join(config.ALLOWED_FILE_TYPES)}"
            )
        
        # Verificar el tamaño del archivo
        file_size = file.file.seek(0, 2)
        file.file.seek(0)
        if file_size > config.max_file_size_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"El tamaño del archivo excede el máximo permitido de {config.MAX_FILE_SIZE_MB}MB"
            )
        
        # Procesar el archivo utilizando el servicio de InvoiceParser
        logger.info(f"Procesando archivo: {file.filename}")
        result = await invoice_parser.process_file(file)
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al procesar el archivo: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al procesar el archivo")

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
