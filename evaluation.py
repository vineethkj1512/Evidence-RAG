from retriever import retrieve


# Evaluation dataset
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


print("======================================")
print("       RAG EVALUATION HARNESS")
print("======================================")

print("Total questions:", len(evaluation_dataset))


# Evaluation counters
recall_at_1 = 0
recall_at_3 = 0
mrr_total = 0


# Evaluate every question
for item in evaluation_dataset:

    question = item["question"]
    expected_page = item["expected_page"]

    results = retrieve(question, n_results=3)

    retrieved_pages = [
        metadata["page_number"]
        for metadata in results["metadatas"][0]
    ]

    # Recall@1
    if expected_page in retrieved_pages[:1]:
        recall_at_1 += 1
        r1 = "PASS"
    else:
        r1 = "FAIL"

    # Recall@3
    if expected_page in retrieved_pages[:3]:
        recall_at_3 += 1
        r3 = "PASS"
    else:
        r3 = "FAIL"

    # MRR
    if expected_page in retrieved_pages:

        rank = retrieved_pages.index(expected_page) + 1

        reciprocal_rank = 1 / rank

        mrr_total += reciprocal_rank

    else:

        reciprocal_rank = 0

    # Show individual result
    print("\n--------------------------------------")
    print("Question:", question)
    print("Expected page:", expected_page)
    print("Retrieved pages:", retrieved_pages)
    print("Recall@1:", r1)
    print("Recall@3:", r3)
    print("Reciprocal Rank:", f"{reciprocal_rank:.3f}")


# Calculate final scores
total = len(evaluation_dataset)

recall_at_1_score = (recall_at_1 / total) * 100
recall_at_3_score = (recall_at_3 / total) * 100

mrr_score = mrr_total / total


# Final report
print("\n======================================")
print("          EVALUATION REPORT")
print("======================================")

print(f"Recall@1 : {recall_at_1_score:.2f}%")
print(f"Recall@3 : {recall_at_3_score:.2f}%")
print(f"MRR      : {mrr_score:.3f}")

print("======================================")