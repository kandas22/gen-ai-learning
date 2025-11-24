"""
Neon DB Vector Store implementation using pgvector.
Handles vector storage, indexing, and similarity search.
"""

import psycopg2
from psycopg2.extras import execute_values
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class NeonVectorStore:
    """Vector store using Neon DB (PostgreSQL) with pgvector extension."""
    
    def __init__(self):
        """Initialize Neon DB connection."""
        self.connection = None
        self.cursor = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Neon DB."""
        try:
            # Use the connection URI directly
            self.connection = psycopg2.connect(settings.neon_db_uri)
            self.cursor = self.connection.cursor()
            
            # Log masked URI for debugging
            masked_uri = settings.neon_db_uri.split('@')[-1] if '@' in settings.neon_db_uri else '***'
            logger.info(f"Successfully connected to Neon DB ({masked_uri})")
            
            # Check if tables exist, if not initialize
            self._ensure_tables_exist()
            
        except Exception as e:
            logger.error(f"Failed to connect to Neon DB: {e}")
            raise

    def _ensure_tables_exist(self):
        """Check if required tables exist and initialize if not."""
        try:
            self.cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'documents'
                );
            """)
            exists = self.cursor.fetchone()[0]
            
            if not exists:
                logger.warning("Tables not found, initializing database schema...")
                self.initialize()
            
        except Exception as e:
            logger.error(f"Failed to check/initialize tables: {e}")
    
    def initialize(self):
        """Initialize database schema and pgvector extension."""
        try:
            # Enable pgvector extension
            self.cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            # Create documents table
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    filename VARCHAR(500) NOT NULL,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_pages INTEGER,
                    file_size INTEGER,
                    metadata JSONB
                );
            """)
            
            # Create chunks table with vector column
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id SERIAL PRIMARY KEY,
                    document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
                    chunk_index INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    embedding vector({settings.embedding_dimension}),
                    page_number INTEGER,
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create index on document_id for faster lookups
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_chunks_document_id 
                ON document_chunks(document_id);
            """)
            
            # Create vector index for similarity search
            if settings.vector_index_type == "hnsw":
                self.cursor.execute(f"""
                    CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw 
                    ON document_chunks 
                    USING hnsw (embedding vector_cosine_ops)
                    WITH (m = {settings.hnsw_m}, ef_construction = {settings.hnsw_ef_construction});
                """)
            elif settings.vector_index_type == "ivfflat":
                self.cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_chunks_embedding_ivfflat 
                    ON document_chunks 
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100);
                """)
            
            self.connection.commit()
            logger.info("Database schema initialized successfully")
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def add_document(
        self, 
        filename: str, 
        total_pages: int, 
        file_size: int, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Add a document record.
        
        Args:
            filename: Name of the document
            total_pages: Total number of pages
            file_size: File size in bytes
            metadata: Optional metadata dictionary
            
        Returns:
            Document ID
        """
        try:
            import json
            self.cursor.execute(
                """
                INSERT INTO documents (filename, total_pages, file_size, metadata)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (filename, total_pages, file_size, json.dumps(metadata or {}))
            )
            document_id = self.cursor.fetchone()[0]
            self.connection.commit()
            logger.info(f"Added document: {filename} (ID: {document_id})")
            return document_id
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Failed to add document: {e}")
            raise
    
    def add_chunks(
        self, 
        document_id: int, 
        chunks: List[Dict[str, Any]]
    ):
        """Add document chunks with embeddings.
        
        Args:
            document_id: ID of the parent document
            chunks: List of chunk dictionaries with keys:
                   - content: Text content
                   - embedding: Vector embedding
                   - chunk_index: Index of chunk
                   - page_number: Page number
                   - metadata: Optional metadata
        """
        try:
            import json
            values = [
                (
                    document_id,
                    chunk['chunk_index'],
                    chunk['content'],
                    chunk['embedding'],
                    chunk.get('page_number'),
                    json.dumps(chunk.get('metadata', {}))
                )
                for chunk in chunks
            ]
            
            execute_values(
                self.cursor,
                """
                INSERT INTO document_chunks 
                (document_id, chunk_index, content, embedding, page_number, metadata)
                VALUES %s
                """,
                values
            )
            
            # Retrieve generated IDs
            self.cursor.execute(
                "SELECT id, chunk_index FROM document_chunks WHERE document_id = %s ORDER BY chunk_index",
                (document_id,)
            )
            rows = self.cursor.fetchall()
            
            # Map IDs back to chunks
            id_map = {row[1]: row[0] for row in rows}
            for chunk in chunks:
                if chunk['chunk_index'] in id_map:
                    chunk['chunk_id'] = id_map[chunk['chunk_index']]
            
            self.connection.commit()
            logger.info(f"Added {len(chunks)} chunks for document {document_id}")
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Failed to add chunks: {e}")
            raise
    
    def similarity_search(
        self, 
        query_embedding: List[float], 
        top_k: int = None,
        document_id: Optional[int] = None,
        min_similarity: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Search for similar chunks using cosine similarity.
        
        Args:
            query_embedding: Query vector embedding
            top_k: Number of results to return (default from settings)
            document_id: Optional filter by document ID
            min_similarity: Minimum similarity threshold (0-1)
            
        Returns:
            List of matching chunks with similarity scores
        """
        try:
            if top_k is None:
                top_k = settings.top_k_retrieval
            
            # Convert embedding to string format for pgvector
            embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
            
            # Build query
            query = """
                SELECT 
                    dc.id,
                    dc.document_id,
                    dc.content,
                    dc.page_number,
                    dc.chunk_index,
                    dc.metadata,
                    d.filename,
                    1 - (dc.embedding <=> %s::vector) as similarity
                FROM document_chunks dc
                JOIN documents d ON dc.document_id = d.id
                WHERE 1 - (dc.embedding <=> %s::vector) >= %s
            """
            
            params = [embedding_str, embedding_str, min_similarity]
            
            if document_id:
                query += " AND dc.document_id = %s"
                params.append(document_id)
            
            query += " ORDER BY dc.embedding <=> %s::vector LIMIT %s"
            params.extend([embedding_str, top_k])
            
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            
            # Format results
            formatted_results = []
            for row in results:
                formatted_results.append({
                    'chunk_id': row[0],
                    'document_id': row[1],
                    'content': row[2],
                    'page_number': row[3],
                    'chunk_index': row[4],
                    'metadata': row[5],
                    'filename': row[6],
                    'similarity': float(row[7])
                })
            
            logger.info(f"Found {len(formatted_results)} similar chunks")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            raise
    
    def get_document_chunks(self, document_id: int) -> List[Dict[str, Any]]:
        """Get all chunks for a document.
        
        Args:
            document_id: Document ID
            
        Returns:
            List of chunks
        """
        try:
            self.cursor.execute(
                """
                SELECT id, chunk_index, content, page_number, metadata
                FROM document_chunks
                WHERE document_id = %s
                ORDER BY chunk_index
                """,
                (document_id,)
            )
            
            results = self.cursor.fetchall()
            return [
                {
                    'chunk_id': row[0],
                    'chunk_index': row[1],
                    'content': row[2],
                    'page_number': row[3],
                    'metadata': row[4]
                }
                for row in results
            ]
            
        except Exception as e:
            logger.error(f"Failed to get document chunks: {e}")
            raise
    
    def delete_document(self, document_id: int):
        """Delete a document and all its chunks.
        
        Args:
            document_id: Document ID to delete
        """
        try:
            self.cursor.execute(
                "DELETE FROM documents WHERE id = %s",
                (document_id,)
            )
            self.connection.commit()
            logger.info(f"Deleted document {document_id}")
            
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Failed to delete document: {e}")
            raise
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents.
        
        Returns:
            List of document records
        """
        try:
            self.cursor.execute(
                """
                SELECT id, filename, upload_date, total_pages, file_size, metadata
                FROM documents
                ORDER BY upload_date DESC
                """
            )
            
            results = self.cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'filename': row[1],
                    'upload_date': row[2],
                    'total_pages': row[3],
                    'file_size': row[4],
                    'metadata': row[5]
                }
                for row in results
            ]
            
        except Exception as e:
            logger.error(f"Failed to get documents: {e}")
            raise
    
    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Closed Neon DB connection")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
