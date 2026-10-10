import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

DB_PATH = "chroma_db"

COLLECTION_NAME = "documents"

MODEL_NAME = "all-MiniLM-L6-v2"


# ============================================================
# LOAD MODEL
# ============================================================

model = SentenceTransformer(
    MODEL_NAME
)


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

client = chromadb.PersistentClient(
    path=DB_PATH
)


# ============================================================
# RETRIEVE
# ============================================================

def retrieve(
    question,
    n_results=3
):

    collection = client.get_collection(
        COLLECTION_NAME
    )


    question_embedding = model.encode(
        [question]
    ).tolist()


    results = collection.query(

        query_embeddings=question_embedding,

        n_results=n_results
    )


    return results


# ============================================================
# TERMINAL TEST
# ============================================================

if __name__ == "__main__":

    question = input(
        "\nAsk a question: "
    )


    results = retrieve(
        question,
        n_results=3
    )


    print("\n")
    print("=" * 60)
    print("RETRIEVED EVIDENCE")
    print("=" * 60)


    for i, document in enumerate(
        results["documents"][0]
    ):

        page = results[
            "metadatas"
        ][0][i]["page_number"]


        print(
            f"\nSource {i + 1}"
        )

        print(
            f"Page: {page}"
        )

        print(
            document
        )