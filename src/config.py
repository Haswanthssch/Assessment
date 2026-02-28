from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database - PostgreSQL (Docker)
    DATABASE_URL: str = "postgresql://admin:admin@postgres:5432/inventory_db"

    # Database - MongoDB Atlas
    MONGODB_URI: str = "mongodb+srv://haswanthssch:dontforget%40123@inventorysystem.eubflik.mongodb.net/"
    MONGODB_DB: str = "activity_logs"

    # Security / JWT
    SECRET_KEY: str = "inventory-super-secret-key-2024"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Flask
    FLASK_SECRET_KEY: str = "flask-inventory-secret-2024"
    FLASK_DEBUG: bool = True

    # App
    APP_PORT: int = 5000
    APP_HOST: str = "0.0.0.0"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
