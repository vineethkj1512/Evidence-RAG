import os
import streamlit as st
from groq import Groq


MODEL_NAME = "openai/gpt-oss-20b"


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

    # Evidence-grounded prompt
    prompt = f"""
You are an Evidence-RAG document question answering assistant.

Answer the user's question using ONLY the provided document evidence.

STRICT RULES:
1. Use only the provided evidence.
2. Do not use outside knowledge.
3. Do not invent information.
4. If the answer is not present in the evidence, say:
   "The document does not provide enough information to answer this."
5. Keep the answer concise and clear.
6. Include relevant page numbers using [Page X].
7. Never invent a page number.

DOCUMENT EVIDENCE:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    # Read the API key from Streamlit Secrets or environment variables
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except (KeyError, FileNotFoundError):
            raise RuntimeError(
                "GROQ_API_KEY is missing. Add it to Streamlit Secrets."
            )

    # Generate answer using Groq
    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content