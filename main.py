from fastapi import FastAPI
from routers.main_router import router as main_router

app = FastAPI()

# Ruta raíz para prueba simple
@app.get("/")
async def root():
    return {"message": "Servidor backend de música funcionando"}

# Incluir todas las rutas
app.include_router(main_router)
