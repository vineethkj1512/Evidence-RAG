import pymupdf


PDF_PATH = "data/documents/sample.pdf"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def extract_pages(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text().strip()

        if text:
            pages.append({
                "page_number": page_number + 1,
                "text": text
            })

    document.close()

    return pages


def create_chunks(pages):
    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page_number"]

        start = 0

        while start < len(text):
            end = start + CHUNK_SIZE

            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "page_number": page_number
            })

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


pages = extract_pages(PDF_PATH)

chunks = create_chunks(pages)

print(f"Total pages: {len(pages)}")
print(f"Total chunks: {len(chunks)}")

print("\n--- First Chunk ---")
print(chunks[0]["text"])

print("\n--- First Chunk Page ---")
print(chunks[0]["page_number"])