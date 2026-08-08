from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import Base, engine
from app.models.user import User
from app.models.document import Document

from app.routers import users
from app.routers import pdf


app = FastAPI(
    title="DocMind AI API",
    description="Backend API for DocMind AI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
app.include_router(users.router)
app.include_router(pdf.router)