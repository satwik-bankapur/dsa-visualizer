from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    model_path: str
    redis_url: str
    log_level: str
    environment: str
    port: Optional[int] = 8001  # Add this line - optional with default value

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()

if __name__ == "__main__":
    settings = get_settings()
    print(f"Model path: {settings.model_path}")
    print(f"Redis URL: {settings.redis_url}")
    print(f"Log level: {settings.log_level}")
    print(f"Environment: {settings.environment}")
    print(f"Port: {settings.port}")  # Add this line too