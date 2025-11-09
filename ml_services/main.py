# main.py
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.settings import get_settings
from config.log_config import setup_logging, get_logger
from api.middleware import setup_middleware
from api.analysis_router import router as analysis_router
from api.unified_router import router as unified_router

settings = get_settings()
setup_logging(settings.log_level, "logs/ml_service.log")
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting ML Service")
    yield
    logger.info("🛑 Shutting down ML Service...")

app = FastAPI(
    title="DSA Code Explanation ML Service",
    description="AI-powered service for explaining Data Structures & Algorithms code",
    version="1.0.0",
    lifespan=lifespan
)

setup_middleware(app)
app.include_router(analysis_router)
app.include_router(unified_router)

@app.get('/health')
async def checkhealth():
    logger.info("Health check requested")
    return {"status": "healthy"}

if __name__ == "__main__":
    logger.info(f"Starting server on port {settings.port or 8001}")
    uvicorn.run(app, host="0.0.0.0", port=settings.port or 8001)
