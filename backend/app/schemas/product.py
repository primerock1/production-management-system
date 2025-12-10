from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    """Базовая схема продукции"""
    name: str
    product_type_id: Optional[int] = None
    article: Optional[str] = None
    min_price: Optional[float] = None
    main_material: Optional[str] = None

class ProductCreate(ProductBase):
    """Схема для создания продукции"""
    pass

class ProductResponse(ProductBase):
    """Схема ответа с продукцией"""
    id: int
    
    class Config:
        from_attributes = True