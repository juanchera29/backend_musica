from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.search import buscar_canciones
from app.downloader import download_audio  # ajusta la ruta si está en otro archivo
from app.stream import obtener_url_video    # importamos la función de stream
import os
import asyncio

router = APIRouter()

@router.get("/buscar/")
async def buscar(query: str, user_id: str = "anonimo"):
    resultado = await buscar_canciones(query)
    return resultado

@router.get("/descargar_audio/")
async def descargar_audio_endpoint(url: str):
    try:
        path = await download_audio(url)
        if os.path.exists(path):
            return FileResponse(path, media_type='audio/mpeg', filename=os.path.basename(path))
        else:
            raise HTTPException(status_code=404, detail="Archivo no encontrado después de la descarga.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar audio: {str(e)}")

@router.get("/stream/")
async def stream_video(query: str):
    try:
        loop = asyncio.get_running_loop()
        url = await loop.run_in_executor(None, obtener_url_video, query)
        return {"stream_url": url}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
