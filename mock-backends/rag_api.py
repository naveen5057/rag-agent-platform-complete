from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Local Mock RAG API")


class Query(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


@app.get("/health")
async def health() -> Any:
    return {"status": "ok", "service": "rag-mock"}


@app.post("/query")
async def query(body: Query) -> Any:
    return {
        "answer": (
            "Sample answer from the local mock RAG API. Replace this service "
            "with your existing RAG API for real retrieval."
        ),
        "question": body.question,
        "sources": [
            {
                "document_id": "sample-ingestion-guide",
                "title": "Sample ingestion guide",
                "snippet": "Documents are ingested, chunked, embedded, and indexed.",
            }
        ],
        "mock": True,
    }
