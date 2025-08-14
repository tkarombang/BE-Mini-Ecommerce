import datetime
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from app.crud_product import get_product

# CRUD ORDER start
#Create_Order
def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
  if not order.items:
    raise HTTPException(status_code=400, detail="Order harus memiliki minimal 1 Item")  
  
  #1.Ambil_semua_product_id_dari_data_pesanan_yang_masuk
  product_ids = [item.product_id for item in order.items]

  #2.Ambil_semua_product_terkait_dalam_SATU_query_yang_efisien
  products = db.query(models.Product).filter(models.Product.id.in_(product_ids)).all()

  #3.Simpan_kedala_object_baru_untuk_hasil_pencarian_poin(1-2)
  products_obj = {p.id: p for p in products}

  #Cek_apakah_semua_produk_yang_diminta_ada_di_database
  if len(products) != len(products_obj):
    found_obj = products_obj.keys()
    missing_ids = [pid for pid in products_obj if pid not in found_obj]
    raise HTTPException(
      status_code=404,
      detail=f"Produk dengan ID {missing_ids} Tidak Ditemukan"
    )
  
  #4.Inisialisasi_daftar_pesanan_&_total_harga
  order_items_list = []
  total_price = 0

  #5.Iterasi_data_pesanan|lakukan_validasi|hitung_harga_menggunakan_products_obj(BUKAN QUERY DATABASE LAGI)
  for item in order.items:
    product = products_obj[item.product_id]

    if product.stok < item.quantity:
      raise HTTPException(
        status_code=400,
        detail=f"Stok Produk '{product.nama}' Tidak Mencukupi {product.stok}"
      )
    #Kurangi_stok_produk
    product.stok -= item.quantity
    #Totalkan_keseluruhan_harga_&_Item
    item_price = product.price * item.quantity
    total_price += item_price
    #Buat_object_untuk_daftar_item_pesanan
    order_items_list.append(models.OrderItem(
      product_id=item.product_id,
      quantity=item.quantity,
      price=item_price
    ))

  #6.Buat_Objek_untuk_Pesanan_Utama
  db_order = models.Order(
    # customer_name=order.customer_name,
    # customer_email=order.customer_email,
    total_price=total_price,
    items=order_items_list
  )

  #7.Simpan_semua_Perubahan
  db.add(db_order)
  db.commit()
  db.refresh(db_order)

  return db_order


#Read_All_Order
def get_orders(db: Session) -> List[models.Order]:
  orders = db.query(models.Order).options(
    joinedload(models.Order.items).joinedload(models.OrderItem.product)
  ).all()

  return orders

#Read_Satu_Order_By_Id
def get_order_by_id(db: Session, order_id: int):
  order = db.query(models.Order).filter(models.Order.id == order_id).first()
  if not order:
    raise HTTPException(status_code=404, detail="Order tidak ditemukan")
  return  order

#Update_Order
def get_product_by_ids(db: Session, product_ids: List[int]) -> List[models.Product]:
  return db.query(models.Product).filter(models.Product.id.in_(product_ids)).all()
def update_order(db: Session, order_id: int, order_data: schemas.OrderCreate) -> Optional[models.Order]:
  #Ambil_Pesanan_dari_database_berdasarkan_ID
  db_order = get_order_by_id(db, order_id)
  if not db_order:
    return None
    
  ##1:Kembalikan_Stok_Lama_Sebelum_Update
  #a.ambil ID produk dari Item pesanan lama
  old_product_ids = [item.product_id for item in db_order.items]
  #b.ambil semua produk lama dalam SATU query
  old_products = get_product_by_ids(db, old_product_ids)
  old_products_obj = {p.id: p for p in old_products}

  #c.kembalikan stok produk lama dengan efisien
  for item in db_order.items:
    product = old_products_obj.get(item.product_id)
    if product:
      product.stok += item.quantity
    
  ##2:Hapus_semua_order_item_lama
  db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()
  #a.ambil ID produk dari item pesanan baru
  new_product_ids = [item.product_id for item in order_data.items]
  #c.ambil semua produk baru dalam SATU query
  new_products = get_product_by_ids(db, new_product_ids)
  new_products_obj = {p.id: p for p in new_products}

  #d.cek apakah semua produk baru ditemukan
  if len(new_products) != len(new_product_ids):
    missing_ids = [pid for pid in new_product_ids if pid not in new_products_obj]
    raise ValueError(f"Produk dengan ID {missing_ids} Not Found")
  
  ##3:Kurangi_Stok_baru_dan_Simpan_item_Baru
  total_price = 0
  order_items = []
  for item in order_data.items:
    #a.lewati_jika_quantity_didalam_item_0
    if item.quantity <= 0:
      continue

    product = new_products_obj[item.product_id]
    if product.stok < item.quantity:
      raise ValueError(f"Stok Produk {product.nama} Habis")
    
    #b.kurangi_stok_&_menghitung_total_price
    product.stok -= item.quantity
    item_price = product.price * item.quantity
    total_price += item_price

    order_items.append(models.OrderItem(
      order_id=order_id,
      product_id=item.product_id,
      quantity=item.quantity,
      price=item_price
    ))

  ##4:Simpan Perubahan
  db_order.total_price = total_price
  # db_order.customer_name = order_data.customer_name
  # db_order.customer_email = order_data.customer_email
  db.add_all(order_items)

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








