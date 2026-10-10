import re

from retriever import retrieve


# ============================================================
# EVALUATION DATASET
# ============================================================

evaluation_dataset = [

    {
        "question": "What payment methods are supported?",
        "expected_page": 1
    },

    {
        "question": "What happens when a payment fails?",
        "expected_page": 13
    },

    {
        "question": "What is regression testing?",
        "expected_page": 19
    },

    {
        "question": "What causes delayed confirmation messages?",
        "expected_page": 16
    },

    {
        "question": "What are the major defects in the application?",
        "expected_page": 3
    }

]


# ============================================================
# PAGE NUMBER NORMALIZATION
# ============================================================

def normalize_page(page):

    """
    Converts different page formats into an integer.

    Examples:

        1        -> 1
        "1"      -> 1
        "Page 1" -> 1
        "page_1" -> 1
    """

    if page is None:
        return None

    if isinstance(page, int):
        return page

    text = str(page).strip()

    match = re.search(
        r"\d+",
        text
    )

    if match:

        return int(
            match.group()
        )

    return None


# ============================================================
# SINGLE QUESTION EVALUATION
# ============================================================

def evaluate_question(
    question,
    expected_page,
    top_k=3
):

    results = retrieve(
        question,
        n_results=top_k
    )

    pages = []

    for metadata in results["metadatas"][0]:

        page = metadata.get(
            "page_number"
        )

        normalized_page = normalize_page(
            page
        )

        if normalized_page is not None:

            pages.append(
                normalized_page
            )


    expected_page = normalize_page(
        expected_page
    )


    # --------------------------------------------------------
    # Recall @ 1
    # --------------------------------------------------------

    recall_at_1 = (
        len(pages) > 0
        and pages[0] == expected_page
    )


    # --------------------------------------------------------
    # Recall @ 3
    # --------------------------------------------------------

    recall_at_3 = (
        expected_page in pages[:3]
    )


    # --------------------------------------------------------
    # Reciprocal Rank
    # --------------------------------------------------------

    reciprocal_rank = 0.0

    if expected_page in pages:

        rank = (
            pages.index(expected_page)
            + 1
        )

        reciprocal_rank = 1 / rank


    return {

        "question": question,

        "expected_page": expected_page,

        "retrieved_pages": pages,

        "recall_at_1": recall_at_1,

        "recall_at_3": recall_at_3,

        "reciprocal_rank": reciprocal_rank

    }


# ============================================================
# COMPLETE EVALUATION
# ============================================================

def evaluate():

    results = []

    recall_at_1_total = 0

    recall_at_3_total = 0

    mrr_total = 0.0


    for item in evaluation_dataset:

        result = evaluate_question(

            question=item["question"],

            expected_page=item["expected_page"],

            top_k=3

        )

        results.append(
            result
        )


        if result["recall_at_1"]:

            recall_at_1_total += 1


        if result["recall_at_3"]:

            recall_at_3_total += 1


        mrr_total += (
            result["reciprocal_rank"]
        )


    total = len(
        evaluation_dataset
    )


    if total == 0:

        return {

            "recall_at_1": 0,

            "recall_at_3": 0,

            "mrr": 0,

            "details": []

        }


    return {

        "recall_at_1":
            (recall_at_1_total / total) * 100,

        "recall_at_3":
            (recall_at_3_total / total) * 100,

        "mrr":
            mrr_total / total,

        "details":
            results

    }


# ============================================================
# TERMINAL REPORT
# ============================================================

if __name__ == "__main__":

    report = evaluate()


    print()
    print("=" * 60)
    print("              EVIDENCE-RAG EVALUATION")
    print("=" * 60)


    for result in report["details"]:

        print()

        print(
            "Question:",
            result["question"]
        )

        print(
            "Expected Page:",
            result["expected_page"]
        )

        print(
            "Retrieved Pages:",
            result["retrieved_pages"]
        )

        print(
            "Recall@1:",
            result["recall_at_1"]
        )

        print(
            "Recall@3:",
            result["recall_at_3"]
        )

        print(
            "Reciprocal Rank:",
            f"{result['reciprocal_rank']:.3f}"
        )


    print()
    print("=" * 60)

    print(
        f"Recall@1 : "
        f"{report['recall_at_1']:.2f}%"
    )

    print(
        f"Recall@3 : "
        f"{report['recall_at_3']:.2f}%"
    )

    print(
        f"MRR      : "
        f"{report['mrr']:.3f}"
    )

    print("=" * 60)