from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.search import buscar_cancion
from app.database import get_db

router = APIRouter()

@router.get("/buscar/")
async def buscar(query: str, user_id: str = "anonimo", db: Session = Depends(get_db)):
    return buscar_cancion(query, user_id, db)
