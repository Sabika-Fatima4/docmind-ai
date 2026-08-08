from fastapi import APIRouter, UploadFile, File,Depends,HTTPException
import os
import shutil
import uuid

from app.ai.pdf_loader import extract_text
from app.ai.chunker import chunk_text
from app.ai.embeddings import create_embeddings
from app.ai.vectordb import store_chunks,delete_document
from app.ai.rag import retrieve_context, ask_question
from app.schemas.chat import ChatRequest

from app.database.dependencies import get_db
from app.models.document import Document
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.models.user import User


router = APIRouter(prefix="/pdf", tags=["PDF"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

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

    document = Document(
        document_id=document_id,
        filename=file.filename,
        owner_id=current_user.id
    )

    db.add(document)
    db.commit()

    return {
        "document_id": document_id,
        "filename": file.filename,
        "pages": pdf["pages"],
        "chunks": len(chunks),
        "status": "Indexed successfully"
    }

@router.post("/search")
def search_pdf(
    question: str,
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.document_id == document_id,
        Document.owner_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "question": question,
        "results": retrieve_context(
            question,
            document_id
        )
    }


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.document_id == request.document_id,
        Document.owner_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return ask_question(
        request.question,
        request.document_id
    )

@router.get("/my-documents")
def get_my_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    documents = db.query(Document).filter(
        Document.owner_id == current_user.id
    ).all()

    return documents

@router.delete("/{document_id}")
def delete_pdf(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.document_id == document_id,
        Document.owner_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    # Delete embeddings from ChromaDB
    delete_document(document_id)

    # Delete the physical PDF file
    file_path = os.path.join(
        UPLOAD_FOLDER,
        f"{document_id}_{document.filename}"
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete the database record
    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }