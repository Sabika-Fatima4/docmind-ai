from fastapi import FastAPI

from app.database.database import Base, engine
from app.models.user import User

from app.routers import users


app = FastAPI(
    title="DocMind AI API",
    description="Backend API for DocMind AI",
    version="1.0.0",
)
Base.metadata.create_all(bind=engine)
app.include_router(users.router)