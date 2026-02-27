from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, jobs
from utils.config import settings
from database.database import engine
from sqlalchemy import text

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