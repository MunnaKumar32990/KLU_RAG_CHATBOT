"""
Document Loader Module
Handles loading and chunking of documents from the data directory
Supports text files, PDFs, and other document formats
"""

import os
from pathlib import Path
from typing import List, Dict
import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader,
)
from langchain_core.documents import Document

from backend.config import (
    DATA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SUPPORTED_EXTENSIONS,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentLoader:
    """
    Loads and processes documents from the data directory
    Chunks documents using RecursiveCharacterTextSplitter
    """
    
    def __init__(self):
        """Initialize the document loader with text splitter"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        self.data_dir = DATA_DIR
        
    def load_single_file(self, file_path: Path) -> List[Document]:
        """
        Load a single file and return documents
        
        Args:
            file_path: Path to the file
            
        Returns:
            List of Document objects
        """
        try:
            file_extension = file_path.suffix.lower()
            
            if file_extension == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_extension in [".txt", ".md"]:
                loader = TextLoader(str(file_path), encoding='utf-8')
            else:
                logger.warning(f"Unsupported file type: {file_path}")
                return []
            
            documents = loader.load()
            
            # Add source metadata
            for doc in documents:
                doc.metadata["source"] = str(file_path.relative_to(self.data_dir.parent))
            
            logger.info(f"Loaded {len(documents)} document(s) from {file_path.name}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {str(e)}")
            return []
    
    def load_all_documents(self) -> List[Document]:
        """
        Load all documents from the data directory and subdirectories
        
        Returns:
            List of all Document objects
        """
        all_documents = []
        
        if not self.data_dir.exists():
            logger.error(f"Data directory not found: {self.data_dir}")
            return all_documents
        
        # Walk through all subdirectories
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                file_path = Path(root) / file
                
                # Check if file extension is supported
                if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    documents = self.load_single_file(file_path)
                    all_documents.extend(documents)
        
        logger.info(f"Total documents loaded: {len(all_documents)}")
        return all_documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval
        
        Args:
            documents: List of Document objects to chunk
            
        Returns:
            List of chunked Document objects
        """
        if not documents:
            logger.warning("No documents to chunk")
            return []
        
        try:
            chunked_docs = self.text_splitter.split_documents(documents)
            logger.info(f"Created {len(chunked_docs)} chunks from {len(documents)} documents")
            return chunked_docs
        except Exception as e:
            logger.error(f"Error chunking documents: {str(e)}")
            return []
    
    def load_and_chunk(self) -> List[Document]:
        """
        Load all documents and chunk them in one operation
        
        Returns:
            List of chunked Document objects ready for embedding
        """
        logger.info("Starting document loading and chunking process...")
        
        # Load all documents
        documents = self.load_all_documents()
        
        if not documents:
            logger.warning("No documents found to process")
            return []
        
        # Chunk documents
        chunked_documents = self.chunk_documents(documents)
        
        logger.info("Document loading and chunking completed successfully")
        return chunked_documents
    
    def get_document_stats(self, documents: List[Document]) -> Dict:
        """
        Get statistics about loaded documents
        
        Args:
            documents: List of Document objects
            
        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_documents": len(documents),
            "sources": list(set(doc.metadata.get("source", "unknown") for doc in documents)),
            "total_sources": len(set(doc.metadata.get("source", "unknown") for doc in documents)),
        }
        return stats


# Singleton instance
document_loader = DocumentLoader()
