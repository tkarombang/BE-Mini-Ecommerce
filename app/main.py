from fastapi import Depends, FastAPI, HTTPException
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import text
from app import crud_product, models, schemas, crud_order
from app.database import get_db, engine

# Membuat tabel dari model
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini E-Commerce API")

@app.get("/")
def read_root(session: Session = Depends(get_db)):
    try:
        result = session.execute(text("SELECT 1")).scalar()
        return {"message": "Mini E-Commerce API is running 🚀", "db_test": result}
    except sqlalchemy.exc.SQLAlchemyError as e:
        return {"message": "Gagal terhubung ke database", "error": str(e)}
    

# ENDPOINT_product_START
@app.post("/products", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db=db, product=product)

@app.get("/products", response_model=list[schemas.ProductOut])
def read_products(skip: int = 0, limit = 10, db: Session = Depends(get_db)):
    db_product_all =  crud_product.get_products(db, skip=skip, limit=limit)
    if not db_product_all:
        raise HTTPException(status_code=404, detail="Semua Produk Tidak Ada")
    return db_product_all

@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product tidak ada")
    return db_product

@app.put("/product/{product_id}", response_model=schemas.ProductOut)
def upd_product(product_id: int, product_upd: schemas.ProductUpdate ,db: Session = Depends(get_db)):
    crud_product.update_product(db, product_id, product_upd)

@app.delete("/product/{product_id}", response_model=schemas.ProductOut)
def del_product(product_id: int, db: Session = Depends(get_db)):
    return crud_product.delete_product(db, product_id)
# ENDPOINT_product_END

# ENDPOINT_orderss_START
@app.post("/orders", response_model=schemas.OrderOut)
def get_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud_order.create_order(db=db, order=order)

@app.get("/orders", response_model=list[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return crud_order.get_orders(db)

@app.get("/orders/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud_order.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")
    return db_order

@app.put("/orders/{order_id}", response_model=schemas.OrderOut)
def update_order_endpoint(order_id: int, order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    order = crud_order.update_order(db, order_id, order_data)
    if not order:
        raise HTTPException(status_code=404, detail="Order Tidak Ada")
    return order

@app.delete("/orders/{order_id}")
def delete_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    order = crud_order.delete_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order Tidak Ada")
    return {"message": "Order Sukses Terhapus"}
# ENDPOINT_orderss_END


def rot():
    return {"Message": "Mini E-Commerce API Sedang Berjalan..."}