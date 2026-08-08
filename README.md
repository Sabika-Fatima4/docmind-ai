# DocMind AI

DocMind AI is an AI-powered document assistant that allows users to upload PDF documents and interact with them through natural-language questions.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant sections from uploaded documents and generate answers grounded in the available document content.

## Features

- User registration and authentication
- JWT-based authentication
- User-specific document management
- PDF document upload
- PDF text extraction and processing
- Document chunking
- Semantic embeddings using Sentence Transformers
- Vector search using ChromaDB
- Retrieval-Augmented Generation (RAG)
- AI-generated answers using Ollama
- Source references with document pages
- Document deletion
- Interactive document chat interface

## How It Works

1. A user creates an account and logs in.
2. The user uploads a PDF document.
3. The backend extracts and processes the document text.
4. The text is divided into smaller chunks.
5. Each chunk is converted into an embedding using Sentence Transformers.
6. The embeddings and document metadata are stored in ChromaDB.
7. When the user asks a question, the question is converted into an embedding.
8. ChromaDB retrieves the most relevant chunks from the selected document.
9. The retrieved context is passed to the language model.
10. The language model generates an answer using the retrieved information.
11. The frontend displays the answer together with the retrieved sources.

## Architecture

```text
                    React + Vite
                         |
                      REST API
                         |
                      FastAPI
                    /         \
             PostgreSQL      ChromaDB
             Users + Docs    Embeddings
                                |
                         Retrieved Context
                                |
                         Ollama / Llama 3.2
```

## Tech Stack

### Frontend

- React
- Vite
- Axios
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT authentication

### AI / RAG

- Sentence Transformers
- `all-MiniLM-L6-v2`
- ChromaDB
- Ollama
- Llama 3.2

### PDF Processing

- pypdf

## Project Structure

```text
docmind-ai/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── chat.py
│   │   │   ├── chunker.py
│   │   │   ├── embeddings.py
│   │   │   ├── llm.py
│   │   │   ├── pdf_loader.py
│   │   │   ├── rag.py
│   │   │   └── vectordb.py
│   │   │
│   │   ├── auth/
│   │   │   ├── dependencies.py
│   │   │   ├── jwt.py
│   │   │   └── security.py
│   │   │
│   │   ├── database/
│   │   │   ├── database.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── models/
│   │   │   ├── document.py
│   │   │   └── user.py
│   │   │
│   │   ├── routers/
│   │   │   ├── pdf.py
│   │   │   └── users.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── chat.py
│   │   │   └── user.py
│   │   │
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js
│   │   │
│   │   ├── pages/
│   │   │   ├── DocumentChat.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── dashboard.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```
## Running Locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://localhost/docmind
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Start the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL provided by Vite.

## Ollama Setup

DocMind AI uses Ollama for local language-model inference.

Make sure the required model is available:

```bash
ollama pull llama3.2
```

The Ollama service must be running when using document chat.

## Environment Variables

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL database connection |
| `SECRET_KEY` | Secret used to sign JWT access tokens |
| `ALGORITHM` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token expiration time |

Do not commit `.env` files or secret credentials to Git.

## Authentication

DocMind AI uses JWT-based authentication.

After login, the frontend sends the access token with authenticated API requests. The backend validates the token and identifies the current user before allowing access to protected resources.

Documents are associated with their owner, keeping users' documents separated.

## RAG Pipeline

```text
PDF
 ↓
Text Extraction
 ↓
Text Chunking
 ↓
Sentence Transformer Embeddings
 ↓
ChromaDB
 ↓
Question Embedding
 ↓
Similarity Search
 ↓
Relevant Document Chunks
 ↓
Ollama / Llama 3.2
 ↓
Generated Answer + Sources
```

The assistant is instructed to answer using the retrieved document information and to indicate when the available document context is insufficient.

## Current Limitations

DocMind AI is currently an MVP. Its main limitations include:

- PDF files are currently the supported document format.
- The current MVP uses Ollama for local LLM inference, so deployment requires a server capable of running the selected Llama model or a change to a hosted LLM provider.
- ChromaDB is currently used as the vector database.
- Large-scale production deployment would require additional infrastructure for concurrent users and persistent storage.
- Large documents may require more processing time and memory.
- Production-grade rate limiting and usage quotas are not currently implemented.
- Conversation history is currently handled within the document-chat interface rather than as a persistent chat-history system.

## Future Improvements

- Streaming AI responses
- Support for DOCX, TXT and other formats
- Background document processing
- Cloud object storage
- Production-grade vector database
- Persistent conversation history
- Rate limiting and usage quotas
- Improved source highlighting
- Document sharing and permissions
- Usage monitoring and analytics
- Scalable inference infrastructure

## Security

- Passwords are hashed before storage.
- JWTs are used for authentication.
- Protected API endpoints require authentication.
- Documents are associated with authenticated users.
- Secrets are supplied through environment variables.
- Local environment files and generated data should not be committed to the repository.

## Author

**Sabika Fatima**

Final Year Electrical Engineering Student  
NUST, Pakistan
