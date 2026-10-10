import chromadb
from sentence_transformers import SentenceTransformer
from chunker import create_chunks, extract_pages, PDF_PATH


# 1. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# 2. Read and chunk the PDF
pages = extract_pages(PDF_PATH)
chunks = create_chunks(pages)


# 3. Create embeddings
texts = [chunk["text"] for chunk in chunks]
embeddings = model.encode(texts).tolist()


# 4. Create ChromaDB
client = chromadb.PersistentClient(path="chroma_db")


# 5. Create a collection
collection = client.get_or_create_collection(
    name="documents"
)


# 6. Store chunks + embeddings
collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=texts,
    embeddings=embeddings,
    metadatas=[
        {"page_number": chunk["page_number"]}
        for chunk in chunks
    ]
)


print("Vector database created successfully!")
print(f"Stored chunks: {collection.count()}")