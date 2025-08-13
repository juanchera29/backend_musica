from fastapi import APIRouter, HTTPException
import yt_dlp
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

executor = ThreadPoolExecutor(max_workers=2)

def formatear_duracion(segundos):
    if segundos is None:
        return "Desconocido"
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos_restantes = segundos % 60
    if horas:
        return f"{horas:02}:{minutos:02}:{segundos_restantes:02}"
    else:
        return f"{minutos:02}:{segundos_restantes:02}"

def buscar_sync(query: str):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': False,
        'force_generic_extractor': False,
        'default_search': 'ytsearch10',  # Buscar más resultados para filtrar los que fallen
        'format': 'bestaudio/best',
        'noplaylist': True,
        'geo_bypass': True,
        'geo_bypass_country': 'US',
        'age_limit': 0,
    }

    resultados = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(query, download=False)

            for entry in search_results.get("entries", []):
                try:
                    if entry.get("id") and entry.get("title"):
                        resultados.append({
                            "titulo": entry.get("title"),
                            "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                            "duracion": formatear_duracion(entry.get("duration")),
                            "miniatura": entry.get("thumbnail") or "No disponible",
                        })
                except yt_dlp.utils.DownloadError:
                    # Ignorar videos con restricciones
                    continue

        if not resultados:
            return {"error": "No se encontraron videos disponibles para esta búsqueda."}

        return resultados

    except Exception as e:
        return {"error": f"Error al buscar: {str(e)}"}

async def buscar_canciones(query: str):
    loop = asyncio.get_running_loop()
    resultados = await loop.run_in_executor(executor, buscar_sync, query)
    return resultados

@router.get("/buscar")
async def api_buscar_canciones(query: str):
    resultados = await buscar_canciones(query)
    if isinstance(resultados, dict) and "error" in resultados:
        raise HTTPException(status_code=400, detail=resultados["error"])
    return {"resultados": resultados}
