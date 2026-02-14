"""
Pydantic models for request/response validation
Defines the API contract for the chatbot endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    """
    question: str = Field(
        ..., 
        description="User's question about the college",
        min_length=1,
        max_length=500,
        example="What are the admission requirements for B.Tech?"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation ID for maintaining context"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are the placement statistics for 2024?",
                "conversation_id": "conv_12345"
            }
        }


class SourceDocument(BaseModel):
    """
    Model for source document metadata
    """
    content: str = Field(..., description="Relevant text chunk from the document")
    source: str = Field(..., description="File path of the source document")
    relevance_score: float = Field(..., description="Similarity score (0-1)")


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint
    """
    answer: str = Field(..., description="Generated answer from LLaMA 3")
    sources: List[SourceDocument] = Field(
        ..., 
        description="List of source documents used for generating the answer"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Conversation ID for tracking"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The B.Tech admission process requires...",
                "sources": [
                    {
                        "content": "Admission criteria: 75% in 12th...",
                        "source": "data/admissions/admission_process.txt",
                        "relevance_score": 0.92
                    }
                ],
                "conversation_id": "conv_12345"
            }
        }


class HealthResponse(BaseModel):
    """
    Health check response
    """
    status: str = Field(..., description="API health status")
    vector_db_initialized: bool = Field(..., description="Vector DB status")
    ollama_available: bool = Field(..., description="Ollama service status")


class IndexStatus(BaseModel):
    """
    Document indexing status
    """
    total_documents: int = Field(..., description="Total documents processed")
    total_chunks: int = Field(..., description="Total chunks created")
    status: str = Field(..., description="Indexing status")
