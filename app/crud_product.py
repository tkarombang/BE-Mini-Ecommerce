from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas

# CRUD RPODUCT start 
def get_products(db: Session, skip: int = 0, limit: int=10):
  products = db.query(models.Product).offset(skip).limit(limit).all()
  if not products:
    raise HTTPException(status_code=404, detail="Produk Gagal Menampilkan")
  return products

def get_product(db: Session, product_id: int):
  product_by_id = db.query(models.Product).filter(models.Product.id == product_id).first()
  if not product_by_id:
    raise HTTPException(status_code=404, detail="Produk dengan ID Gagal Menampilkan")
  return product_by_id

def create_product(db: Session, product: schemas.ProductCreate):
  db_product = models.Product(**product.model_dump())
  db.add(db_product)
  db.commit()
  db.refresh(db_product)
  return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
  up_product = get_product(db, product_id)
  for key, value in product_update.model_dump().items():
    setattr(up_product, key, value)
  db.commit()
  db.refresh(up_product)
  return up_product

def delete_product(db: Session, product_id: int):
  del_product = get_product(db, product_id)
  db.delete(del_product)
  db.commit()
  return {"message: Berhasil Menghapus Produk"}

# CRUD RPODUCT end



