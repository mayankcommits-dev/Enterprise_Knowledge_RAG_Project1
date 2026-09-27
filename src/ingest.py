from pathlib import Path

from src import document_processor
from src import embeddings
from src import vector_store


project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"


def ingest_documents():
    all_documents = document_processor.load_documents(data_dir)

    all_chunks, all_ids, all_metadata = document_processor.create_chunks(
        all_documents, 50, 10
    )

    chunk_embeddings = embeddings.embed_chunks(all_chunks)

    vector_store.store_chunks(
        all_ids,
        chunk_embeddings,
        all_chunks,
        all_metadata
    )

    print(f"Ingested {len(all_chunks)} chunks into ChromaDB.")


if __name__ == "__main__":
    ingest_documents()