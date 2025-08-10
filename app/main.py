from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

app = FastAPI(title="Mini E-Commerce API")

@app.get("/")
def read_root(session: Session = Depends(get_db)):
    try:
        result = session.execute(text("SELECT 1")).scalar()
        return {"message": "Mini E-Commerce API is running 🚀", "db_test": result}
    except Exception as e:
        return {"message": "Gagal terhubung ke database", "error": str(e)}

