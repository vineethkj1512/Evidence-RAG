import os
import fitz
import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

DB_PATH = "chroma_db"
COLLECTION_NAME = "documents"

MODEL_NAME = "all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    MODEL_NAME
)


# ============================================================
# CHROMADB
# ============================================================

client = chromadb.PersistentClient(
    path=DB_PATH
)


# ============================================================
# EXTRACT PDF TEXT
# ============================================================

def extract_pdf(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(
        document,
        start=1
    ):

        text = page.get_text("text").strip()

        if text:

            pages.append({
                "page_number": page_number,
                "text": text
            })

    document.close()

    return pages


# ============================================================
# CHUNK TEXT
# ============================================================

def create_chunks(pages):

    chunks = []

    for page in pages:

        text = page["text"]

        page_number = page["page_number"]

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append({
                    "text": chunk_text,
                    "page_number": page_number
                })

            start += (
                CHUNK_SIZE
                - CHUNK_OVERLAP
            )

    return chunks


# ============================================================
# BUILD / REBUILD VECTOR DATABASE
# ============================================================

def build_vector_database(pdf_path):

    print()
    print("=" * 60)
    print("BUILDING KNOWLEDGE BASE")
    print("=" * 60)

    print(
        f"Document: {os.path.basename(pdf_path)}"
    )


    # --------------------------------------------------------
    # Extract
    # --------------------------------------------------------

    print("\nExtracting PDF text...")

    pages = extract_pdf(
        pdf_path
    )

    print(
        f"Pages extracted: {len(pages)}"
    )


    if not pages:

        raise ValueError(
            "No readable text was found in the PDF."
        )


    # --------------------------------------------------------
    # Chunk
    # --------------------------------------------------------

    print("\nCreating chunks...")

    chunks = create_chunks(
        pages
    )

    print(
        f"Chunks created: {len(chunks)}"
    )


    # --------------------------------------------------------
    # Create fresh collection
    # --------------------------------------------------------

    try:

        client.delete_collection(
            COLLECTION_NAME
        )

        print(
            "\nPrevious knowledge base removed."
        )

    except Exception:

        pass


    collection = client.create_collection(
        name=COLLECTION_NAME
    )


    # --------------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------------

    print("\nGenerating embeddings...")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]


    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True
    )


    # --------------------------------------------------------
    # Store in ChromaDB
    # --------------------------------------------------------

    print("\nStoring vectors...")

    ids = []

    documents = []

    metadatas = []

    embedding_list = []


    for index, chunk in enumerate(chunks):

        ids.append(
            f"chunk_{index}"
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append({
            "page_number": chunk["page_number"],
            "chunk_id": index,
            "source": os.path.basename(
                pdf_path
            )
        })

        embedding_list.append(
            embeddings[index].tolist()
        )


    collection.add(

        ids=ids,

        documents=documents,

        metadatas=metadatas,

        embeddings=embedding_list
    )


    print()
    print("=" * 60)
    print("KNOWLEDGE BASE READY")
    print("=" * 60)

    print(
        f"Document : {os.path.basename(pdf_path)}"
    )

    print(
        f"Pages    : {len(pages)}"
    )

    print(
        f"Chunks   : {len(chunks)}"
    )

    print("=" * 60)


    return {

        "document": os.path.basename(
            pdf_path
        ),

        "pages": len(pages),

        "chunks": len(chunks)

    }