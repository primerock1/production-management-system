from pydantic import BaseModel
from typing import Optional

class MaterialTypeBase(BaseModel):
    """Базовая схема типа материала"""
    name: str
    loss_percentage: Optional[float] = None

class MaterialTypeCreate(MaterialTypeBase):
    """Схема для создания типа материала"""
    pass

class MaterialTypeResponse(MaterialTypeBase):
    """Схема ответа с типом материала"""
    id: int
    
    class Config:
        from_attributes = True