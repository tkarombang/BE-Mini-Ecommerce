import datetime
from typing import List
from sqlalchemy.orm import Session
from app import models, schemas

# CRUD ORDER start
#Create_Order
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

#Read_All_Order
def get_orders(db: Session) -> List[models.Order]:
  return db.query(models.Order).all()

#Read_Satu_Order_By_Id
def get_order_by_id(db: Session, order_id: int):
  return db.query(models.Order).filter(models.Order.id == order_id).first() 

#Update_Order
def update_order(db: Session, order_id: int, order_data: schemas.OrderCreate):
  order = db.query(models.Order).filter(models.Order.id == order_id).first()
  if not order:
    return None
  
  #1. hapus_item_lama
  db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()

  #2. tambah_item_baru
  total_price = 0
  for item in order_data.item:
    total_price += item.price * item.quantity
    new_item = models.OrderItem(
      order_id=order.id,
      product_id=item.product_id,
      quantity=item.quantity,
      price=item.price
    )
    db.add(new_item)
  
  order.total_price = total_price
  order.created_at = datetime.datetime.utcnow()
  db.commit()
  db.refresh(order)
  return order

#Delete_Order
def delete_order(db: Session, order_id: int):
  order = db.query(models.Order).filter(models.Order.id == order_id).first()
  if not order:
    return None
  
  # ambil_semua_item_di_order
  items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
  # kembalikan_stok_produk
  for item in items:
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if product:
      product.stok += item.quantity
      db.add(product)

  db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()
  db.delete(order)
  db.commit()
  return order
# CRUD ORDER end 


