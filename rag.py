from retriever import retrieve
from llm import generate_answer


# ============================================================
# ASK QUESTION
# ============================================================

def ask_question(
    question,
    top_k=3
):

    results = retrieve(
        question,
        n_results=top_k
    )


    retrieved_chunks = []


    for i, document in enumerate(
        results["documents"][0]
    ):

        metadata = results[
            "metadatas"
        ][0][i]


        page = metadata.get(
            "page_number"
        )


        retrieved_chunks.append({

            "page": page,

            "text": document

        })


    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    answer = generate_answer(

        question,

        retrieved_chunks

    )


    return {

        "question": question,

        "answer": answer,

        "sources": retrieved_chunks

    }


# ============================================================
# TERMINAL MODE
# ============================================================

if __name__ == "__main__":

    question = input(
        "\nAsk a question about the document: "
    )


    result = ask_question(
        question
    )


    print("\n")
    print("=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(
        result["answer"]
    )


    print("\n")
    print("=" * 60)
    print("RETRIEVED SOURCES")
    print("=" * 60)


    for source in result["sources"]:

        print(
            f"\nPage {source['page']}"
        )