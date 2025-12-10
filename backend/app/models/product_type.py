from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class ProductType(Base):
    """Тип продукции"""
    __tablename__ = "product_type"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    coefficient = Column(Float, nullable=True)