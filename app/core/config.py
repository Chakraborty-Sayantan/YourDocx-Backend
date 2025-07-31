from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Doc-Redactor API"
    upload_dir: str = Field("/tmp/uploads", env="UPLOAD_DIR")
    max_file_size_mb: int = Field(50, env="MAX_FILE_SIZE_MB")
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    history_max: int = Field(50, env="HISTORY_MAX")

    class Config:
        env_file = ".env"

settings = Settings()