from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Order
def get_total_revenue(db: Session) -> float:
  # """
  #   Menghitung total pendapatan dari semua pesanan.
  #   Fungsi ini menjumlahkan total_price dari semua pesanan yang ada id database.
  #   Args:
  #     db: Sesi Database SQLAlchemy.
  #   Returns:
  #     Total Pendapatan keseluruhan sebagai float.
  # """
  total = db.query(func.sum(Order.total_price)).scalar()
  return total or 0.0