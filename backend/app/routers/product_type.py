from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.product_type import ProductType
from app.schemas.product_type import ProductTypeCreate, ProductTypeResponse

router = APIRouter(prefix="/api/product-types", tags=["Product Types"])

@router.get("/", response_model=List[ProductTypeResponse])
def get_product_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех типов продукции"""
    product_types = db.query(ProductType).offset(skip).limit(limit).all()
    return product_types

@router.get("/{product_type_id}", response_model=ProductTypeResponse)
def get_product_type(product_type_id: int, db: Session = Depends(get_db)):
    """Получить тип продукции по ID"""
    product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    return product_type

@router.post("/", response_model=ProductTypeResponse, status_code=201)
def create_product_type(product_type: ProductTypeCreate, db: Session = Depends(get_db)):
    """Создать новый тип продукции"""
    # Проверяем, существует ли уже такой тип продукции
    existing = db.query(ProductType).filter(ProductType.name == product_type.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product type with this name already exists")
    
    db_product_type = ProductType(**product_type.model_dump())
    db.add(db_product_type)
    db.commit()
    db.refresh(db_product_type)
    return db_product_type

@router.put("/{product_type_id}", response_model=ProductTypeResponse)
def update_product_type(product_type_id: int, product_type: ProductTypeCreate, db: Session = Depends(get_db)):
    """Обновить тип продукции"""
    db_product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if not db_product_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    
    # Проверяем уникальность имени (исключая текущую запись)
    existing = db.query(ProductType).filter(
        ProductType.name == product_type.name,
        ProductType.id != product_type_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product type with this name already exists")
    
    for key, value in product_type.model_dump().items():
        setattr(db_product_type, key, value)
    
    db.commit()
    db.refresh(db_product_type)
    return db_product_type

@router.delete("/{product_type_id}")
def delete_product_type(product_type_id: int, db: Session = Depends(get_db)):
    """Удалить тип продукции"""
    db_product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if not db_product_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    
    db.delete(db_product_type)
    db.commit()
    return {"message": "Product type deleted successfully"}