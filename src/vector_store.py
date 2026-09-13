import chromadb

client = chromadb.Client()

collections = client.get_or_create_collection(
    name= "enterprise_knowledge_base")

def store_chunks(ids,embeddings,chunks,metadata):

    collections.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadata)

def search(query_embedding, top_k):

    results = collections.query(query_embeddings=
        [query_embedding.tolist()],n_results=top_k)
    
    return results


    