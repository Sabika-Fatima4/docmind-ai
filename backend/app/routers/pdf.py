from fastapi import APIRouter, UploadFile, File
import os
import shutil
from app.ai.pdf_loader import extract_text
from app.ai.chunker import chunk_text
from app.ai.chunker import chunk_text
from app.ai.embeddings import create_embeddings
from app.ai.vectordb import store_chunks
from app.ai.rag import retrieve_context, ask_question
router = APIRouter(prefix="/pdf", tags=["PDF"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed."
        }

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pdf = extract_text(file_path)
    chunks = chunk_text(pdf["text"])
    embeddings = create_embeddings(chunks)
    store_chunks(chunks, embeddings)


    return {
    "filename": file.filename,
    "pages": pdf["pages"],
    "words": len(pdf["text"].split()),
    "characters": len(pdf["text"]),
    "chunks": len(chunks),
    "status": "Indexed successfully"
     }

@router.post("/search")
async def search_pdf(question: str):

    chunks = retrieve_context(question)

    return {
        "question": question,
        "results": chunks
    }

@router.post("/chat")
async def chat(question: str):

    return ask_question(question)