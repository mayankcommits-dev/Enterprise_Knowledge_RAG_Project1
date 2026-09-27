from src import rag_pipeline
from src import retriever


#question = "What caused the payment gateway authentication failures?"
test_questions = [
    "What caused the payment gateway authentication failures?",
    "What caused the invoice OCR failures?",
    "What caused the order processing database failure?",
    "What should happen after allowed system retries are exhausted?",
    "What caused the Kubernetes cluster outage?",
    "Why is the mobile application crashing during login?"
]

for question in test_questions:

    retrieved = retriever.retrieve(question, 3)

    print("\nQUESTION:", question)

    for chunk in retrieved:
        print(
            chunk["metadata"]["document_id"],
            "distance:",
            round(chunk["distance"], 3)
        )

    result = rag_pipeline.ask(question, 3)

    print("ANSWER:", result["answer"])
    print("SOURCES:", result["sources"])

