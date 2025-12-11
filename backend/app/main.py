from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    material_type,
    product_type,
    workshop,
    product,
    product_workshop,
    material_calculator,
)

app = FastAPI(
    title="Production Management API",
    description="API для управления производством",
    version="1.0.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(material_type.router)
app.include_router(product_type.router)
app.include_router(workshop.router)
app.include_router(product.router)
app.include_router(product_workshop.router)
app.include_router(material_calculator.router)

@app.get("/")
def root():
    """Корневой endpoint"""
    return {
        "message": "Production Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "material_types": "/api/material-types",
            "product_types": "/api/product-types",
            "workshops": "/api/workshops",
            "products": "/api/products",
            "product_workshops": "/api/product-workshops",
            "calculator": "/api/calculator",
        }
    }

@app.get("/health")
def health_check():
    """Проверка здоровья API"""
    return {"status": "ok"}