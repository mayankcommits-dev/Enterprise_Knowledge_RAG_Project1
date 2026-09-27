from pathlib import Path
import chromadb

project_root = Path(__file__).resolve().parent.parent
chroma_path = project_root / "chroma_db"

client = chromadb.PersistentClient(path=str(chroma_path))

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


    