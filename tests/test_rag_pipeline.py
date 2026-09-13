from unittest.mock import patch
from src import rag_pipeline

def test_retrieve():

    fake_retrieved_chunks  = [
        {
          "id": "INC-2026-001_chunk_1",
        "text": "irrelevant text",
        "metadata": {
            "document_id": "INC-2026-001",
            "source": "incident_payment_auth.txt"
        },
        "distance": 1.30
    }]
    with patch("src.rag_pipeline.retriever.retrieve") as mock_retrieve, \
         patch("src.rag_pipeline.llm.generate_answer") as mock_answer:

        mock_retrieve.return_value = fake_retrieved_chunks 

        result = rag_pipeline.ask("Why is the mobile app crashing?",3)

        assert result["answer"] == "I don't have enough information to answer this."
        assert result["sources"] == []

        mock_answer.assert_not_called()

def test_known_question():

    fake_retrieved_chunks = [
        {
            "id": "INC-2026-001_chunk_1",
            "text": "Running services continued using the expired cached token.",
            "metadata": {
                "document_id": "INC-2026-001",
                "source": "incident_payment_auth.txt"
            },
            "distance": 0.60
        }
    ]

    with patch("src.rag_pipeline.retriever.retrieve") as mock_retrieve, \
         patch("src.rag_pipeline.llm.generate_answer") as mock_answer:

        mock_retrieve.return_value = fake_retrieved_chunks
        mock_answer.return_value = "The services continued using an expired cached token."

        result = rag_pipeline.ask(
            "What caused the payment authentication failures?",3)

        assert result["answer"] == "The services continued using an expired cached token."
        assert result["sources"] == ["incident_payment_auth.txt"]

        mock_answer.assert_called_once()


def test_duplicate_sources():

    fake_retrieved_chunks = [
        {
            "id": "INC-2026-001_chunk_1",
            "text": "Payment authentication failed.",
            "metadata": {
                "document_id": "INC-2026-001",
                "source": "incident_payment_auth.txt"
            },
            "distance": 0.60
        },
        {
            "id": "INC-2026-001_chunk_2",
            "text": "Services were using the expired token.",
            "metadata": {
                "document_id": "INC-2026-001",
                "source": "incident_payment_auth.txt"
            },
            "distance": 0.65
        }
    ]

    with patch("src.rag_pipeline.retriever.retrieve") as mock_retrieve, \
         patch("src.rag_pipeline.llm.generate_answer") as mock_answer:

        mock_retrieve.return_value = fake_retrieved_chunks
        mock_answer.return_value = "Authentication failed because of the expired token."

        result = rag_pipeline.ask(
            "What caused the authentication failure?",3)

        assert result["sources"] == ["incident_payment_auth.txt"]