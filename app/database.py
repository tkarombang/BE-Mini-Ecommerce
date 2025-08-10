from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

#load env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Buat engine koneksi
engine = create_engine(DATABASE_URL)

# Buat session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base untuk model
Base = declarative_base()

# Dependeny untuk mendapatkan session di endpoint
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    