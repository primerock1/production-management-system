"""
Сервисы приложения
"""
from .material_calculator import MaterialCalculatorService, calculate_material_for_product

__all__ = [
    'MaterialCalculatorService',
    'calculate_material_for_product'
]