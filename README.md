# Enterprise Knowledge Intelligence & RAG Platform

An enterprise-style Retrieval-Augmented Generation system that answers questions using internal knowledge documents, retrieves supporting evidence, abstains when evidence is insufficient, and returns source references.

## Business Problem

Enterprise knowledge is often scattered across incident reports, SOPs, troubleshooting guides, and operational documentation.

This project builds a RAG system that:

- ingests internal knowledge documents
- splits documents into overlapping chunks
- converts chunks into embeddings
- stores and searches them using a vector database
- retrieves relevant evidence for a user's question
- generates answers grounded in the retrieved evidence
- abstains when the retrieved evidence is insufficient
- returns source documents for traceability

## Architecture

```text
Enterprise Documents
        ↓
Load + Extract Metadata
        ↓
Chunking (50 words, 10-word overlap)
        ↓
Sentence Transformer Embeddings
        ↓
Chroma Vector Store
        ↓
User Question
        ↓
Query Embedding
        ↓
Top-K Retrieval
        ↓
Retrieval Sufficiency Gate
        ↓
Prompt + Retrieved Context
        ↓
Groq LLM
        ↓
Grounded Answer + Sources
```

## Project Structure

```text
Enterprise_Knowledge_RAG_Project1/
├── data/
├── src/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── prompt_builder.py
│   ├── llm.py
│   ├── rag_pipeline.py
│   └── main.py
├── tests/
│   └── test_rag_pipeline.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

### 1. Document Processing
Enterprise documents are loaded from the `data/` folder. Metadata is extracted and the documents are split into overlapping chunks.

Current chunking configuration:
- Chunk size: 50 words
- Overlap: 10 words

### 2. Embeddings
Each chunk is converted into a numerical embedding using `sentence-transformers/all-MiniLM-L6-v2`.

### 3. Vector Storage
The chunk embeddings, text, IDs, and metadata are stored in Chroma.

### 4. Retrieval
When a user asks a question, the question is embedded and Chroma retrieves the top-K most similar chunks.

### 5. Grounded Generation
The retrieved chunks are added to the prompt as context. The LLM is instructed to answer only from this evidence and abstain when the evidence is insufficient.

### 6. Source Attribution
The final result contains the generated answer along with the unique source documents retrieved for that answer.

## Retrieval Sufficiency Gate

Vector databases return the nearest available results even when none of the stored documents are actually relevant to the question.

To reduce the risk of unrelated context being sent to the LLM, the pipeline checks the distance of the best retrieved chunk.

During testing, known questions produced best-match distances between approximately `0.50` and `0.90`, while out-of-knowledge questions produced best-match distances above approximately `1.20`.

Based on this small test set, the current experimental threshold is:

```python
1.1
```

If the best retrieved chunk has a distance greater than `1.1`, the pipeline stops before calling the LLM and returns:

```text
I don't have enough information to answer this.
```

with an empty sources list.

This threshold is specific to the current dataset and embedding/vector-store configuration. It is not treated as a universal production threshold and would require broader evaluation and tuning for a larger system.


## Engineering Decisions

### Chunking Strategy

The initial implementation used 20-word chunks with a 5-word overlap. During testing, important root-cause information was split across small chunks and was not consistently retrieved.

The configuration was changed to:

- Chunk size: 50 words
- Overlap: 10 words

This preserved more complete evidence in individual chunks for the current dataset.

The values are experimental rather than universally optimal and should be evaluated against a larger question set.

### In-Memory Vector Store During Development

The project initially used persistent Chroma storage.

After changing the chunking strategy, previously indexed chunks remained in the persistent database and caused retrieval results to contain stale data.

The development version therefore uses an in-memory Chroma client so that every run creates a fresh index.

A production implementation would instead use controlled re-indexing, collection versioning, or another explicit index lifecycle strategy.

### Retrieval-First Debugging

When the system generated an inaccurate answer, the retrieved chunks were inspected before changing the LLM prompt.

This helped distinguish between:

- retrieval failures
- generation failures
- poor chunking
- stale indexed data
- insufficient evidence

This avoids trying to solve retrieval problems only through prompt engineering.


## Source Attribution

The pipeline returns the generated answer together with unique source documents retrieved for the question.

Example:

```python
{
    "answer": "The authentication failures were caused by...",
    "sources": [
        "incident_payment_auth.txt"
    ]
}
```

Duplicate chunks from the same document do not create duplicate source entries.

The returned sources identify the documents used as retrieved context. They should not be interpreted as claim-level citation verification.


## Testing

The project uses `pytest` and mocking to test important pipeline behavior without making unnecessary real LLM calls.

Current tests verify that:

- irrelevant retrieval causes the pipeline to abstain
- the LLM is not called when the retrieval sufficiency gate rejects the evidence
- relevant retrieval can proceed to generation
- duplicate chunks from the same document produce only one source entry
- empty retrieval is handled gracefully without calling the LLM

Run the tests with:

```bash
py -m pytest -v
```


## Dataset

The project currently uses synthetic enterprise documents covering:

- payment gateway authentication incidents
- invoice OCR failures
- database connection pool failures
- automation queue recovery procedures
- API retry policies
- RPA runtime troubleshooting

Synthetic documents are used so that the repository does not expose confidential enterprise information.


## Technologies

- Python
- Groq LLM API
- `openai/gpt-oss-20b`
- Sentence Transformers
- `sentence-transformers/all-MiniLM-L6-v2`
- ChromaDB
- Pytest
- python-dotenv


## Setup

### 1. Install Dependencies

```bash
py -m pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_api_key
```

The `.env` file is excluded from Git and should never be committed to the repository.

### 3. Run the Application

From the project root:

```bash
py -m src.main
```

### 4. Run Tests

```bash
py -m pytest -v
```


## Current Limitations

The current version intentionally remains a focused RAG implementation.

Current limitations include:

- small synthetic knowledge base
- experimentally selected retrieval threshold
- no reranking
- no hybrid keyword/vector retrieval
- no production persistent index lifecycle
- no claim-level citation validation
- no automated RAG evaluation framework
- no deployment or monitoring layer


## Future Improvements

Potential future improvements include:

- larger evaluation datasets
- systematic retrieval-threshold tuning
- reranking
- hybrid search
- persistent vector storage with controlled re-indexing
- structured answer outputs
- claim-level citation validation
- automated RAG evaluation
- guardrails
- API deployment
- monitoring and telemetry


## Key Engineering Learnings

Building the pipeline involved debugging several realistic RAG failure modes:

1. Small chunks fragmented important root-cause evidence.
2. Increasing top-K alone introduced additional irrelevant context.
3. Persistent vector storage retained stale chunks after the chunking strategy changed.
4. Vector search returned nearest neighbors even for questions outside the knowledge base.
5. Retrieval quality needed to be inspected separately from LLM generation quality.
6. A retrieval sufficiency gate reduced unnecessary LLM calls for clearly irrelevant retrieval.
7. Unit tests were added to verify abstention, LLM-call prevention, and source deduplication.

These experiments shaped the final architecture rather than treating RAG as only an embedding-search-LLM pipeline.
