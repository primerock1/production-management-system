from pydantic import BaseModel
from typing import Optional

class ProductTypeBase(BaseModel):
    """Базовая схема типа продукции"""
    name: str
    coefficient: Optional[float] = None

class ProductTypeCreate(ProductTypeBase):
    """Схема для создания типа продукции"""
    pass

class ProductTypeResponse(ProductTypeBase):
    """Схема ответа с типом продукции"""
    id: int
    
    class Config:
        from_attributes = True