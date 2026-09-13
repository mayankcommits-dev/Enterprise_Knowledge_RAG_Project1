from src import document_processor
from src import embeddings
from src import vector_store
from src import rag_pipeline
from src import retriever
from pathlib import Path

#INGEST DATA
project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"

all_documents = document_processor.load_documents(data_dir)

#CHUNKING
all_chunks,all_ids,all_metadata = document_processor.create_chunks(
    all_documents,50,10)


#EMBEDDINGS
chunk_embeddings = embeddings.embed_chunks(all_chunks)

# print("all_chunks:", len(all_chunks))
# print("all_ids:", len(all_id))
# print("all_metadata:", len(all_metadeta))
# print("chunk_emb length:", len(chunk_emb))

#STORE VECTORS
vector_store.store_chunks(all_ids,chunk_embeddings,all_chunks,all_metadata)


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


#ANSWER
answer = rag_pipeline.ask(question,5)

print("\nFINAL ANSWER:")
print(answer)

print("\nSOURCES:")
for source in answer["sources"]:
    print("-", source)