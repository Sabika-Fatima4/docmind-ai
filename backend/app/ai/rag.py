from app.ai.embeddings import model
from app.ai.vectordb import search
from app.ai.llm import generate_answer


def retrieve_context(question: str, document_id: str, n_results: int = 3):

    question_embedding = model.encode(question).tolist()

    results = search(
        question_embedding,
        document_id,
        n_results
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    sources = []

    for document, metadata in zip(documents, metadatas):
        sources.append({
            "text": document,
            "filename": metadata.get("filename"),
            "page": metadata.get("page"),
            "chunk": metadata.get("chunk")
        })

    return sources


def ask_question(question: str, document_id: str):

    sources = retrieve_context(
        question,
        document_id
    )

    if not sources:
        return {
            "question": question,
            "answer": "I couldn't find relevant information in this document.",
            "sources": []
        }

    context = [
        source["text"]
        for source in sources
    ]

    answer = generate_answer(
        question,
        context
    )

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }