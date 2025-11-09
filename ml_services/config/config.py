from pydantic_settings import BaseSettings
from typing import Set, List

class Settings(BaseSettings):
    """
    Centralized application configuration.
    Values can be overridden by environment variables or a .env file.
    """
    # Security settings
    DANGEROUS_IMPORTS: Set[str] = {'os', 'subprocess', 'sys', 'shutil', 'socket'}
    DANGEROUS_FUNCTIONS: Set[str] = {'eval', 'exec', 'compile', '__import__'}

    # Supported languages
    SUPPORTED_LANGUAGES: List[str] = ["python", "javascript"]

    # Logging Level
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

# Create a single, importable instance of the settings
settings = Settings()