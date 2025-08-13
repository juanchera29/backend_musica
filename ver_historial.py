from app.database import SessionLocal, SearchHistory

db = SessionLocal()
resultados = db.query(SearchHistory).all()

for item in resultados:
    print(item.query, item.timestamp)
