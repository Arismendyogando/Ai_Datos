from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import vision
from google.api_core import retry
import os
import hashlib
import aiofiles
import asyncio
from functools import lru_cache
from typing import Optional
import numpy as np
from config import Config
import logging
from fastapi.responses import JSONResponse

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize configuration
config = Config()

app = FastAPI(
    debug=config.DEBUG,
    title="Invoice Parser API",
    description="API para procesamiento de facturas con OCR",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente de Vision con retry
@retry.Retry()
def get_vision_client():
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_CREDENTIALS_PATH
        return vision.ImageAnnotatorClient()
    except Exception as e:
        logger.error(f"Error initializing Vision client: {e}")
        raise

# Cache para respuestas de OCR
@lru_cache(maxsize=100)
def get_cached_ocr_result(file_hash: str) -> Optional[str]:
    return None  # Expandir con Redis/Memcached en producción

# Generar hash de archivo
async def get_file_hash(file_contents: bytes) -> str:
    return hashlib.sha256(file_contents).hexdigest()

# Cliente singleton con reconexión
class VisionClientSingleton:
    _instance = None
    _lock = asyncio.Lock()
    
    @classmethod
    async def get_instance(cls):
        if not cls._instance:
            async with cls._lock:
                if not cls._instance:
                    cls._instance = get_vision_client()
        return cls._instance
    
    @classmethod
    async def reconnect(cls):
        async with cls._lock:
            cls._instance = get_vision_client()
            return cls._instance

# Inicializar cliente
vision_client = None

@app.on_event("startup")
async def startup_event():
    global vision_client
    try:
        vision_client = await VisionClientSingleton.get_instance()
    except Exception as e:
        logger.error(f"Failed to initialize Vision client: {e}")
        raise

async def process_file_async(contents: bytes, background_tasks: BackgroundTasks):
    try:
        # Verificar caché
        file_hash = await get_file_hash(contents)
        cached_result = get_cached_ocr_result(file_hash)
        if cached_result:
            return cached_result

        # Procesar con Vision API
        image = vision.Image(content=contents)
        response = vision_client.document_text_detection(image=image)
        text = response.full_text_annotation.text

        # Guardar en caché en background
        background_tasks.add_task(lambda: get_cached_ocr_result(file_hash))
        
        return text
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise

@app.post("/api/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        # Validar extensión
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in Config.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Formato no soportado. Permitidos: {', '.join(Config.ALLOWED_EXTENSIONS)}"
            )

        # Validar tamaño
        if file.size > Config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Archivo demasiado grande. Máximo: {Config.MAX_FILE_SIZE / 1024 / 1024}MB"
            )

        # Leer archivo en chunks para archivos grandes
        chunks = []
        async for chunk in file.stream():
            chunks.append(chunk)
        contents = b''.join(chunks)

        # Procesar archivo
        text = await process_file_async(contents, background_tasks)
        
        return JSONResponse(
            content={"text": text},
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Error en upload_file: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/health")
async def health_check():
    """Endpoint para verificar salud del servicio"""
    try:
        # Verificar conexión a Vision API
        await VisionClientSingleton.get_instance()
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            content={"status": "unhealthy", "error": str(e)},
            status_code=503
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        content={"error": str(exc)},
        status_code=500
    )
