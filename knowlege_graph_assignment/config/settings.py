"""
Configuration management for RAG system with Knowledge Graph.
Loads and validates environment variables.
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # =============================================================================
    # LLM Configuration
    # =============================================================================
    llm_provider: str = Field(default="google", description="LLM provider: openai, google, anthropic")
    
    # OpenAI
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4-turbo-preview", description="OpenAI model name")
    openai_embedding_model: str = Field(default="text-embedding-3-large", description="OpenAI embedding model")
    
    # Google Gemini
    google_api_key: Optional[str] = Field(default=None, description="Google API key")
    google_model: str = Field(default="gemini-1.5-pro", description="Google model name")
    google_embedding_model: str = Field(default="models/embedding-001", description="Google embedding model")
    
    # Anthropic
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    anthropic_model: str = Field(default="claude-3-opus-20240229", description="Anthropic model name")
    
    # =============================================================================
    # Neon DB Configuration
    # =============================================================================
    neon_db_uri: str = Field(..., description="Neon DB connection URI")
    neon_api_key: Optional[str] = Field(default=None, description="Neon API key (optional)")
    
    # =============================================================================
    # Neo4j Configuration
    # =============================================================================
    neo4j_uri: str = Field(default="bolt://localhost:7687", description="Neo4j connection URI")
    neo4j_username: str = Field(default="neo4j", description="Neo4j username")
    neo4j_password: str = Field(..., description="Neo4j password")
    neo4j_database: str = Field(default="neo4j", description="Neo4j database name")
    
    # =============================================================================
    # Vector Configuration
    # =============================================================================
    embedding_dimension: int = Field(default=768, description="Embedding vector dimension")
    vector_index_type: str = Field(default="hnsw", description="Vector index type: hnsw or ivfflat")
    hnsw_m: int = Field(default=16, description="HNSW M parameter")
    hnsw_ef_construction: int = Field(default=64, description="HNSW ef_construction parameter")
    
    # =============================================================================
    # Document Processing Configuration
    # =============================================================================
    chunk_size: int = Field(default=1000, description="Text chunk size in characters")
    chunk_overlap: int = Field(default=200, description="Overlap between chunks")
    top_k_retrieval: int = Field(default=5, description="Number of chunks to retrieve")
    min_confidence_threshold: float = Field(default=0.7, description="Minimum confidence threshold")
    
    # =============================================================================
    # OCR Configuration
    # =============================================================================
    tesseract_cmd: str = Field(default="/opt/homebrew/bin/tesseract", description="Path to Tesseract")
    tesseract_lang: str = Field(default="eng", description="Tesseract language")
    ocr_confidence_threshold: int = Field(default=60, description="OCR confidence threshold (0-100)")
    
    # =============================================================================
    # Application Configuration
    # =============================================================================
    environment: str = Field(default="development", description="Environment: development or production")
    log_level: str = Field(default="INFO", description="Logging level")
    max_upload_size_mb: int = Field(default=100, description="Maximum file upload size in MB")
    session_timeout_minutes: int = Field(default=60, description="Session timeout in minutes")
    
    # =============================================================================
    # RAG Pipeline Configuration
    # =============================================================================
    llm_temperature: float = Field(default=0.1, description="LLM temperature for generation")
    max_response_tokens: int = Field(default=1000, description="Maximum tokens for response")
    enable_graph_retrieval: bool = Field(default=True, description="Enable graph-based retrieval")
    graph_traversal_depth: int = Field(default=2, description="Graph traversal depth")
    vector_retrieval_weight: float = Field(default=0.6, description="Weight for vector retrieval")
    graph_retrieval_weight: float = Field(default=0.4, description="Weight for graph retrieval")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"
    
    @property
    def max_upload_size_bytes(self) -> int:
        """Get maximum upload size in bytes."""
        return self.max_upload_size_mb * 1024 * 1024
    
    def get_llm_api_key(self) -> str:
        """Get the API key for the selected LLM provider."""
        if self.llm_provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OpenAI API key not set")
            return self.openai_api_key
        elif self.llm_provider == "google":
            if not self.google_api_key:
                raise ValueError("Google API key not set")
            return self.google_api_key
        elif self.llm_provider == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError("Anthropic API key not set")
            return self.anthropic_api_key
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")
    
    def get_llm_model(self) -> str:
        """Get the model name for the selected LLM provider."""
        if self.llm_provider == "openai":
            return self.openai_model
        elif self.llm_provider == "google":
            return self.google_model
        elif self.llm_provider == "anthropic":
            return self.anthropic_model
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")
    
    def get_embedding_model(self) -> str:
        """Get the embedding model name for the selected LLM provider."""
        if self.llm_provider == "openai":
            return self.openai_embedding_model
        elif self.llm_provider == "google":
            return self.google_embedding_model
        else:
            raise ValueError(f"Embedding not supported for provider: {self.llm_provider}")
    
    def validate_retrieval_weights(self) -> None:
        """Validate that retrieval weights sum to 1.0."""
        total = self.vector_retrieval_weight + self.graph_retrieval_weight
        if not (0.99 <= total <= 1.01):  # Allow small floating point errors
            raise ValueError(
                f"Retrieval weights must sum to 1.0, got {total:.2f} "
                f"(vector: {self.vector_retrieval_weight}, graph: {self.graph_retrieval_weight})"
            )


# Global settings instance
settings = Settings()

# Validate settings on import
settings.validate_retrieval_weights()
