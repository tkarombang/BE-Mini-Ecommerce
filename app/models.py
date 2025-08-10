from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
  __tablename__ = "products"

  id = Column(Integer, primary_key=True, index=True)
  nama = Column(String, nullable=False)
  price = Column(Float, nullable=False)
  deskripsi = Column(String, nullable=False)
  kategori = Column(String, nullable=False)
  stok = Column(Integer, nullable=False)
  rating = Column(Float, nullable=False)
  image = Column(Integer, nullable=False)
