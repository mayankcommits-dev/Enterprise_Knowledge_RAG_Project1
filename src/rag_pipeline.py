from src import retriever
from src import prompt_builder
from src import llm

RETRIEVAL_DISTANCE_THRESHOLD = 1.1

def ask(question, top_k):
    retrieved_chunks = retriever.retrieve(question, top_k)

    if not retrieved_chunks:
        return {
            "answer": "I don't have enough information to answer this.",
            "sources": []
        }

    best_distance = retrieved_chunks[0]["distance"]

    if best_distance > RETRIEVAL_DISTANCE_THRESHOLD:
        return {
            "answer": "I don't have enough information to answer this.",
            "sources": []
        }

    prompt = prompt_builder.build_prompt(question,retrieved_chunks)

    generated_answer = llm.generate_answer(prompt)

    sources = []

    for chunk in retrieved_chunks:
        metadata = chunk["metadata"]
        source = metadata["source"]

        if source not in sources:
            sources.append(source)

    result = {
        "answer": generated_answer,
        "sources": sources
        }

    return result