from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional


# PRODUCT SCHEMA start
class ProductState(BaseModel):
  nama: str = Field(..., min_length=3, max_length=50)
  price: float = Field(..., gt=0)
  deskripsi: str = Field(..., min_length=20)
  kategori: str 
  stok: int = Field(..., ge=0)
  rating: float = Field(..., ge=0, le=5)
  image: str

class ProductCreate(ProductState):
  pass

class ProductUpdate(ProductState):
  nama: Optional[str] = Field(None, min_length=3, max_length=50)
  price: Optional[float] = Field(None, gt=0)
  deskripsi: Optional[str] = Field(None, min_length=20)
  kategori: Optional[str] = None
  stok: Optional[int] = Field(None, ge=0)
  rating: Optional[float] = Field(None, ge=0, le=5)
  image: Optional[str] = None


class ProductOut(ProductState):
  id: int
  model_config = ConfigDict(from_attributes=True)
# PRODUCT SCHEMA end


# ORDER ITEM SCHEMA start
class OrderItemBase(BaseModel):
  product_id: int
  quantity: int
  price: float

class OrderItemCreate(OrderItemBase):
  pass

class OrderItemResponse(BaseModel):
  id: int
  product_id: int
  quantity: int
  price: float
  product: "ProductOut"
  model_config = ConfigDict(from_attributes=True)
# ORDER ITEM SCHEMA end


# ORDER SCHEMA start
# class OrderBase(BaseModel):
#   total_price: float 

class OrderCreate(BaseModel):
  # total_price: float
  items: List[OrderItemCreate]

class OrderResponse(BaseModel):
  id: int
  total_price: float
  # customer_name: Optional[str] = None
  # customer_email: Optional[EmailStr] = None
  created_at: datetime
  items: List[OrderItemResponse]  
  model_config = ConfigDict(from_attributes=True)
#ORDER SCHEMA end