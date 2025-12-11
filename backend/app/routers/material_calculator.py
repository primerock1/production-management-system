"""
API роутер для расчета сырья
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List

from app.database import get_db
from app.services.material_calculator import calculate_material_for_product
from app.models.product import Product
from app.models.product_workshop import ProductWorkshop
from app.models.workshop import Workshop

router = APIRouter(
    prefix="/api/calculator",
    tags=["calculator"]
)


class MaterialCalculationRequest(BaseModel):
    """Запрос на расчет сырья"""
    product_type_id: int = Field(..., description="ID типа продукции")
    material_type_id: int = Field(..., description="ID типа материала")
    quantity: int = Field(..., gt=0, description="Количество продукции")
    param1: float = Field(..., gt=0, description="Первый параметр (например, длина)")
    param2: float = Field(..., gt=0, description="Второй параметр (например, ширина)")


class MaterialCalculationResponse(BaseModel):
    """Ответ с результатом расчета"""
    required_material: int = Field(..., description="Необходимое количество сырья")
    product_type_id: int
    material_type_id: int
    quantity: int
    param1: float
    param2: float
    success: bool = Field(..., description="Успешность расчета")
    message: str = Field(..., description="Сообщение о результате")


class WorkshopForProductResponse(BaseModel):
    """Цех для производства продукта"""
    workshop_id: int
    workshop_name: str
    workshop_type: str
    staff_count: int
    production_time_hours: float


@router.post("/calculate-material", response_model=MaterialCalculationResponse)
def calculate_required_material(
    request: MaterialCalculationRequest,
    db: Session = Depends(get_db)
):
    """
    Рассчитать количество сырья для производства продукции
    
    Метод рассчитывает количество сырья с учетом:
    - Параметров продукции (param1 * param2)
    - Коэффициента типа продукции
    - Процента потерь материала
    
    Формула: ceil((param1 * param2 * коэффициент) * количество * (1 + потери%/100))
    """
    try:
        result = calculate_material_for_product(
            db=db,
            product_type_id=request.product_type_id,
            material_type_id=request.material_type_id,
            quantity=request.quantity,
            param1=request.param1,
            param2=request.param2
        )
        
        if result == -1:
            return MaterialCalculationResponse(
                required_material=-1,
                product_type_id=request.product_type_id,
                material_type_id=request.material_type_id,
                quantity=request.quantity,
                param1=request.param1,
                param2=request.param2,
                success=False,
                message="Ошибка расчета: неверные данные или несуществующие типы"
            )
        
        return MaterialCalculationResponse(
            required_material=result,
            product_type_id=request.product_type_id,
            material_type_id=request.material_type_id,
            quantity=request.quantity,
            param1=request.param1,
            param2=request.param2,
            success=True,
            message=f"Для производства {request.quantity} единиц продукции потребуется {result} единиц сырья"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при расчете сырья: {str(e)}"
        )


@router.get("/workshops-for-product/{product_id}", response_model=List[WorkshopForProductResponse])
def get_workshops_for_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить список цехов для производства конкретного продукта
    с указанием времени производства в каждом цехе
    """
    try:
        # Проверяем существование продукта
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        
        # Получаем цеха для данного продукта
        workshops_query = db.query(
            ProductWorkshop.workshop_id,
            Workshop.name,
            Workshop.workshop_type,
            Workshop.staff_count,
            ProductWorkshop.production_time_hours
        ).join(
            Workshop, ProductWorkshop.workshop_id == Workshop.id
        ).filter(
            ProductWorkshop.product_id == product_id
        )
        
        workshops = workshops_query.all()
        
        if not workshops:
            return []
        
        return [
            WorkshopForProductResponse(
                workshop_id=workshop.workshop_id,
                workshop_name=workshop.name,
                workshop_type=workshop.workshop_type,
                staff_count=workshop.staff_count,
                production_time_hours=workshop.production_time_hours
            )
            for workshop in workshops
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении цехов: {str(e)}"
        )


@router.get("/total-production-time/{product_id}")
def get_total_production_time(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Рассчитать общее время производства продукта
    (сумма времени во всех цехах)
    """
    try:
        # Проверяем существование продукта
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        
        # Получаем общее время производства
        total_time = db.query(
            db.func.sum(ProductWorkshop.production_time_hours)
        ).filter(
            ProductWorkshop.product_id == product_id
        ).scalar()
        
        return {
            "product_id": product_id,
            "product_name": product.name,
            "total_production_time_hours": float(total_time) if total_time else 0.0,
            "workshops_count": db.query(ProductWorkshop).filter(
                ProductWorkshop.product_id == product_id
            ).count()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при расчете времени: {str(e)}"
        )