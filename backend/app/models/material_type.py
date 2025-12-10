from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class MaterialType(Base):
    """Тип материала"""
    __tablename__ = "material_type"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    loss_percentage = Column(Float, nullable=True)