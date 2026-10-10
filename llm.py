import ollama


MODEL_NAME = "llama3.2:3b"


def generate_answer(question, retrieved_chunks):

    # Build evidence context
    context_parts = []

    for i, chunk in enumerate(retrieved_chunks):

        page = chunk["page"]
        text = chunk["text"]

        context_parts.append(
            f"[Source {i + 1} | Page {page}]\n{text}"
        )

    context = "\n\n".join(context_parts)

    # Prompt for evidence-grounded answering
    prompt = f"""
You are an Evidence-RAG document question answering assistant.

Your job is to answer the user's question using ONLY the
provided document evidence.

STRICT RULES:

1. Use only the provided evidence.
2. Do not use outside knowledge.
3. Do not invent information.
4. If the answer is not present in the evidence, say:
   "The document does not provide enough information to answer this."
5. Keep the answer concise and clear.
6. Include the relevant page number using [Page X].
7. Never invent a page number.

DOCUMENT EVIDENCE:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    # Ask local Llama model
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]