from pydantic import BaseModel
from typing import Optional

class WorkshopBase(BaseModel):
    """Базовая схема цеха"""
    name: str
    workshop_type: Optional[str] = None
    staff_count: Optional[int] = None

class WorkshopCreate(WorkshopBase):
    """Схема для создания цеха"""
    pass

class WorkshopResponse(WorkshopBase):
    """Схема ответа с цехом"""
    id: int
    
    class Config:
        from_attributes = True