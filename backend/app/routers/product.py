from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.product import Product
from app.models.product_type import ProductType
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всей продукции"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Получить продукцию по ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Создать новую продукцию"""
    # Проверяем, существует ли указанный тип продукции
    if product.product_type_id:
        product_type = db.query(ProductType).filter(ProductType.id == product.product_type_id).first()
        if not product_type:
            raise HTTPException(status_code=400, detail="Product type not found")
    
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product