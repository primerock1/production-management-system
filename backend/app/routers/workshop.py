from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.workshop import Workshop
from app.schemas.workshop import WorkshopCreate, WorkshopResponse

router = APIRouter(prefix="/api/workshops", tags=["Workshops"])

@router.get("/", response_model=List[WorkshopResponse])
def get_workshops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех цехов"""
    workshops = db.query(Workshop).offset(skip).limit(limit).all()
    return workshops

@router.get("/{workshop_id}", response_model=WorkshopResponse)
def get_workshop(workshop_id: int, db: Session = Depends(get_db)):
    """Получить цех по ID"""
    workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return workshop

@router.post("/", response_model=WorkshopResponse, status_code=201)
def create_workshop(workshop: WorkshopCreate, db: Session = Depends(get_db)):
    """Создать новый цех"""
    # Проверяем, существует ли уже такой цех
    existing = db.query(Workshop).filter(Workshop.name == workshop.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Workshop with this name already exists")
    
    db_workshop = Workshop(**workshop.model_dump())
    db.add(db_workshop)
    db.commit()
    db.refresh(db_workshop)
    return db_workshop

@router.put("/{workshop_id}", response_model=WorkshopResponse)
def update_workshop(workshop_id: int, workshop: WorkshopCreate, db: Session = Depends(get_db)):
    """Обновить цех"""
    db_workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    if not db_workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    
    # Проверяем уникальность имени (исключая текущую запись)
    existing = db.query(Workshop).filter(
        Workshop.name == workshop.name,
        Workshop.id != workshop_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Workshop with this name already exists")
    
    for key, value in workshop.model_dump().items():
        setattr(db_workshop, key, value)
    
    db.commit()
    db.refresh(db_workshop)
    return db_workshop

@router.delete("/{workshop_id}")
def delete_workshop(workshop_id: int, db: Session = Depends(get_db)):
    """Удалить цех"""
    db_workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    if not db_workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    
    db.delete(db_workshop)
    db.commit()
    return {"message": "Workshop deleted successfully"}