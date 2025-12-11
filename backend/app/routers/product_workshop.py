from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.product_workshop import ProductWorkshop
from app.models.product import Product
from app.models.workshop import Workshop
from app.schemas.product_workshop import ProductWorkshopCreate, ProductWorkshopResponse

router = APIRouter(prefix="/api/product-workshops", tags=["Product Workshops"])

@router.get("/", response_model=List[ProductWorkshopResponse])
def get_product_workshops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех связей продукции и цехов"""
    product_workshops = db.query(ProductWorkshop).offset(skip).limit(limit).all()
    return product_workshops

@router.get("/{product_workshop_id}", response_model=ProductWorkshopResponse)
def get_product_workshop(product_workshop_id: int, db: Session = Depends(get_db)):
    """Получить связь продукции и цеха по ID"""
    product_workshop = db.query(ProductWorkshop).filter(ProductWorkshop.id == product_workshop_id).first()
    if not product_workshop:
        raise HTTPException(status_code=404, detail="Product workshop relationship not found")
    return product_workshop

@router.post("/", response_model=ProductWorkshopResponse, status_code=201)
def create_product_workshop(product_workshop: ProductWorkshopCreate, db: Session = Depends(get_db)):
    """Создать новую связь продукции и цеха"""
    # Проверяем, существует ли продукция
    product = db.query(Product).filter(Product.id == product_workshop.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    
    # Проверяем, существует ли цех
    workshop = db.query(Workshop).filter(Workshop.id == product_workshop.workshop_id).first()
    if not workshop:
        raise HTTPException(status_code=400, detail="Workshop not found")
    
    # Проверяем, не существует ли уже такая связь
    existing = db.query(ProductWorkshop).filter(
        ProductWorkshop.product_id == product_workshop.product_id,
        ProductWorkshop.workshop_id == product_workshop.workshop_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product workshop relationship already exists")
    
    db_product_workshop = ProductWorkshop(**product_workshop.model_dump())
    db.add(db_product_workshop)
    db.commit()
    db.refresh(db_product_workshop)
    return db_product_workshop

@router.put("/{product_workshop_id}", response_model=ProductWorkshopResponse)
def update_product_workshop(product_workshop_id: int, product_workshop: ProductWorkshopCreate, db: Session = Depends(get_db)):
    """Обновить связь продукции и цеха"""
    db_product_workshop = db.query(ProductWorkshop).filter(ProductWorkshop.id == product_workshop_id).first()
    if not db_product_workshop:
        raise HTTPException(status_code=404, detail="Product workshop relationship not found")
    
    # Проверяем, существует ли продукция
    product = db.query(Product).filter(Product.id == product_workshop.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    
    # Проверяем, существует ли цех
    workshop = db.query(Workshop).filter(Workshop.id == product_workshop.workshop_id).first()
    if not workshop:
        raise HTTPException(status_code=400, detail="Workshop not found")
    
    # Проверяем уникальность связи (исключая текущую запись)
    existing = db.query(ProductWorkshop).filter(
        ProductWorkshop.product_id == product_workshop.product_id,
        ProductWorkshop.workshop_id == product_workshop.workshop_id,
        ProductWorkshop.id != product_workshop_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product workshop relationship already exists")
    
    for key, value in product_workshop.model_dump().items():
        setattr(db_product_workshop, key, value)
    
    db.commit()
    db.refresh(db_product_workshop)
    return db_product_workshop

@router.delete("/{product_workshop_id}")
def delete_product_workshop(product_workshop_id: int, db: Session = Depends(get_db)):
    """Удалить связь продукции и цеха"""
    db_product_workshop = db.query(ProductWorkshop).filter(ProductWorkshop.id == product_workshop_id).first()
    if not db_product_workshop:
        raise HTTPException(status_code=404, detail="Product workshop relationship not found")
    
    db.delete(db_product_workshop)
    db.commit()
    return {"message": "Product workshop relationship deleted successfully"}