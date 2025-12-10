from pydantic_settings import BaseSettings
from pathlib import Path
import os

# Определяем путь к БД (в корне проекта)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "production_db.sqlite"

class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Database (путь к БД в корне проекта)
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()