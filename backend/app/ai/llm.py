import ollama


def generate_answer(question: str, context: list[str]):

    context_text = "\n\n".join(context)

    prompt = f"""
You are DocMind AI, an assistant that answers questions based only on the provided document context.

Document context:
{context_text}

Question:
{question}

Instructions:
- Answer using only the information in the document context.
- If the answer cannot be found in the context, say that the information is not available in the document.
- Do not make up information.
- Keep the answer clear and concise.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]