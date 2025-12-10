from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class ProductWorkshop(Base):
    """Связь продукции и цехов"""
    __tablename__ = "product_workshops"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    workshop_id = Column(Integer, ForeignKey("workshops.id"), nullable=False)
    production_time_hours = Column(Float, nullable=True)
    
    # Связи
    product = relationship("Product", back_populates="workshops")
    workshop = relationship("Workshop", backref="product_workshops")
    
    # Уникальное ограничение
    __table_args__ = (UniqueConstraint('product_id', 'workshop_id', name='unique_product_workshop'),)