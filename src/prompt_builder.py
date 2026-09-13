def build_prompt(question, retrieved_chunks):
    retrieved=[]
    for chunk in retrieved_chunks:
        text =chunk["text"]
        retrieved.append(text)
    context ="\n\n".join(retrieved)    

    prompt = f"""
    Use only the context below to answer the question.

    Context:
    {context}

    Question:
    {question}

    If the context does not contain enough information, say:
    "I don't have enough information to answer this."

    Do not shorten the answer, tell the root cause if you get proper answer from the
    contexts, tell in detail what happened and just,
    Do not infer or add causes that are not explicitly stated in the context.
    Use only information explicitly supported by the context.

    Answer:
    """
    return prompt


