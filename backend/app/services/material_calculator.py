"""
Сервис для расчета количества сырья для производства продукции
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.product_type import ProductType
from app.models.material_type import MaterialType


class MaterialCalculatorService:
    """Сервис для расчета сырья с учетом потерь"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_raw_material(
        self,
        product_type_id: int,
        material_type_id: int,
        quantity: int,
        param1: float,
        param2: float
    ) -> int:
        """
        Рассчитывает количество сырья для производства продукции
        
        Args:
            product_type_id: ID типа продукции
            material_type_id: ID типа материала
            quantity: Количество продукции
            param1: Первый параметр продукции
            param2: Второй параметр продукции
            
        Returns:
            int: Количество сырья с учетом потерь, -1 при ошибке
        """
        try:
            # Проверяем входные данные
            if quantity <= 0 or param1 <= 0 or param2 <= 0:
                return -1
            
            # Получаем тип продукции
            product_type = self.db.query(ProductType).filter(
                ProductType.id == product_type_id
            ).first()
            
            if not product_type:
                return -1
            
            # Получаем тип материала
            material_type = self.db.query(MaterialType).filter(
                MaterialType.id == material_type_id
            ).first()
            
            if not material_type:
                return -1
            
            # Рассчитываем базовое количество сырья на единицу продукции
            # Формула: param1 * param2 * коэффициент_типа_продукции
            base_material_per_unit = param1 * param2 * product_type.coefficient
            
            # Общее количество сырья без учета потерь
            total_base_material = base_material_per_unit * quantity
            
            # Учитываем потери сырья
            # Формула: базовое_количество * (1 + процент_потерь/100)
            loss_multiplier = 1 + (material_type.loss_percentage / 100)
            total_material_with_losses = total_base_material * loss_multiplier
            
            # Возвращаем целое число (округляем вверх для гарантии достаточности)
            import math
            return math.ceil(total_material_with_losses)
            
        except Exception as e:
            print(f"Ошибка при расчете сырья: {e}")
            return -1


def calculate_material_for_product(
    db: Session,
    product_type_id: int,
    material_type_id: int,
    quantity: int,
    param1: float,
    param2: float
) -> int:
    """
    Функция-обертка для расчета сырья
    
    Args:
        db: Сессия базы данных
        product_type_id: ID типа продукции
        material_type_id: ID типа материала  
        quantity: Количество продукции
        param1: Первый параметр продукции (например, длина)
        param2: Второй параметр продукции (например, ширина)
        
    Returns:
        int: Количество сырья с учетом потерь, -1 при ошибке
        
    Example:
        >>> calculate_material_for_product(db, 1, 2, 10, 1.5, 2.0)
        45  # Пример результата
    """
    calculator = MaterialCalculatorService(db)
    return calculator.calculate_raw_material(
        product_type_id=product_type_id,
        material_type_id=material_type_id,
        quantity=quantity,
        param1=param1,
        param2=param2
    )