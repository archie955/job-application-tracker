from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from routers import user, jobs
from utils.config import settings
from database.database import engine
from sqlalchemy import text
from utils.logging_config import setup_logging
import logging
from fastapi.responses import JSONResponse


setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
origins = [
    settings.backend_url,
    settings.frontend_url,
    settings.nginx_baseurl
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router)
app.include_router(jobs.router)

@app.exception_handler(Exception)
async def global_expression_handler(request: Request):
    logger.error(
        "Unhandled exception occurred",
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method
        }
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

@app.get("/health")
async def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception:
        return {"status": "unhealthy"}

@app.get("/")
def root():
    return {"message": "home page"}