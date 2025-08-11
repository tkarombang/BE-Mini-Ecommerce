from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
  __tablename__ = "products"

  id = Column(Integer, primary_key=True, index=True)
  nama = Column(String, nullable=False)
  price = Column(Float, nullable=False)
  deskripsi = Column(String, nullable=False)
  kategori = Column(String, nullable=False)
  stok = Column(Integer, nullable=False)
  rating = Column(Float, nullable=False)
  image = Column(String, nullable=False)


class Order(Base):
  __tablename__ = "orders"

  id = Column(Integer, primary_key=True, index=True)
  customer_name = Column(String, nullable=False)
  customer_email = Column(String, nullable=False)
  total_price = Column(Float, nullable=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now())

  # RELASI KE ORDER ITEMS
  items = relationship("OrderItem", back_populates="order", cascade="all, delete")

class OrderItem(Base):
  __tablename__ = "order_item"

  id = Column(Integer, primary_key=True, index=True)
  order_id = Column(Integer, ForeignKey("orders.id"))
  product_id = Column(Integer, ForeignKey("products.id"))
  quantity = Column(Integer, nullable=False)
  price = Column(Float, nullable=False)

  # RELASI BALIK
  order = relationship("Order", back_populates="items")
  product = relationship("Product")