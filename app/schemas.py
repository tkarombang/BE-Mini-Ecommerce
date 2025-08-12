from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List

# PRODUCT SCHEMA start
class ProductState(BaseModel):
  nama: str = Field(..., min_length=3, max_length=50)
  price: float = Field(..., gt=0)
  deskripsi: str = Field(..., min_leng=5)
  kategori: str 
  stok: int = Field(..., ge=0)
  rating: float = Field(..., ge=0, le=5)
  image: str

class ProductCreate(ProductState):
  pass

class Product(ProductState):
  id: int

model_config = ConfigDict(from_attributes=True)
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

model_config = ConfigDict(from_attributes=True)#UNTUK ORM MODE

class OrderOut(BaseModel):
  id: int
  total_price: float
  created_at: datetime
  items: List[OrderItemResponse]

model_config = ConfigDict(from_attributes=True)
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

model_config = ConfigDict(from_attributes=True)
#ORDER SCHEMA end