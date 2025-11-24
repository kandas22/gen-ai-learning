"""
Graph builder that orchestrates entity extraction, relationship extraction,
and populates the Neo4j knowledge graph.
"""

import time
from typing import List, Dict, Any
from config import settings
from database.neo4j_graph_store import Neo4jGraphStore
from knowledge_graph.entity_extractor import EntityExtractor
from knowledge_graph.relationship_extractor import RelationshipExtractor
from utils.logger import get_logger

logger = get_logger(__name__)


class GraphBuilder:
    """Build knowledge graph from document chunks."""
    
    def __init__(self):
        """Initialize graph builder."""
        self.graph_store = Neo4jGraphStore()
        self.entity_extractor = EntityExtractor()
        self.relationship_extractor = RelationshipExtractor()
        
        logger.info("GraphBuilder initialized")
    
    def build_graph_for_document(
        self,
        document_id: int,
        filename: str,
        chunks: List[Dict[str, Any]],
        metadata: Dict[str, Any] = None
    ):
        """Build knowledge graph for a document.
        
        Args:
            document_id: Document ID
            filename: Document filename
            chunks: List of chunk dictionaries with 'chunk_id' and 'content'
            metadata: Optional document metadata
        """
        logger.info(f"Building knowledge graph for document: {filename}")
        
        # Create document node
        self.graph_store.add_document_node(
            document_id=document_id,
            filename=filename,
            metadata=metadata
        )
        
        # Process each chunk
        all_entities = []
        all_relationships = []
        
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}")
            
            chunk_id = chunk['chunk_id']
            content = chunk['content']
            page_number = chunk.get('page_number')
            chunk_metadata = chunk.get('metadata', {})
            
            # Create chunk node
            self.graph_store.add_chunk_node(
                chunk_id=chunk_id,
                document_id=document_id,
                content=content,
                chunk_index=chunk['chunk_index'],
                page_number=page_number,
                metadata=chunk_metadata
            )
            
            # Extract entities from chunk
            entities = self.entity_extractor.extract_entities(content)
            
            # Add entities to graph and link to chunk
            for entity in entities:
                # Add entity node
                self.graph_store.add_entity(
                    entity_name=entity['text'],
                    entity_type=entity['type'],
                    confidence=entity['confidence'],
                    context=entity.get('context'),
                    metadata={'source_chunk': chunk_id}
                )
                
                # Link chunk to entity
                self.graph_store.link_chunk_to_entity(
                    chunk_id=chunk_id,
                    entity_name=entity['text'],
                    entity_type=entity['type']
                )
            
            all_entities.extend(entities)
            
            # Extract relationships if we have entities
            if len(entities) >= 2:
                relationships = self.relationship_extractor.extract_relationships(
                    text=content,
                    entities=entities
                )
                
                # Add relationships to graph
                for rel in relationships:
                    # Find entity types
                    source_type = self._find_entity_type(rel['source'], entities)
                    target_type = self._find_entity_type(rel['target'], entities)
                    
                    if source_type and target_type:
                        self.graph_store.add_entity_relationship(
                            source_entity=rel['source'],
                            source_type=source_type,
                            target_entity=rel['target'],
                            target_type=target_type,
                            relationship_type=rel['relationship'],
                            confidence=rel['confidence'],
                            evidence=rel.get('evidence')
                        )
                
                all_relationships.extend(relationships)
            
            # Rate limiting for Gemini API
            # gemini-1.5-flash has higher limits (15 RPM free, 1000 RPM paid)
            # 2s delay = ~30 requests/minute, safe for most tiers
            if settings.llm_provider == "google":
                logger.info("Waiting 6s to respect Gemini API rate limits...")
                time.sleep(6)
        
        # Deduplicate entities and relationships
        unique_entities = self.entity_extractor.deduplicate_entities(all_entities)
        unique_relationships = self.relationship_extractor.deduplicate_relationships(all_relationships)
        
        logger.info(
            f"Graph built: {len(unique_entities)} unique entities, "
            f"{len(unique_relationships)} unique relationships"
        )
        
        return {
            'entities': unique_entities,
            'relationships': unique_relationships
        }
    
    def _find_entity_type(
        self,
        entity_name: str,
        entities: List[Dict[str, Any]]
    ) -> str:
        """Find entity type by name.
        
        Args:
            entity_name: Entity name to find
            entities: List of entities
            
        Returns:
            Entity type or None
        """
        for entity in entities:
            if entity['text'].lower() == entity_name.lower():
                return entity['type']
        return None
    
    def close(self):
        """Close graph store connection."""
        self.graph_store.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
