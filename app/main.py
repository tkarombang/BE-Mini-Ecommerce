from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import models, schemas, crud
from app.database import get_db
from .database import engine

# Membuat tabel dari model
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini E-Commerce API")

@app.get("/")
def read_root(session: Session = Depends(get_db)):
    try:
        result = session.execute(text("SELECT 1")).scalar()
        return {"message": "Mini E-Commerce API is running 🚀", "db_test": result}
    except Exception as e:
        return {"message": "Gagal terhubung ke database", "error": str(e)}
    

@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit = 10, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product tidak ada")
    return db_product


def rot():
    return {"Message": "Mini E-Commerce API Sedang Berjalan..."}