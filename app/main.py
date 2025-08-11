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
    

# ENDPOINT_product_START
@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit = 10, db: Session = Depends(get_db)):
    db_product_all =  crud.get_products(db, skip=skip, limit=limit)
    if not db_product_all:
        raise HTTPException(status_code=404, detail="Semua Produk Tidak Ada")
    return db_product_all

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product tidak ada")
    return db_product
# ENDPOINT_product_END

# ENDPOINT_orderss_START
@app.post("/orders", response_model=schemas.OrderOut)
def get_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)

@app.get("/orders", response_model=list[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@app.get("/orders/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")
    return db_order
# ENDPOINT_orderss_END


def rot():
    return {"Message": "Mini E-Commerce API Sedang Berjalan..."}