from app.ai.embeddings import model
from app.ai.vectordb import search
from app.ai.llm import generate_answer


def retrieve_context(question: str, n_results: int = 3):

    question_embedding = model.encode(question).tolist()

    results = search(question_embedding, n_results)

    documents = results.get("documents", [[]])[0]

    return documents


def ask_question(question: str):

    context = retrieve_context(question)

    answer = generate_answer(question, context)

    return {
        "question": question,
        "answer": answer,
        "sources": context
    }