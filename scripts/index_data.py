"""
Document Indexing Script
Loads all documents from data/ directory and indexes them into ChromaDB
Run this script after adding or updating documents in the data/ folder
"""

import sys
from pathlib import Path

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
from backend.document_loader import document_loader
from backend.vector_store import vector_store

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main indexing function
    Loads documents, chunks them, and indexes into vector store
    """
    logger.info("=" * 80)
    logger.info("STARTING DOCUMENT INDEXING PROCESS")
    logger.info("=" * 80)
    
    try:
        # Step 1: Load and chunk documents
        logger.info("\n[Step 1/3] Loading and chunking documents from data/ directory...")
        chunked_documents = document_loader.load_and_chunk()
        
        if not chunked_documents:
            logger.error("No documents found or loaded. Please add documents to the data/ directory.")
            logger.error("Supported formats: .txt, .pdf, .md, .docx")
            return
        
        # Get statistics
        stats = document_loader.get_document_stats(chunked_documents)
        logger.info(f"\nDocument Statistics:")
        logger.info(f"  - Total chunks created: {stats['total_documents']}")
        logger.info(f"  - Unique source files: {stats['total_sources']}")
        logger.info(f"\nSource files:")
        for source in stats['sources']:
            logger.info(f"  - {source}")
        
        # Step 2: Index documents into vector store
        logger.info(f"\n[Step 2/3] Indexing {len(chunked_documents)} chunks into ChromaDB...")
        result = vector_store.index_documents(chunked_documents)
        
        if result["status"] == "success":
            logger.info(f"\n✓ {result['message']}")
        else:
            logger.error(f"\n✗ {result['message']}")
            return
        
        # Step 3: Verify indexing
        logger.info("\n[Step 3/3] Verifying indexing...")
        collection_count = vector_store.get_collection_count()
        logger.info(f"  - Documents in vector store: {collection_count}")
        
        if collection_count > 0:
            logger.info("\n" + "=" * 80)
            logger.info("INDEXING COMPLETED SUCCESSFULLY!")
            logger.info("=" * 80)
            logger.info("\nYour vector database is ready. You can now:")
            logger.info("  1. Start the FastAPI server: python -m backend.main")
            logger.info("  2. Or use: uvicorn backend.main:app --reload")
            logger.info("  3. Access API docs at: http://localhost:8000/docs")
            logger.info("=" * 80)
        else:
            logger.error("Indexing verification failed. No documents in vector store.")
    
    except Exception as e:
        logger.error(f"\n✗ Error during indexing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
