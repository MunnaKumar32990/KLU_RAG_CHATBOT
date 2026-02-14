"""
Vector Store Module
Manages ChromaDB vector database for document embeddings
Handles indexing and similarity search operations
"""

import logging
from typing import List, Dict, Tuple
from pathlib import Path

import chromadb
from chromadb.config import Settings
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from backend.config import (
    EMBEDDING_MODEL_NAME,
    EMBEDDING_DEVICE,
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIRECTORY,
    TOP_K_RESULTS,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    """
    Manages the ChromaDB vector store for document embeddings
    Provides methods for indexing documents and performing similarity search
    """
    
    def __init__(self):
        """Initialize the vector store with HuggingFace embeddings"""
        logger.info(f"Initializing embeddings with model: {EMBEDDING_MODEL_NAME}")
        
        # Initialize HuggingFace embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={'device': EMBEDDING_DEVICE},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        self.persist_directory = CHROMA_PERSIST_DIRECTORY
        self.collection_name = CHROMA_COLLECTION_NAME
        self.vector_store = None
        
        # Ensure vector_db directory exists
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Try to load existing vector store
        self._load_or_create_store()
    
    def _load_or_create_store(self):
        """Load existing vector store or create a new one"""
        try:
            # Try to load existing vector store
            self.vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )
            
            # Check if the collection has any documents
            collection_count = self.vector_store._collection.count()
            
            if collection_count > 0:
                logger.info(f"Loaded existing vector store with {collection_count} documents")
            else:
                logger.info("Vector store exists but is empty")
                
        except Exception as e:
            logger.warning(f"Could not load existing vector store: {str(e)}")
            logger.info("Will create new vector store when documents are indexed")
    
    def index_documents(self, documents: List[Document]) -> Dict:
        """
        Index documents into the vector store
        
        Args:
            documents: List of chunked Document objects
            
        Returns:
            Dictionary with indexing statistics
        """
        if not documents:
            logger.warning("No documents to index")
            return {"status": "failed", "message": "No documents provided"}
        
        try:
            logger.info(f"Indexing {len(documents)} document chunks...")
            
            # Delete existing collection if it exists
            if self.vector_store is not None:
                logger.info("Deleting existing collection...")
                try:
                    self.vector_store.delete_collection()
                except:
                    pass
            
            # Create new vector store from documents
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=self.persist_directory,
            )
            
            # Persist the vector store
            self.vector_store.persist()
            
            logger.info(f"Successfully indexed {len(documents)} chunks")
            
            return {
                "status": "success",
                "total_chunks": len(documents),
                "message": f"Successfully indexed {len(documents)} document chunks"
            }
            
        except Exception as e:
            logger.error(f"Error indexing documents: {str(e)}")
            return {
                "status": "failed",
                "message": f"Error indexing documents: {str(e)}"
            }
    
    def similarity_search(
        self, 
        query: str, 
        k: int = TOP_K_RESULTS
    ) -> List[Tuple[Document, float]]:
        """
        Perform similarity search on the vector store
        
        Args:
            query: User's question
            k: Number of top results to return
            
        Returns:
            List of tuples (Document, similarity_score)
        """
        if self.vector_store is None:
            logger.error("Vector store not initialized. Please index documents first.")
            return []
        
        try:
            # Perform similarity search with scores
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            logger.info(f"Found {len(results)} relevant documents for query: '{query[:50]}...'")
            
            return results
            
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            return []
    
    def get_relevant_context(
        self, 
        query: str, 
        k: int = TOP_K_RESULTS
    ) -> Tuple[str, List[Dict]]:
        """
        Get relevant context and source information for a query
        
        Args:
            query: User's question
            k: Number of top results to return
            
        Returns:
            Tuple of (combined_context_text, list_of_source_dicts)
        """
        results = self.similarity_search(query, k=k)
        
        if not results:
            return "", []
        
        # Prepare context and sources
        context_parts = []
        sources = []
        
        for i, (doc, score) in enumerate(results, 1):
            # Add to context with source reference
            context_parts.append(
                f"[Source {i}: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}\n"
            )
            
            # Add to sources list
            sources.append({
                "content": doc.page_content,
                "source": doc.metadata.get('source', 'unknown'),
                "relevance_score": float(1 - score)  # Convert distance to similarity
            })
        
        combined_context = "\n---\n".join(context_parts)
        
        return combined_context, sources
    
    def is_initialized(self) -> bool:
        """Check if vector store is initialized and has documents"""
        if self.vector_store is None:
            return False
        
        try:
            count = self.vector_store._collection.count()
            return count > 0
        except:
            return False
    
    def get_collection_count(self) -> int:
        """Get total number of documents in the collection"""
        if self.vector_store is None:
            return 0
        
        try:
            return self.vector_store._collection.count()
        except:
            return 0


# Singleton instance
vector_store = VectorStore()
