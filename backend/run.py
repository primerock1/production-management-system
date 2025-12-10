import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Запуск Production Management API")
    print("=" * 60)
    print(f"📡 Сервер запущен на: http://localhost:{settings.PORT}")
    print(f"📚 Документация API: http://localhost:{settings.PORT}/docs")
    print(f"📖 ReDoc: http://localhost:{settings.PORT}/redoc")
    print("=" * 60)
    print("Нажмите CTRL+C для остановки сервера")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=settings.PORT,
        reload=True
    )