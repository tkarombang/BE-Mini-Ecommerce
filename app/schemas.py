from pydantic import BaseModel
from typing import Optional

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
    