from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class HistorialBusqueda(Base):
    __tablename__ = "historial_busquedas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    query = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
