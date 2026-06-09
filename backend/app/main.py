"""FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.utils.response import fail

app = FastAPI(
    title=settings.APP_NAME,
    description="知识型阅读工作台后端 API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS - 从环境变量读取允许的源
cors_origins = settings.CORS_ALLOWED_ORIGINS.split(",") if settings.CORS_ALLOWED_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.code,
        content=fail(code=exc.code, message=exc.message).model_dump(),
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle uncaught exceptions."""
    if settings.DEBUG:
        import traceback
        detail = str(exc)
        trace = traceback.format_exc()
    else:
        detail = "Internal server error"
        trace = None

    return JSONResponse(
        status_code=500,
        content=fail(code=500, message=detail).model_dump(),
    )


# Health check
@app.get("/health")
def health_check():
    """Health check endpoint."""
    from app.utils.response import success
    return success(data={"status": "ok"})


# Include API router
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.DEBUG,
    )
