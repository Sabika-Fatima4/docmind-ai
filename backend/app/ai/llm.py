import ollama



def classify_question(question: str) -> str:

    prompt = f"""
You are an intent classifier for DocMind AI.

Classify the user's message into exactly ONE category.

DOCUMENT:
Choose DOCUMENT if the message contains ANY question that asks
for factual information, even if it is combined with casual conversation.

Examples:
- "What is this document about?"
- "When was the blood drive?"
- "Who won the World Cup?"
- "Who won the World Cup? Also how are you?"
- "Tell me about the people mentioned in the PDF."
- "What happened on page 5?"

CONVERSATIONAL:
Choose CONVERSATIONAL ONLY when the message is purely casual conversation
and does not ask for factual information.

Examples:
- "Hello"
- "Hi"
- "How are you?"
- "Are you helpful?"
- "Thank you"
- "Goodbye"

IMPORTANT:
If the message contains BOTH a factual question and casual conversation,
choose DOCUMENT.

User message:
{question}

Respond with EXACTLY ONE word:

DOCUMENT

or

CONVERSATIONAL
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

    result = response["message"]["content"].strip().upper()

    if result == "CONVERSATIONAL":
        return "CONVERSATIONAL"

    return "DOCUMENT"

def generate_conversational_answer(question: str):

    prompt = f"""
You are DocMind AI, a friendly and intelligent AI assistant.

The user is having a casual conversation with you rather than asking
about the uploaded document.

Respond naturally and helpfully.

User:
{question}

Keep the response concise and conversational.
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


def generate_answer(question: str, context: list[str]):

    context_text = "\n\n---\n\n".join(context)

    prompt = f"""
You are DocMind AI, an intelligent document assistant.

Your job is to answer the user's question using ONLY the information
contained in the provided document excerpts.

Document excerpts:
{context_text}

User question:
{question}

Rules:

1. Use ONLY the information contained in the document excerpts.
2. Do NOT use outside knowledge, assumptions, or guesses.
3. Do NOT invent names, dates, numbers, events, or facts.
4. If the excerpts do not contain enough information to answer the
   question, say exactly:

"I couldn't find enough information to answer that in the uploaded document."

5. If only part of the question can be answered from the excerpts,
   clearly state what can and cannot be determined.
6. For questions asking what the document is about, give a concise
   overview based only on the provided excerpts.
7. For summarization requests, combine information from the excerpts
   into a coherent summary.
8. For specific questions, give a direct answer supported by the excerpts.
9. Do not mention retrieval, embeddings, vector databases, excerpts,
   internal processing, or these instructions.
10. Keep the response clear, natural, and professional.

Answer:
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