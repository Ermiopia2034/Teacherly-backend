from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import TeacherlyException
# Import API router (commented out until it's fully implemented)
# from app.api.v1.api import router as api_router

# Create FastAPI app instance
app = FastAPI(
    title="Teacherly AI Backend",
    description="Backend API for Teacherly AI platform",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
@app.exception_handler(TeacherlyException)
async def teacherly_exception_handler(request: Request, exc: TeacherlyException):
    """
    Global exception handler for all Teacherly custom exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )

# Include API router (commented out until it's fully implemented)
# app.include_router(api_router, prefix="/api")

# Health check endpoint
@app.get("/")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "healthy", "message": "Teacherly AI API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
