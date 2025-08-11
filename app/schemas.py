from pydantic import BaseModel, EmailStr
from typing import List

# PRODUCT SCHEMA start
class ProductState(BaseModel):
  nama: str
  price: float
  deskripsi: str
  kategori: str
  stok: int
  rating: float
  image: str

class ProductCreate(ProductState):
  pass

class Product(ProductState):
  id: int

  class Config:
    orm_mode = True
# PRODUCT SCHEMA end



# ORDER ITEM SCHEMA start
class OrderItemBase(BaseModel):
  product_id: int
  quantity: int
  price: int

class OrderItemCreate(OrderItemBase):
  pass

class OrderItemResponse(OrderItemBase):
  id: int

  class Config:
    from_attributes = True #UNTUK ORM MODE
# ORDER ITEM SCHEMA end



# ORDER SCHEMA start
class OrderBase(BaseModel):
  customer_name: str
  customer_email: EmailStr
  total_price: float

class OrderCreate(OrderBase):
  item: List[OrderItemCreate]

class OrderResponse(OrderBase):
  id: int
  items: List[OrderItemResponse]

  class Config:
    from_attributes = True
#ORDER SCHEMA end