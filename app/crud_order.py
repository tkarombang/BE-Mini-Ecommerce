import datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas

# CRUD ORDER start
#Create_Order
def create_order(db: Session, order: schemas.OrderCreate):
  if not order.items:
    raise HTTPException(status_code=404, detail="Order harus memiliki minimal 1 Item")  
  
  #1.Deklarasi_order_&_Total-Harga_item(child)
  order_items = []
  total_price = 0
  #1.Melakukan_Penelusuran_&_Pengecekan
  for item in order.items:
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
      raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} Tidak Ditemukan")
    
    if product.stok < item.quantity:
      raise HTTPException(status_code=404, detail=f"Stok Produk {product.nama} Tidak Mencukupi")
    
    #a.Mengurangi_Stok(Produk)_&_Menambah_Total_Harga(Orders)
    product.stok -= item.quantity
    item_price = product.price * item.quantity
    total_price += item_price

    #b.Mengisi(child)_Array_order_items[]
    order_items.append(models.OrderItem(
      product_id=item.product_id,
      quantity=item.quantity,
      price=product.price
    ))

  #2.Buat_Object_Order_dengan_Childnya
  db_order = models.Order(
  # customer_name=order.customer_name,
  # customer_email=order.customer_email,
  total_price=total_price,
  items=order_items
  )

  #3.Simpan
  db.add(db_order)
  db.commit()
  db.refresh(db_order)

  return db_order

#Read_All_Order
def get_orders(db: Session) -> List[schemas.OrderResponse]:
  orders = db.query(models.Order).all()

  response_orders = []
  for order in orders:
    items_with_product = []
    for item in order.items:
      product = db.query(models.Product).filter(models.Product.id == item.product_id).first()            

      if product:
        item_response = schemas.OrderItemResponse(
          id=item.id,
          product=schemas.ProductOut(
            id=product.id,
            nama=product.nama,
            price=product.price,
            deskripsi=product.deskripsi,
            kategori=product.kategori,
            stok=product.stok,
            rating=product.rating,
            image=product.image,
          ),
          quantity=item.quantity,
          price=item.price
        )
      items_with_product.append(item_response)
    
    order_response = schemas.OrderResponse(
      id=order.id,
      total_price=order.total_price,
      created_at=order.created_at,
      items=items_with_product
    )
    response_orders.append(order_response)
    
  return response_orders

#Read_Satu_Order_By_Id
def get_order_by_id(db: Session, order_id: int):
  order = db.query(models.Order).filter(models.Order.id == order_id).first()
  if not order:
    raise HTTPException(status_code=404, detail="Order tidak ditemukan")
  return  order

#Update_Order
def update_order(db: Session, order_id: int, order_data: schemas.OrderCreate):
  db_order = get_order_by_id(db, order_id)

  #1.Kembalikan_Stok_Lama_Sebelum_Update
  for item in db_order.items:
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if product:
      product.stok += item.quantity
    
  #2.Hapus_semua_order_item_lama
  db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()

  #a.telusuri_&_mengisi_order_item
  total_price = 0
  order_item = []
  for item in order_data.items:

    #lewati_jika_quantity_didalam_item_0
    if item.quantity <= 0:
      continue

    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
      raise HTTPException(status_code=404, detail=f"Produk ID {item.product_id} Tidak Ditemukan")
    if product.stok < item.quantity:
      raise HTTPException(status_code=404, detail=f"Stok Produk {product.nama} Habis")
    
    #b.kurangi_stok_&_menghitung_total_price
    product.stok -= item.quantity
    total_price += product.price * item.quantity

    order_item.append(models.OrderItem(
      order_id=order_id,
      product_id=item.product_id,
      quantity=item.quantity,
      price=product.price
    ))
  #c.simpan
  db_order.total_price = total_price
  db.add_all(order_item)
  db.commit()
  db.refresh(db_order)
  return db_order


#Delete_Order
def delete_order(db: Session, order_id: int):
  db_order = get_order_by_id(db, order_id)

  # kembalikan_stok_produk
  for item in db_order.items:
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if product:
      product.stok += item.quantity

  db.delete(db_order)
  db.commit()
  return {"message": "Order berhasil dihapus  dan stok dikembalikan"}
# CRUD ORDER end 


