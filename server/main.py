from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routers import user, jobs
from server.utils.config import settings

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    settings.backend_url
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

@app.get("/")
def root():
    return {"message": "home page"}