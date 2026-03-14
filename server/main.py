from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import user, jobs
from utils.config import settings
from database.database import get_db
from sqlalchemy import text
from utils.logging_config import setup_logging
import logging
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
# origins = [
#     settings.backend_url,
#     settings.frontend_url,
#     settings.nginx_baseurl
# ]
origins = ["*"]

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
def global_expression_handler(request: Request, exc: Exception):
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
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except:
        return {"status": "unhealthy"}

@app.get("/")
def root():
    return {"message": "home page"}