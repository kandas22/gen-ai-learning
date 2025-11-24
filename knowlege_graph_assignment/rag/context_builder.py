"""
Context builder that aggregates retrieved chunks into coherent context.
Removes duplicates, orders by relevance, and formats for LLM consumption.
"""

from typing import List, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)


class ContextBuilder:
    """Build context from retrieved chunks."""
    
    def __init__(self, max_context_length: int = 4000):
        """Initialize context builder.
        
        Args:
            max_context_length: Maximum context length in characters
        """
        self.max_context_length = max_context_length
        logger.info(f"ContextBuilder initialized: max_length={max_context_length}")
    
    def build_context(
        self,
        retrieved_chunks: List[Dict[str, Any]],
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """Build context from retrieved chunks.
        
        Args:
            retrieved_chunks: List of retrieved chunk dictionaries
            include_metadata: Whether to include source metadata
            
        Returns:
            Dictionary with formatted context and metadata
        """
        if not retrieved_chunks:
            return {
                'context': '',
                'sources': [],
                'total_chunks': 0,
                'total_chars': 0
            }
        
        # Remove duplicates by chunk_id
        unique_chunks = self._deduplicate_chunks(retrieved_chunks)
        
        # Sort by score (already sorted, but ensure)
        sorted_chunks = sorted(
            unique_chunks,
            key=lambda x: x.get('final_score', x.get('score', 0)),
            reverse=True
        )
        
        # Build context within token limit
        context_parts = []
        sources = []
        total_chars = 0
        
        for i, chunk in enumerate(sorted_chunks):
            content = chunk['content']
            chunk_length = len(content)
            
            # Check if adding this chunk would exceed limit
            if total_chars + chunk_length > self.max_context_length:
                # Try to fit partial content
                remaining = self.max_context_length - total_chars
                if remaining > 200:  # Only add if meaningful amount left
                    content = content[:remaining] + "..."
                    chunk_length = len(content)
                else:
                    break
            
            # Add chunk to context
            if include_metadata:
                source_info = self._format_source(chunk, i + 1)
                context_parts.append(f"[Source {i+1}]\n{content}\n")
                sources.append(source_info)
            else:
                context_parts.append(content)
            
            total_chars += chunk_length
            
            # Stop if we've reached the limit
            if total_chars >= self.max_context_length:
                break
        
        # Join context parts
        context = "\n\n".join(context_parts)
        
        result = {
            'context': context,
            'sources': sources,
            'total_chunks': len(context_parts),
            'total_chars': total_chars
        }
        
        logger.info(
            f"Built context: {result['total_chunks']} chunks, "
            f"{result['total_chars']} characters"
        )
        
        return result
    
    def _deduplicate_chunks(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate chunks by ID.
        
        Args:
            chunks: List of chunks
            
        Returns:
            Deduplicated list
        """
        seen_ids = set()
        unique = []
        
        for chunk in chunks:
            chunk_id = chunk.get('chunk_id')
            if chunk_id and chunk_id not in seen_ids:
                seen_ids.add(chunk_id)
                unique.append(chunk)
            elif not chunk_id:
                # No ID, check content similarity
                unique.append(chunk)
        
        return unique
    
    def _format_source(
        self,
        chunk: Dict[str, Any],
        source_num: int
    ) -> Dict[str, Any]:
        """Format source metadata.
        
        Args:
            chunk: Chunk dictionary
            source_num: Source number
            
        Returns:
            Formatted source info
        """
        return {
            'source_number': source_num,
            'filename': chunk.get('filename', 'Unknown'),
            'page_number': chunk.get('page_number'),
            'chunk_id': chunk.get('chunk_id'),
            'score': chunk.get('final_score', chunk.get('score', 0)),
            'retrieval_sources': chunk.get('sources', [chunk.get('retrieval_source', 'unknown')])
        }
    
    def build_graph_context(
        self,
        graph_data: Dict[str, Any]
    ) -> str:
        """Build context from knowledge graph data.
        
        Args:
            graph_data: Graph context with entities and relationships
            
        Returns:
            Formatted graph context string
        """
        if not graph_data:
            return ""
        
        parts = []
        
        # Add entities
        entities = graph_data.get('entities', [])
        if entities:
            entity_strs = [
                f"- {e['name']} ({e['type']})"
                for e in entities[:10]  # Limit to top 10
            ]
            parts.append("Relevant Entities:\n" + "\n".join(entity_strs))
        
        # Add relationships
        relationships = graph_data.get('relationships', [])
        if relationships:
            rel_strs = [
                f"- {r['source']} {r['type']} {r['target']}"
                for r in relationships[:10]  # Limit to top 10
            ]
            parts.append("Relationships:\n" + "\n".join(rel_strs))
        
        return "\n\n".join(parts)
    
    def format_sources_for_display(
        self,
        sources: List[Dict[str, Any]]
    ) -> str:
        """Format sources for user display.
        
        Args:
            sources: List of source dictionaries
            
        Returns:
            Formatted string
        """
        if not sources:
            return "No sources available"
        
        formatted = []
        for source in sources:
            page_info = f"Page {source['page_number']}" if source.get('page_number') else "Unknown page"
            score_info = f"(relevance: {source['score']:.2f})"
            
            formatted.append(
                f"{source['source_number']}. {source['filename']} - {page_info} {score_info}"
            )
        
        return "\n".join(formatted)
