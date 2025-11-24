"""
Embedding generation using various LLM providers.
Generates vector embeddings for text chunks.
"""

from typing import List, Union
import numpy as np
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class EmbeddingGenerator:
    """Generate embeddings using configured LLM provider."""
    
    def __init__(self):
        """Initialize embedding generator based on configured provider."""
        self.provider = settings.llm_provider
        self.model_name = settings.get_embedding_model()
        self.dimension = settings.embedding_dimension
        
        # Initialize the appropriate client
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "google":
            self._init_google()
        else:
            raise ValueError(f"Unsupported embedding provider: {self.provider}")
        
        logger.info(
            f"EmbeddingGenerator initialized: provider={self.provider}, "
            f"model={self.model_name}, dimension={self.dimension}"
        )
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.get_llm_api_key())
            logger.info("OpenAI client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    def _init_google(self):
        """Initialize Google Generative AI client."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.get_llm_api_key())
            self.client = genai
            logger.info("Google Generative AI client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Google client: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as list of floats
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return [0.0] * self.dimension
        
        try:
            if self.provider == "openai":
                return self._generate_openai_embedding(text)
            elif self.provider == "google":
                return self._generate_google_embedding(text)
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise
    
    def _generate_openai_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI API.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        response = self.client.embeddings.create(
            model=self.model_name,
            input=text
        )
        embedding = response.data[0].embedding
        return embedding
    
    def _generate_google_embedding(self, text: str) -> List[float]:
        """Generate embedding using Google Generative AI API.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        result = self.client.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_document"
        )
        embedding = result['embedding']
        return embedding
    
    def generate_embeddings_batch(
        self,
        texts: List[str],
        batch_size: int = 100,
        show_progress: bool = True
    ) -> List[List[float]]:
        """Generate embeddings for multiple texts in batches.
        
        Args:
            texts: List of input texts
            batch_size: Number of texts to process per batch
            show_progress: Whether to show progress
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        embeddings = []
        total_batches = (len(texts) + batch_size - 1) // batch_size
        
        logger.info(f"Generating embeddings for {len(texts)} texts in {total_batches} batches")
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            if show_progress:
                logger.info(f"Processing batch {batch_num}/{total_batches}")
            
            try:
                if self.provider == "openai":
                    batch_embeddings = self._generate_openai_batch(batch)
                elif self.provider == "google":
                    batch_embeddings = self._generate_google_batch(batch)
                
                embeddings.extend(batch_embeddings)
                
            except Exception as e:
                logger.error(f"Failed to process batch {batch_num}: {e}")
                # Add zero vectors for failed batch
                embeddings.extend([[0.0] * self.dimension] * len(batch))
        
        logger.info(f"Generated {len(embeddings)} embeddings")
        return embeddings
    
    def _generate_openai_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch using OpenAI.
        
        Args:
            texts: List of texts
            
        Returns:
            List of embeddings
        """
        response = self.client.embeddings.create(
            model=self.model_name,
            input=texts
        )
        embeddings = [item.embedding for item in response.data]
        return embeddings
    
    def _generate_google_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch using Google.
        
        Args:
            texts: List of texts
            
        Returns:
            List of embeddings
        """
        # Google API processes one at a time
        embeddings = []
        for text in texts:
            embedding = self._generate_google_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a search query.
        
        Args:
            query: Search query text
            
        Returns:
            Query embedding vector
        """
        if self.provider == "google":
            # Use retrieval_query task type for Google
            result = self.client.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        else:
            # For other providers, use standard embedding
            return self.generate_embedding(query)
    
    def cosine_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0-1)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)
    
    def normalize_embedding(self, embedding: List[float]) -> List[float]:
        """Normalize embedding to unit length.
        
        Args:
            embedding: Input embedding vector
            
        Returns:
            Normalized embedding
        """
        vec = np.array(embedding)
        norm = np.linalg.norm(vec)
        
        if norm == 0:
            return embedding
        
        normalized = vec / norm
        return normalized.tolist()
