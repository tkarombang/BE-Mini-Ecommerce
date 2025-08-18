from typing import List
from fastapi import Depends, FastAPI, HTTPException, APIRouter
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import text
from app import crud_analytics, crud_product, models, schemas, crud_order
from app.database import get_db, engine
from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="Mini E-Commerce API")
app = FastAPI()

# Membuat tabel dari model
models.Base.metadata.create_all(bind=engine)

origins = [
    "https://fe-mini-ecommerce.vercel.app",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()



@router.get("/")
def read_root(session: Session = Depends(get_db)):
    try:
        result = session.execute(text("SELECT 1")).scalar()
        return {"message": "Mini E-Commerce API is running 🚀", "db_test": result}
    except sqlalchemy.exc.SQLAlchemyError as e:
        return {"message": "Gagal terhubung ke database", "error": str(e)}
    

# ENDPOINT_product_START
@router.post("/products", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db=db, product=product)

@router.get("/products", response_model=List[schemas.ProductOut])
def read_products(skip: int = 0, limit = 10, db: Session = Depends(get_db)):
    db_product_all =  crud_product.get_products(db, skip=skip, limit=limit)
    return db_product_all

@router.get("/products/{product_id}", response_model=schemas.ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product tidak ada")
    return db_product

@router.put("/products/{product_id}", response_model=schemas.ProductOut)
def upd_product(product_id: int, product_upd: schemas.ProductUpdate ,db: Session = Depends(get_db)):
    return crud_product.update_product(db, product_id, product_upd)

@router.delete("/products/{product_id}")
def del_product(product_id: int, db: Session = Depends(get_db)):
    return crud_product.delete_product(db, product_id)
# ENDPOINT_product_END



@router.get("/analytics/revenue", response_model=float)
def get_total_revenue_endpoint(db: Session = Depends(get_db)):
    total_revenue = crud_analytics.get_total_revenue(db)
    return total_revenue

# ENDPOINT_orderss_START
@router.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud_order.create_order(db=db, order=order)

@router.get("/orders", response_model=List[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return crud_order.get_orders(db)

@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    return crud_order.get_order_by_id(db, order_id)

@router.put("/orders/{order_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud_order.update_order(db, order_id, order_data)

@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return crud_order.delete_order(db, order_id)
# ENDPOINT_orderss_END


app.include_router(router)