from fastapi import APIRouter, UploadFile, File
import os
import shutil
import uuid

from app.ai.pdf_loader import extract_text
from app.ai.chunker import chunk_text
from app.ai.embeddings import create_embeddings
from app.ai.vectordb import store_chunks
from app.ai.rag import retrieve_context, ask_question
from app.schemas.chat import ChatRequest
router = APIRouter(prefix="/pdf", tags=["PDF"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed."
        }

    document_id = str(uuid.uuid4())

    file_path = os.path.join(
        UPLOAD_FOLDER,
        f"{document_id}_{file.filename}"
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pdf = extract_text(file_path)

    chunks = chunk_text(pdf["page_data"])

    chunk_texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = create_embeddings(chunk_texts)

    store_chunks(
        chunks,
        embeddings,
        document_id,
        file.filename
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "pages": pdf["pages"],
        "chunks": len(chunks),
        "status": "Indexed successfully"
    }

@router.post("/search")
async def search_pdf(
    question: str,
    document_id: str
):

    return {
        "question": question,
        "results": retrieve_context(
            question,
            document_id
        )
    }


@router.post("/chat")
async def chat(request: ChatRequest):

    return ask_question(
        request.question,
        request.document_id
    )