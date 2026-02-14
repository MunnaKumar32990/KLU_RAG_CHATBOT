"""
Configuration file for the RAG College Chatbot
Contains all environment variables and system settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# Directory Paths
# ============================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = BASE_DIR / "vector_db"
PROMPTS_DIR = BASE_DIR / "backend" / "prompts"

# ============================================
# Embedding Model Configuration
# ============================================
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DEVICE = "cpu"  # Change to "cuda" if GPU is available

# ============================================
# ChromaDB Configuration
# ============================================
CHROMA_COLLECTION_NAME = "college_documents"
CHROMA_PERSIST_DIRECTORY = str(VECTOR_DB_DIR)

# ============================================
# Document Processing Configuration
# ============================================
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks for context continuity

# ============================================
# Ollama/LLaMA Configuration
# ============================================
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")  # Optimized for low memory
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.3"))  # Lower for more focused answers
OLLAMA_MAX_TOKENS = int(os.getenv("OLLAMA_MAX_TOKENS", "512"))  # Reduced for faster responses

# ============================================
# RAG Retrieval Configuration
# ============================================
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))  # Reduced for smaller model context

# ============================================
# API Configuration
# ============================================
API_TITLE = "College RAG Chatbot API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Production-ready RAG chatbot for college-related queries using LLaMA 3"

# ============================================
# Supported File Extensions
# ============================================
SUPPORTED_EXTENSIONS = [".txt", ".pdf", ".md", ".docx"]

# ============================================
# Logging Configuration
# ============================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
