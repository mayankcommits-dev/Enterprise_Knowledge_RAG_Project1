from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_chunks(chunks):
    chunks_embedding = model.encode(chunks)
    return chunks_embedding

def embed_query(query):
    query_embedding = model.encode(query)
    return query_embedding

    