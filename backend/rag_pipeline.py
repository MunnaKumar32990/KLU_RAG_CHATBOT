"""
RAG Pipeline Module
Implements the core Retrieval Augmented Generation logic
Combines document retrieval with LLaMA 3 generation via Ollama
"""

import logging
from typing import Dict, List
import requests
import json

from backend.config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    OLLAMA_TEMPERATURE,
    OLLAMA_MAX_TOKENS,
    PROMPTS_DIR,
)
from backend.vector_store import vector_store
from backend.schemas import ChatResponse, SourceDocument

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    RAG Pipeline for retrieval and generation
    Retrieves relevant documents and generates responses using LLaMA 3
    """
    
    def __init__(self):
        """Initialize the RAG pipeline"""
        self.ollama_url = f"{OLLAMA_BASE_URL}/api/generate"
        self.model_name = OLLAMA_MODEL
        self.temperature = OLLAMA_TEMPERATURE
        self.max_tokens = OLLAMA_MAX_TOKENS
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load the system prompt from file"""
        try:
            prompt_file = PROMPTS_DIR / "system_prompt.txt"
            if prompt_file.exists():
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            else:
                logger.warning(f"System prompt file not found at {prompt_file}")
                return self._get_default_system_prompt()
        except Exception as e:
            logger.error(f"Error loading system prompt: {str(e)}")
            return self._get_default_system_prompt()
    
    def _get_default_system_prompt(self) -> str:
        """Get default system prompt if file is not found"""
        return """You are a helpful college information assistant. Your role is to answer questions about the college based ONLY on the provided context documents.

CRITICAL RULES:
1. Answer ONLY using information from the provided context
2. If the context doesn't contain the answer, say "I don't have information about that in the college documents"
3. Do NOT mention source files or citations in your answer
4. Be precise, helpful, and friendly
5. Do not make up or assume information not present in the context
6. If multiple sources provide relevant info, synthesize them coherently
7. Provide clean, natural answers without any references to where the information came from"""
    
    def _build_prompt(self, question: str, context: str) -> str:
        """
        Build the complete prompt for LLaMA 3
        
        Args:
            question: User's question
            context: Retrieved context from documents
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""{self.system_prompt}

CONTEXT DOCUMENTS:
{context}

USER QUESTION: {question}

ANSWER:"""
        
        return prompt
    
    def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API to generate response
        
        Args:
            prompt: Complete prompt with context and question
            
        Returns:
            Generated response from LLaMA 3
        """
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                }
            }
            
            logger.info(f"Calling Ollama API with model: {self.model_name}")
            
            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=120  # 2 minute timeout for generation
            )
            
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get("response", "")
            
            logger.info("Successfully generated response from Ollama")
            
            return generated_text.strip()
            
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            return "Error: Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Ollama. Make sure it's running.")
            return "Error: Could not connect to Ollama. Please ensure Ollama is running with 'ollama serve'."
        except Exception as e:
            logger.error(f"Error calling Ollama: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def check_ollama_health(self) -> bool:
        """
        Check if Ollama service is available
        
        Returns:
            True if Ollama is running, False otherwise
        """
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_response(self, question: str) -> ChatResponse:
        """
        Generate response using RAG pipeline
        
        Args:
            question: User's question
            
        Returns:
            ChatResponse with answer and sources
        """
        logger.info(f"Processing question: '{question[:100]}...'")
        
        # Step 1: Retrieve relevant context
        context, sources = vector_store.get_relevant_context(question)
        
        if not context:
            return ChatResponse(
                answer="I couldn't find any relevant information in the college documents to answer your question. Please try rephrasing or ask about topics covered in our documentation.",
                sources=[],
                conversation_id=None
            )
        
        # Step 2: Build prompt
        prompt = self._build_prompt(question, context)
        
        # Step 3: Generate response
        answer = self._call_ollama(prompt)
        
        # Step 4: Format sources
        source_documents = [
            SourceDocument(
                content=src["content"][:300] + "..." if len(src["content"]) > 300 else src["content"],
                source=src["source"],
                relevance_score=src["relevance_score"]
            )
            for src in sources
        ]
        
        # Step 5: Return response
        return ChatResponse(
            answer=answer,
            sources=source_documents,
            conversation_id=None
        )


# Singleton instance
rag_pipeline = RAGPipeline()
