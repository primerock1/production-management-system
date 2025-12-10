from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.material_type import MaterialType
from app.schemas.material_type import MaterialTypeCreate, MaterialTypeResponse

router = APIRouter(prefix="/api/material-types", tags=["Material Types"])

@router.get("/", response_model=List[MaterialTypeResponse])
def get_material_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех типов материалов"""
    material_types = db.query(MaterialType).offset(skip).limit(limit).all()
    return material_types

@router.get("/{material_type_id}", response_model=MaterialTypeResponse)
def get_material_type(material_type_id: int, db: Session = Depends(get_db)):
    """Получить тип материала по ID"""
    material_type = db.query(MaterialType).filter(MaterialType.id == material_type_id).first()
    if not material_type:
        raise HTTPException(status_code=404, detail="Material type not found")
    return material_type

@router.post("/", response_model=MaterialTypeResponse, status_code=201)
def create_material_type(material_type: MaterialTypeCreate, db: Session = Depends(get_db)):
    """Создать новый тип материала"""
    # Проверяем, существует ли уже такой тип материала
    existing = db.query(MaterialType).filter(MaterialType.name == material_type.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Material type with this name already exists")
    
    db_material_type = MaterialType(**material_type.model_dump())
    db.add(db_material_type)
    db.commit()
    db.refresh(db_material_type)
    return db_material_type