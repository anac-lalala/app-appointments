"""
FastAPI application entry point.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.infrastructure.db import check_db_health

# Dependency injection / startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Application starting up...")
    yield
    # Shutdown
    print("Application shutting down...")

# Create app instance
app = FastAPI(
    title="Citas API",
    description="MVP API for appointment management system",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/health/live")
async def health_live():
    """Liveness probe - always returns 200 if app is running."""
    return {"status": "alive"}

@app.get("/health/ready")
async def health_ready():
    """Readiness probe - returns 200 if app is ready to serve."""
    if not await check_db_health():
        raise HTTPException(status_code=503, detail="database not ready")
    return {"status": "ready"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Citas API",
        "version": "0.1.0",
        "docs": "/docs",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
