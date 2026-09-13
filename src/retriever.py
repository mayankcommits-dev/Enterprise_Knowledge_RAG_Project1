from src import embeddings
from src import vector_store

def retrieve(question,top_k):
    output= []
    query_embedding =embeddings.embed_query(question)

    results  = vector_store.search(query_embedding, top_k)

    for i in range(len(results["ids"][0])):

        record = {
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        }
        output.append(record)
    return output