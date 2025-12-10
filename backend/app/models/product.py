from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    """Продукция"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    product_type_id = Column(Integer, ForeignKey("product_type.id"), nullable=True)
    article = Column(String, nullable=True)
    min_price = Column(Float, nullable=True)
    main_material = Column(String, nullable=True)
    
    # Связи
    product_type = relationship("ProductType", backref="products")
    workshops = relationship("ProductWorkshop", back_populates="product", cascade="all, delete-orphan")