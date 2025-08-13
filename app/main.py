from fastapi import FastAPI, Form, Query
from fastapi.responses import FileResponse
from app.downloader import download_audio
from app.search import router as search_router
from app.stream import obtener_url_video  # NUEVO IMPORT

app = FastAPI()

app.include_router(search_router)

@app.post("/descargar/")
async def descargar_video(url: str = Form(...)):
    mp3_path = await download_audio(url)
    return FileResponse(path=mp3_path, filename=mp3_path.split("/")[-1], media_type="audio/mpeg")

# NUEVA RUTA PARA OBTENER LA URL DEL VIDEO (con manejo de errores)
@app.get("/stream_url")
async def stream_url(query: str = Query(...)):
    try:
        url = obtener_url_video(query)
        return {"url": url}
    except Exception as e:
        return {
            "error": "No se pudo obtener la URL de streaming",
            "detalle": str(e)
        }
