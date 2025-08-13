from fastapi import APIRouter
from fastapi.responses import JSONResponse
from youtubesearchpython import VideosSearch

router = APIRouter()

@router.get("/buscar/")
def buscar_cancion(query: str):
    try:
        videos_search = VideosSearch(query, limit=10)
        resultado = videos_search.result()

        if not resultado or "result" not in resultado:
            return JSONResponse(status_code=404, content={"error": "No se encontraron resultados"})

        canciones = []
        for video in resultado["result"]:
            canciones.append({
                "titulo": video.get("title"),
                "duracion": video.get("duration"),
                "canal": video.get("channel", {}).get("name"),
                "url": video.get("link"),
                "miniatura": video.get("thumbnails", [{}])[0].get("url")
            })

        return canciones

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Ocurrió un error: {str(e)}"})
