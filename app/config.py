import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Guru Pooja Book Sale System"
    DATA_DIR: str = "data"
    BACKUP_DIR: str = os.path.join("data", "backups")
    DATABASE_URL: str = f"sqlite:///./data/guru_pooja.db"

    class Config:
        case_sensitive = True

settings = Settings()

# Ensure directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.BACKUP_DIR, exist_ok=True)

