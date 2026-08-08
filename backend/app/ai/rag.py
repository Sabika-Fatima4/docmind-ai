from app.ai.embeddings import model
from app.ai.vectordb import search
from app.ai.llm import (
    classify_question,
    generate_answer,
    generate_conversational_answer
)


SIMILARITY_THRESHOLD = 1.2


def retrieve_context(
    question: str,
    document_id: str,
    n_results: int = 3
):

    question_embedding = model.encode(question).tolist()

    results = search(
        question_embedding,
        document_id,
        n_results
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    sources = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        if distance >= SIMILARITY_THRESHOLD:
            continue

        sources.append({
            "text": document,
            "filename": metadata.get("filename"),
            "page": metadata.get("page"),
            "chunk": metadata.get("chunk")
        })

    return sources


def ask_question(question: str, document_id: str):

    question_type = classify_question(question)

    # Normal conversation
    if question_type == "CONVERSATIONAL":

        answer = generate_conversational_answer(question)

        return {
            "question": question,
            "answer": answer,
            "sources": []
        }

    # Document question
    sources = retrieve_context(
        question,
        document_id
    )

    if not sources:
        return {
            "question": question,
            "answer": (
                "I couldn't find enough information to answer "
                "that in the uploaded document."
            ),
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