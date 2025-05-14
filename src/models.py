from sqlalchemy import Column, Integer, String, Float,ForeignKey
from src.database import Base  # ✅ Fixed import path

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer,nullable=False)
    discount_percentage = Column(Float, default=0.0)  # ✅ Newly added
    seller_name = Column(String(255), nullable=True)  # ✅ Newly added
    seller_contact = Column(String(255), nullable=True)  # ✅ Newly added
class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit= Column(Float, nullable=False)
