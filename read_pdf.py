import pymupdf

pdf_path = "data/documents/sample.pdf"

document = pymupdf.open(pdf_path)

print(f"Total pages: {len(document)}")

for page_number, page in enumerate(document):
    text = page.get_text()

    print(f"\n--- Page {page_number + 1} ---")
    print(text[:1000])

document.close()