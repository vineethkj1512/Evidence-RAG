from sentence_transformers import SentenceTransformer
from chunker import create_chunks, extract_pages, PDF_PATH


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Extract and chunk the document
pages = extract_pages(PDF_PATH)
chunks = create_chunks(pages)


# Create embeddings
texts = [chunk["text"] for chunk in chunks]

embeddings = model.encode(texts)


print(f"Total chunks: {len(chunks)}")
print(f"Embedding shape: {embeddings.shape}")

print("\nFirst chunk:")
print(chunks[0]["text"][:300])

print("\nFirst embedding:")
print(embeddings[0][:10])