from sqlalchemy import Column, Integer, String
from app.database import Base

class Workshop(Base):
    """Цех производства"""
    __tablename__ = "workshops"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    workshop_type = Column(String, nullable=True)
    staff_count = Column(Integer, nullable=True)