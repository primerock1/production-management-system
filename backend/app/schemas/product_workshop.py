from pydantic import BaseModel
from typing import Optional

class ProductWorkshopBase(BaseModel):
    """Базовая схема связи продукции и цеха"""
    product_id: int
    workshop_id: int
    production_time_hours: Optional[float] = None

class ProductWorkshopCreate(ProductWorkshopBase):
    """Схема для создания связи продукции и цеха"""
    pass

class ProductWorkshopResponse(ProductWorkshopBase):
    """Схема ответа со связью продукции и цеха"""
    id: int
    
    class Config:
        from_attributes = True