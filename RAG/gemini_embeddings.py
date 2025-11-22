"""
Gemini Integration Module for Enhanced RAG System

This module provides:
- Gemini embeddings with multilingual support (especially Tamil)
- Gemini LLM integration for text generation
- Batch processing for efficient embedding generation
- LangChain-compatible interfaces
"""

import os
import time
from typing import List, Dict, Optional, Any
import google.generativeai as genai
from langchain_core.embeddings import Embeddings


class GeminiEmbeddings(Embeddings):
    """
    LangChain-compatible Gemini embeddings class
    Supports multilingual embeddings including Tamil
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "models/embedding-001",
        task_type: str = "retrieval_document",
        batch_size: int = 100
    ):
        """
        Initialize Gemini embeddings
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            model_name: Embedding model name
            task_type: Task type for embeddings (retrieval_document, retrieval_query, etc.)
            batch_size: Batch size for processing
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        self.model_name = model_name
        self.task_type = task_type
        self.batch_size = batch_size
        
        print(f"Initialized Gemini Embeddings: {model_name}")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents
        
        Args:
            texts: List of document texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        
        # Process in batches to avoid rate limits
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            
            try:
                # Generate embeddings for batch
                batch_embeddings = []
                for text in batch:
                    result = genai.embed_content(
                        model=self.model_name,
                        content=text,
                        task_type="retrieval_document"
                    )
                    batch_embeddings.append(result['embedding'])
                
                embeddings.extend(batch_embeddings)
                
                # Rate limiting - small delay between batches
                if i + self.batch_size < len(texts):
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"Error embedding batch {i}-{i+len(batch)}: {e}")
                # Add zero vectors for failed embeddings
                batch_embeddings = [[0.0] * 768] * len(batch)  # Gemini embedding dimension
                embeddings.extend(batch_embeddings)
        
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector
        """
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error embedding query: {e}")
            return [0.0] * 768  # Return zero vector on error


class GeminiLLM:
    """
    Gemini LLM wrapper for text generation
    Supports advanced features like safety settings and generation config
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 2048,
        top_p: float = 0.95,
        top_k: int = 40
    ):
        """
        Initialize Gemini LLM
        
        Args:
            api_key: Gemini API key
            model_name: Model name (defaults to GEMINI_MODEL_NAME env var or gemini-2.0-flash-exp)
            temperature: Sampling temperature
            max_output_tokens: Maximum tokens in response
            top_p: Top-p sampling parameter
            top_k: Top-k sampling parameter
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Get model name from env or use provided/default
        self.model_name = model_name or os.getenv('GEMINI_MODEL_NAME', 'gemini-2.0-flash-exp')
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.top_p = top_p
        self.top_k = top_k
        
        # Generation config
        self.generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
        }
        
        # Safety settings - allow most content for RAG use case
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]
        
        # Initialize model - try different model names for compatibility
        try:
            # Try with the configured model name
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            print(f"Initialized Gemini LLM: {self.model_name}")
        except Exception as e:
            print(f"Warning: Could not initialize {self.model_name}: {e}")
            # Fallback to gemini-pro
            try:
                self.model = genai.GenerativeModel(
                    model_name="gemini-pro",
                    generation_config=self.generation_config,
                    safety_settings=self.safety_settings
                )
                self.model_name = "gemini-pro"
                print(f"Initialized Gemini LLM: gemini-pro (fallback)")
            except Exception as e2:
                print(f"Error: Could not initialize any Gemini model: {e2}")
                raise
    
    def generate(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Generate text from prompt
        
        Args:
            prompt: Input prompt
            system_instruction: Optional system instruction
            
        Returns:
            Generated text
        """
        try:
            # Create model with system instruction if provided
            if system_instruction:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config=self.generation_config,
                    safety_settings=self.safety_settings,
                    system_instruction=system_instruction
                )
            else:
                model = self.model
            
            # Generate response
            response = model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            print(f"Error generating text: {e}")
            return f"Error: {str(e)}"
    
    def generate_with_context(
        self,
        query: str,
        context: str,
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Generate response with context (for RAG)
        
        Args:
            query: User query
            context: Retrieved context
            system_instruction: Optional system instruction
            
        Returns:
            Generated response
        """
        prompt = f"""Context:
{context}

Question: {query}

Please answer the question based on the context provided above. If the context doesn't contain enough information to answer the question, say "I don't have enough information in the provided context to answer this question accurately."

Answer:"""
        
        return self.generate(prompt, system_instruction)
    
    def generate_with_sources(
        self,
        query: str,
        contexts: List[Dict[str, Any]],
        min_confidence: float = 0.6
    ) -> Dict[str, Any]:
        """
        Generate response with source attribution
        
        Args:
            query: User query
            contexts: List of context dicts with 'text', 'source', and 'score'
            min_confidence: Minimum confidence threshold
            
        Returns:
            Dict with 'answer', 'sources', 'confidence', and 'has_answer'
        """
        # Check if we have high-confidence contexts
        high_conf_contexts = [c for c in contexts if c.get('score', 0) >= min_confidence]
        
        if not high_conf_contexts:
            return {
                'answer': "I don't have enough confident information to answer this question. The available context doesn't seem relevant enough.",
                'sources': [],
                'confidence': 0.0,
                'has_answer': False
            }
        
        # Build context with sources
        context_parts = []
        sources = []
        
        # Increase from 5 to 8 contexts for better coverage
        max_contexts = min(8, len(high_conf_contexts))
        
        for idx, ctx in enumerate(high_conf_contexts[:max_contexts], 1):
            # Add relevance score to help LLM prioritize
            relevance = ctx.get('score', 0.0)
            context_parts.append(f"[Source {idx}] (Relevance: {relevance:.1%})\n{ctx['text']}")
            sources.append({
                'index': idx,
                'source': ctx.get('source', 'Unknown'),
                'score': relevance
            })
        
        context_text = "\n\n".join(context_parts)
        
        # Enhanced prompt with better structure and accuracy focus
        prompt = f"""You are an expert document analysis assistant with high precision standards.

Context (with sources and relevance scores):
{context_text}

Question: {query}

Critical Instructions:
1. **Analyze Thoroughly**: Read ALL provided sources carefully, paying attention to relevance scores
2. **Source Attribution**: Cite sources using [Source X] notation - cite ALL relevant sources
3. **Evidence-Based**: Use direct quotes from sources to support your answer
4. **Confidence Assessment**: 
   - High (80-100%): Multiple sources agree, clear evidence
   - Medium (60-80%): Some sources support, partial evidence
   - Low (<60%): Weak evidence, uncertain or conflicting information
5. **Completeness**: If context is insufficient, specify exactly what information is missing
6. **Accuracy First**: Never infer, assume, or use external knowledge
7. **Detail & Precision**: Be specific with facts, numbers, names, and dates
8. **Language Support**: Maintain accuracy for both English and Tamil content

Response Format:
- Start with a clear, direct answer
- Support with evidence and citations [Source X]
- State your confidence level and reasoning
- If uncertain, explain why

Provide a comprehensive, well-supported answer:"""
        
        system_instruction = """You are a precise RAG assistant specializing in accurate information retrieval.

Core Principles:
- Accuracy over speed
- Evidence-based responses only
- Transparent about limitations
- Never hallucinate or guess
- Always cite sources
- Maintain high confidence standards

If you're not confident (below 70%), clearly state your uncertainty and explain what additional information would help."""
        
        answer = self.generate(prompt, system_instruction)
        
        # Enhanced confidence calculation
        # Weight by both relevance score and number of sources
        if sources:
            # Base confidence from average relevance
            avg_confidence = sum(s['score'] for s in sources) / len(sources)
            
            # Boost for multiple agreeing sources (up to 15% bonus)
            source_count_bonus = min(0.15, (len(sources) - 1) * 0.03)
            
            # Penalty if only low-relevance sources (below 0.7)
            high_quality_sources = sum(1 for s in sources if s['score'] >= 0.7)
            if high_quality_sources == 0:
                quality_penalty = 0.1
            else:
                quality_penalty = 0
            
            final_confidence = min(1.0, avg_confidence + source_count_bonus - quality_penalty)
        else:
            final_confidence = 0.0
        
        return {
            'answer': answer,
            'sources': sources,
            'confidence': final_confidence,
            'has_answer': True,
            'metadata': {
                'num_sources': len(sources),
                'high_quality_sources': sum(1 for s in sources if s['score'] >= 0.7),
                'avg_relevance': sum(s['score'] for s in sources) / len(sources) if sources else 0
            }
        }



# Utility functions
def test_gemini_connection(api_key: Optional[str] = None) -> bool:
    """
    Test Gemini API connection
    
    Args:
        api_key: Optional API key to test
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("No API key provided")
            return False
        
        genai.configure(api_key=api_key)
        
        # Try a simple embedding
        result = genai.embed_content(
            model="models/embedding-001",
            content="test",
            task_type="retrieval_query"
        )
        
        print("✓ Gemini connection successful")
        return True
        
    except Exception as e:
        print(f"✗ Gemini connection failed: {e}")
        return False


def get_available_models() -> List[str]:
    """
    Get list of available Gemini models
    
    Returns:
        List of model names
    """
    try:
        models = genai.list_models()
        return [m.name for m in models]
    except Exception as e:
        print(f"Error listing models: {e}")
        return []
