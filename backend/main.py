"""
FastAPI Main Application
Entry point for the RAG College Chatbot API
Provides endpoints for chat, health checks, and document indexing
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.config import API_TITLE, API_VERSION, API_DESCRIPTION
from backend.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
)
from backend.rag_pipeline import rag_pipeline
from backend.vector_store import vector_store

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting RAG College Chatbot API...")
    logger.info(f"Vector store initialized: {vector_store.is_initialized()}")
    logger.info(f"Documents in collection: {vector_store.get_collection_count()}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down RAG College Chatbot API...")


# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "College RAG Chatbot API",
        "version": API_VERSION,
        "status": "running",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs",
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Verifies that vector DB and Ollama are operational
    """
    vector_db_initialized = vector_store.is_initialized()
    ollama_available = rag_pipeline.check_ollama_health()
    
    status = "healthy" if (vector_db_initialized and ollama_available) else "degraded"
    
    return HealthResponse(
        status=status,
        vector_db_initialized=vector_db_initialized,
        ollama_available=ollama_available,
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main chat endpoint for asking questions
    
    Process:
    1. Receives user question
    2. Retrieves relevant documents from vector DB
    3. Formats prompt with context
    4. Generates response using LLaMA 3 via Ollama
    5. Returns answer with source citations
    """
    try:
        # Validate that vector store is initialized
        if not vector_store.is_initialized():
            raise HTTPException(
                status_code=503,
                detail="Vector database not initialized. Please run the indexing script first: python scripts/index_data.py"
            )
        
        # Validate that Ollama is available
        if not rag_pipeline.check_ollama_health():
            raise HTTPException(
                status_code=503,
                detail="Ollama service is not available. Please ensure Ollama is running with 'ollama serve' and the model is pulled with 'ollama pull llama3'"
            )
        
        # Generate response using RAG pipeline
        logger.info(f"Processing chat request: {request.question[:50]}...")
        response = rag_pipeline.generate_response(request.question)
        
        # Add conversation_id if provided
        if request.conversation_id:
            response.conversation_id = request.conversation_id
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/stats", tags=["Information"])
async def get_stats():
    """
    Get statistics about the indexed documents
    """
    try:
        collection_count = vector_store.get_collection_count()
        is_initialized = vector_store.is_initialized()
        
        return {
            "vector_db_initialized": is_initialized,
            "total_chunks": collection_count,
            "status": "ready" if is_initialized else "not initialized",
        }
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving stats: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting FastAPI server...")
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
