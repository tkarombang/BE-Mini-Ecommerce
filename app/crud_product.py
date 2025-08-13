from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas

# CRUD RPODUCT start 
def get_products(db: Session, skip: int = 0, limit: int=10) -> List[models.Product]:
  products = db.query(models.Product).offset(skip).limit(limit).all()
  return products

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
  product_by_id = db.query(models.Product).filter(models.Product.id == product_id).first()
  return product_by_id

def create_product(db: Session, product: schemas.ProductCreate):
  db_product = models.Product(**product.model_dump())
  db.add(db_product)
  db.commit()
  db.refresh(db_product)
  return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate) -> models.Product:
  up_product = get_product(db, product_id)
  if not up_product:
    raise HTTPException(status_code=404, detail="Product Tidak Ditemukan")
  
  update_data = product_update.model_dump(exclude_unset=True)

  for key, value in update_data.items():
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



