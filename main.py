from fastapi import FastAPI
from routers.main_router import router as main_router

app = FastAPI()



# Incluir todas las rutas
app.include_router(main_router)

