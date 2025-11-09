"""
VAMU AI Service - Main FastAPI Application
Provides AI-powered features for the VAMU platform.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.features.inspiration.presentation.router import router as inspiration_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-powered features for VAMU platform including venue suggestions, chatbot, and AI agents",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(inspiration_router, prefix="/api/v1")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service information."""
    return {
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
    }

# Health check
@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION,
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Docs available at: http://localhost:{settings.PORT}/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info(f"Shutting down {settings.APP_NAME}")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions."""
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
    )
