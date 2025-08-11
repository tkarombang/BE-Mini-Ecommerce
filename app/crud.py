from typing import List
from sqlalchemy.orm import Session
from . import models, schemas

# CRUD RPODUCT start 
def get_products(db: Session, skip: int = 0, limit: int=10):
  return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
  return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
  db_product = models.Product(**product.model_dump())
  db.add(db_product)
  db.commit()
  db.refresh(db_product)
  return db_product
# CRUD RPODUCT end


# CRUD ORDER start
#create_order
def create_order(db: Session, order: schemas.OrderCreate):
  # 1.membuat_object_Order
  db_order = models.Order(
    customer_name=order.customer_name,
    customer_email=order.customer_email,
    total_price=order.total_price
  )
  db.add(db_order)
  db.commit()
  db.refresh(db_order)

  # 2.Menambahkan_item_ke_OrderItem
  for item in order.item:
    db_item = models.OrderItem(
      order_id=db_order.id,
      product_id=item.product_id,
      quantity=item.quantity,
      price=item.price
    )
    db.add(db_item)

    # optional: kurangi_stok_produk
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if product:
      product.stok -= item.quantity

  db.commit()
  db.refresh(db_order)
  return db_order

#read_all_order
def get_orders(db: Session) -> List[models.Order]:
  return db.query(models.Order).all()

#read_satu_order_by_id
def get_order_by_id(db: Session, order_id: int):
  return db.query(models.Order).filter(models.Order.id == order_id).first() 
# CRUD ORDER end 


