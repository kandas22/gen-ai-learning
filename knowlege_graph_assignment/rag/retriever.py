"""
Hybrid retriever combining vector search and graph traversal.
Retrieves relevant chunks using both methods and fuses results.
"""

from typing import List, Dict, Any
from database.neon_vector_store import NeonVectorStore
from database.neo4j_graph_store import Neo4jGraphStore
from processing.embeddings import EmbeddingGenerator
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class HybridRetriever:
    """Hybrid retrieval using vector search and knowledge graph."""
    
    def __init__(self):
        """Initialize hybrid retriever."""
        self.vector_store = NeonVectorStore()
        self.graph_store = Neo4jGraphStore()
        self.embedding_generator = EmbeddingGenerator()
        
        self.vector_weight = settings.vector_retrieval_weight
        self.graph_weight = settings.graph_retrieval_weight
        self.top_k = settings.top_k_retrieval
        
        logger.info(
            f"HybridRetriever initialized: vector_weight={self.vector_weight}, "
            f"graph_weight={self.graph_weight}"
        )
    
    def retrieve(
        self,
        query: str,
        top_k: int = None,
        use_graph: bool = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks for a query.
        
        Args:
            query: Search query
            top_k: Number of results to return (default from settings)
            use_graph: Whether to use graph retrieval (default from settings)
            
        Returns:
            List of retrieved chunks with scores
        """
        if top_k is None:
            top_k = self.top_k
        
        if use_graph is None:
            use_graph = settings.enable_graph_retrieval
        
        logger.info(f"Retrieving for query: {query[:100]}...")
        
        # Vector retrieval
        vector_results = self._vector_retrieve(query, top_k)
        
        # Graph retrieval (if enabled)
        graph_results = []
        if use_graph:
            graph_results = self._graph_retrieve(query, vector_results, top_k)
        
        # Fuse results
        fused_results = self._fuse_results(vector_results, graph_results, top_k)
        
        logger.info(f"Retrieved {len(fused_results)} chunks")
        return fused_results
    
    def _vector_retrieve(
        self,
        query: str,
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Retrieve using vector similarity search.
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            List of chunks with similarity scores
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_query_embedding(query)
            
            # Search vector store
            results = self.vector_store.similarity_search(
                query_embedding=query_embedding,
                top_k=top_k,
                min_similarity=settings.min_confidence_threshold
            )
            
            # Add retrieval source
            for result in results:
                result['retrieval_source'] = 'vector'
                result['score'] = result['similarity']
            
            logger.info(f"Vector retrieval found {len(results)} chunks")
            return results
            
        except Exception as e:
            logger.error(f"Vector retrieval failed: {e}")
            return []
    
    def _graph_retrieve(
        self,
        query: str,
        vector_results: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Retrieve using knowledge graph traversal.
        
        Args:
            query: Search query
            vector_results: Results from vector search (to extract entities)
            top_k: Number of results
            
        Returns:
            List of chunks from graph traversal
        """
        try:
            # Extract entity names from query (simple keyword extraction)
            # In production, use NER on the query
            query_words = query.split()
            entity_candidates = [w for w in query_words if len(w) > 3]
            
            # Also get entities from top vector results
            if vector_results:
                # Get entities mentioned in top results
                top_chunks = vector_results[:3]
                chunk_ids = [r['chunk_id'] for r in top_chunks]
                
                # Find entities related to these chunks
                graph_context = self.graph_store.get_graph_context(entity_candidates)
                
                # Get chunks that mention these entities
                graph_chunks = []
                for entity in graph_context.get('entities', []):
                    entity_chunks = self.graph_store.find_chunks_by_entity(
                        entity_name=entity['name'],
                        entity_type=entity['type']
                    )
                    graph_chunks.extend(entity_chunks)
                
                # Remove duplicates and add scores
                seen_ids = set()
                unique_chunks = []
                for chunk in graph_chunks:
                    if chunk['chunk_id'] not in seen_ids:
                        seen_ids.add(chunk['chunk_id'])
                        chunk['retrieval_source'] = 'graph'
                        chunk['score'] = 0.7  # Default graph score
                        unique_chunks.append(chunk)
                
                logger.info(f"Graph retrieval found {len(unique_chunks)} chunks")
                return unique_chunks[:top_k]
            
            return []
            
        except Exception as e:
            logger.error(f"Graph retrieval failed: {e}")
            return []
    
    def _fuse_results(
        self,
        vector_results: List[Dict[str, Any]],
        graph_results: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Fuse vector and graph results using weighted scoring.
        
        Args:
            vector_results: Results from vector search
            graph_results: Results from graph search
            top_k: Number of final results
            
        Returns:
            Fused and ranked results
        """
        # Create a dictionary to merge results by chunk_id
        merged = {}
        
        # Add vector results with weight
        for result in vector_results:
            chunk_id = result['chunk_id']
            merged[chunk_id] = result.copy()
            merged[chunk_id]['final_score'] = result['score'] * self.vector_weight
            merged[chunk_id]['sources'] = ['vector']
        
        # Add/merge graph results with weight
        for result in graph_results:
            chunk_id = result['chunk_id']
            if chunk_id in merged:
                # Chunk found in both - combine scores
                merged[chunk_id]['final_score'] += result['score'] * self.graph_weight
                merged[chunk_id]['sources'].append('graph')
            else:
                # New chunk from graph only
                merged[chunk_id] = result.copy()
                merged[chunk_id]['final_score'] = result['score'] * self.graph_weight
                merged[chunk_id]['sources'] = ['graph']
        
        # Sort by final score
        sorted_results = sorted(
            merged.values(),
            key=lambda x: x['final_score'],
            reverse=True
        )
        
        # Return top-k
        return sorted_results[:top_k]
    
    def close(self):
        """Close database connections."""
        self.vector_store.close()
        self.graph_store.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
