from fastapi import FastAPI
from app.routers import users

app = FastAPI(
    title="DocMind AI API",
    description="Backend API for DocMind AI",
    version="1.0.0",
)

app.include_router(users.router)