"""
Neo4j Graph Store implementation.
Handles knowledge graph storage, entity/relationship management, and graph queries.
"""

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, SessionExpired, TransientError
from typing import List, Dict, Any, Optional
import time
import functools
import json
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


def retry_neo4j_operation(max_retries=3, initial_delay=1):
    """Decorator to retry Neo4j operations on transient errors."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ServiceUnavailable, SessionExpired, TransientError) as e:
                    last_exception = e
                    logger.warning(
                        f"Neo4j operation failed (attempt {attempt + 1}/{max_retries}): {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                except Exception as e:
                    # Check for routing errors in message string if exception type doesn't match
                    if "Unable to retrieve routing information" in str(e):
                        last_exception = e
                        logger.warning(
                            f"Neo4j routing error (attempt {attempt + 1}/{max_retries}): {e}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                        delay *= 2
                    else:
                        raise e
            
            logger.error(f"Neo4j operation failed after {max_retries} attempts")
            raise last_exception
        return wrapper
    return decorator


class Neo4jGraphStore:
    """Knowledge graph store using Neo4j."""
    
    # Singleton driver instance
    _driver_instance = None
    
    def __init__(self):
        """Initialize Neo4j connection."""
        self._connect()
    
    def _connect(self):
        """Establish connection to Neo4j using singleton driver."""
        if Neo4jGraphStore._driver_instance is None:
            try:
                # Configure driver with more robust settings for Aura
                Neo4jGraphStore._driver_instance = GraphDatabase.driver(
                    settings.neo4j_uri,
                    auth=(settings.neo4j_username, settings.neo4j_password),
                    max_connection_lifetime=200,  # Shorter lifetime to avoid stale connections
                    max_connection_pool_size=50,
                    connection_acquisition_timeout=120,  # Longer timeout to wait for connection
                    keep_alive=True  # Enable TCP keep-alive
                )
                logger.info("Neo4j driver initialized successfully (Singleton)")
            except Exception as e:
                logger.error(f"Failed to initialize Neo4j driver: {e}")
                raise
        
        # Use the singleton instance
        self.driver = Neo4jGraphStore._driver_instance
    
    @retry_neo4j_operation(max_retries=5, initial_delay=2)
    def initialize(self):
        """Initialize graph schema with constraints and indexes."""
        try:
            with self.driver.session(database=settings.neo4j_database) as session:
                # Create constraints for unique nodes
                constraints = [
                    "CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
                    "CREATE CONSTRAINT chunk_id IF NOT EXISTS FOR (c:Chunk) REQUIRE c.id IS UNIQUE",
                    "CREATE CONSTRAINT entity_name IF NOT EXISTS FOR (e:Entity) REQUIRE (e.name, e.type) IS UNIQUE",
                ]
                
                for constraint in constraints:
                    try:
                        session.run(constraint)
                    except Exception as e:
                        # Constraint might already exist
                        logger.debug(f"Constraint creation note: {e}")
                
                # Create indexes for performance
                indexes = [
                    "CREATE INDEX entity_type_idx IF NOT EXISTS FOR (e:Entity) ON (e.type)",
                    "CREATE INDEX chunk_document_idx IF NOT EXISTS FOR (c:Chunk) ON (c.document_id)",
                ]
                
                for index in indexes:
                    try:
                        session.run(index)
                    except Exception as e:
                        logger.debug(f"Index creation note: {e}")
                
                logger.info("Neo4j schema initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j schema: {e}")
            raise
    
    @retry_neo4j_operation(max_retries=3, initial_delay=1)
    def add_document_node(
        self, 
        document_id: int, 
        filename: str, 
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Create a document node.
        
        Args:
            document_id: Unique document ID
            filename: Document filename
            metadata: Optional metadata dictionary
        """
        try:
            # Serialize metadata to JSON string to avoid Neo4j type errors with nested dicts
            metadata_str = json.dumps(metadata) if metadata else "{}"
            
            with self.driver.session(database=settings.neo4j_database) as session:
                session.run(
                    """
                    MERGE (d:Document {id: $document_id})
                    SET d.filename = $filename,
                        d.created_at = datetime(),
                        d.metadata = $metadata
                    """,
                    document_id=document_id,
                    filename=filename,
                    metadata=metadata_str
                )
                logger.info(f"Added document node: {filename} (ID: {document_id})")
                
        except Exception as e:
            logger.error(f"Failed to add document node: {e}")
            raise
    
    @retry_neo4j_operation(max_retries=3, initial_delay=1)
    def add_chunk_node(
        self,
        chunk_id: int,
        document_id: int,
        content: str,
        chunk_index: int,
        page_number: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Create a chunk node and link to document.
        
        Args:
            chunk_id: Unique chunk ID
            document_id: Parent document ID
            content: Chunk text content
            chunk_index: Index of chunk in document
            page_number: Optional page number
            metadata: Optional metadata
        """
        try:
            # Serialize metadata to JSON string
            metadata_str = json.dumps(metadata) if metadata else "{}"
            
            with self.driver.session(database=settings.neo4j_database) as session:
                session.run(
                    """
                    MATCH (d:Document {id: $document_id})
                    MERGE (c:Chunk {id: $chunk_id})
                    SET c.content = $content,
                        c.chunk_index = $chunk_index,
                        c.page_number = $page_number,
                        c.document_id = $document_id,
                        c.metadata = $metadata
                    MERGE (d)-[:CONTAINS]->(c)
                    """,
                    chunk_id=chunk_id,
                    document_id=document_id,
                    content=content,
                    chunk_index=chunk_index,
                    page_number=page_number,
                    metadata=metadata_str
                )
                
        except Exception as e:
            logger.error(f"Failed to add chunk node: {e}")
            raise
    
    @retry_neo4j_operation(max_retries=3, initial_delay=1)
    def add_entity(
        self,
        entity_name: str,
        entity_type: str,
        confidence: float,
        context: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Create or update an entity node.
        
        Args:
            entity_name: Name of the entity
            entity_type: Type of entity (PERSON, ORGANIZATION, etc.)
            confidence: Confidence score (0-1)
            context: Optional context text
            metadata: Optional metadata
        """
        try:
            # Serialize metadata to JSON string
            metadata_str = json.dumps(metadata) if metadata else "{}"
            
            with self.driver.session(database=settings.neo4j_database) as session:
                session.run(
                    """
                    MERGE (e:Entity {name: $name, type: $type})
                    SET e.confidence = $confidence,
                        e.context = $context,
                        e.metadata = $metadata,
                        e.updated_at = datetime()
                    """,
                    name=entity_name,
                    type=entity_type,
                    confidence=confidence,
                    context=context,
                    metadata=metadata_str
                )
                
        except Exception as e:
            logger.error(f"Failed to add entity: {e}")
            raise
    
    @retry_neo4j_operation(max_retries=3, initial_delay=1)
    def link_chunk_to_entity(
        self,
        chunk_id: int,
        entity_name: str,
        entity_type: str,
        relationship_type: str = "MENTIONS"
    ):
        """Create relationship between chunk and entity.
        
        Args:
            chunk_id: Chunk ID
            entity_name: Entity name
            entity_type: Entity type
            relationship_type: Type of relationship (default: MENTIONS)
        """
        try:
            with self.driver.session(database=settings.neo4j_database) as session:
                session.run(
                    f"""
                    MATCH (c:Chunk {{id: $chunk_id}})
                    MATCH (e:Entity {{name: $name, type: $type}})
                    MERGE (c)-[r:{relationship_type}]->(e)
                    SET r.created_at = datetime()
                    """,
                    chunk_id=chunk_id,
                    name=entity_name,
                    type=entity_type
                )
                
        except Exception as e:
            logger.error(f"Failed to link chunk to entity: {e}")
            raise
    
    @retry_neo4j_operation(max_retries=3, initial_delay=1)
    def add_entity_relationship(
        self,
        source_entity: str,
        source_type: str,
        target_entity: str,
        target_type: str,
        relationship_type: str,
        confidence: float,
        evidence: Optional[str] = None
    ):
        """Create relationship between two entities.
        
        Args:
            source_entity: Source entity name
            source_type: Source entity type
            target_entity: Target entity name
            target_type: Target entity type
            relationship_type: Type of relationship
            confidence: Confidence score (0-1)
            evidence: Optional evidence text
        """
        try:
            with self.driver.session(database=settings.neo4j_database) as session:
                session.run(
                    f"""
                    MATCH (s:Entity {{name: $source_name, type: $source_type}})
                    MATCH (t:Entity {{name: $target_name, type: $target_type}})
                    MERGE (s)-[r:{relationship_type}]->(t)
                    SET r.confidence = $confidence,
                        r.evidence = $evidence,
                        r.created_at = datetime()
                    """,
                    source_name=source_entity,
                    source_type=source_type,
                    target_name=target_entity,
                    target_type=target_type,
                    confidence=confidence,
                    evidence=evidence
                )
                
        except Exception as e:
            logger.error(f"Failed to add entity relationship: {e}")
            raise
    
    @retry_neo4j_operation(max_retries=3, initial_delay=1)
    def find_related_entities(
        self,
        entity_name: str,
        entity_type: str,
        max_depth: int = None
    ) -> List[Dict[str, Any]]:
        """Find entities related to a given entity.
        
        Args:
            entity_name: Entity name to search from
            entity_type: Entity type
            max_depth: Maximum traversal depth (default from settings)
            
        Returns:
            List of related entities with relationship info
        """
        try:
            if max_depth is None:
                max_depth = settings.graph_traversal_depth
            
            with self.driver.session(database=settings.neo4j_database) as session:
                result = session.run(
                    """
                    MATCH path = (e1:Entity {name: $name, type: $type})-[*1..%d]-(e2:Entity)
                    RETURN DISTINCT e2.name as name, 
                           e2.type as type, 
                           e2.confidence as confidence,
                           length(path) as distance
                    ORDER BY distance, e2.confidence DESC
                    LIMIT 20
                    """ % max_depth,
                    name=entity_name,
                    type=entity_type
                )
                
                entities = []
                for record in result:
                    entities.append({
                        'name': record['name'],
                        'type': record['type'],
                        'confidence': record['confidence'],
                        'distance': record['distance']
                    })
                
                return entities
                
        except Exception as e:
            logger.error(f"Failed to find related entities: {e}")
            raise
    
    @retry_neo4j_operation(max_retries=3, initial_delay=1)
    def find_chunks_by_entity(
        self,
        entity_name: str,
        entity_type: str
    ) -> List[Dict[str, Any]]:
        """Find all chunks that mention an entity.
        
        Args:
            entity_name: Entity name
            entity_type: Entity type
            
        Returns:
            List of chunks mentioning the entity
        """
        try:
            with self.driver.session(database=settings.neo4j_database) as session:
                result = session.run(
                    """
                    MATCH (c:Chunk)-[:MENTIONS]->(e:Entity {name: $name, type: $type})
                    MATCH (d:Document)-[:CONTAINS]->(c)
                    RETURN c.id as chunk_id,
                           c.content as content,
                           c.page_number as page_number,
                           d.filename as filename,
                           d.id as document_id
                    ORDER BY c.chunk_index
                    """,
                    name=entity_name,
                    type=entity_type
                )
                
                chunks = []
                for record in result:
                    chunks.append({
                        'chunk_id': record['chunk_id'],
                        'content': record['content'],
                        'page_number': record['page_number'],
                        'filename': record['filename'],
                        'document_id': record['document_id']
                    })
                
                return chunks
                
        except Exception as e:
            logger.error(f"Failed to find chunks by entity: {e}")
            raise
    
    @retry_neo4j_operation(max_retries=3, initial_delay=1)
    def get_graph_context(
        self,
        entity_names: List[str]
    ) -> Dict[str, Any]:
        """Get graph context for multiple entities.
        
        Args:
            entity_names: List of entity names to explore
            
        Returns:
            Dictionary with entities, relationships, and chunks
        """
        try:
            entities = []
            relationships = []
            chunks = []
            
            with self.driver.session(database=settings.neo4j_database) as session:
                for entity_name in entity_names:
                    # Find entity and its relationships
                    result = session.run(
                        """
                        MATCH (e:Entity)
                        WHERE e.name CONTAINS $name
                        OPTIONAL MATCH (e)-[r]-(other:Entity)
                        RETURN e, collect({rel: type(r), entity: other}) as connections
                        LIMIT 5
                        """,
                        name=entity_name
                    )
                    
                    for record in result:
                        entity = record['e']
                        entities.append({
                            'name': entity['name'],
                            'type': entity['type'],
                            'confidence': entity.get('confidence', 0)
                        })
                        
                        for conn in record['connections']:
                            if conn['entity']:
                                relationships.append({
                                    'source': entity['name'],
                                    'target': conn['entity']['name'],
                                    'type': conn['rel']
                                })
            
            return {
                'entities': entities,
                'relationships': relationships,
                'chunks': chunks
            }
            
        except Exception as e:
            logger.error(f"Failed to get graph context: {e}")
            raise
    
    def delete_document(self, document_id: int):
        """Delete a document and all related nodes.
        
        Args:
            document_id: Document ID to delete
        """
        try:
            with self.driver.session(database=settings.neo4j_database) as session:
                session.run(
                    """
                    MATCH (d:Document {id: $document_id})
                    OPTIONAL MATCH (d)-[:CONTAINS]->(c:Chunk)
                    DETACH DELETE d, c
                    """,
                    document_id=document_id
                )
                logger.info(f"Deleted document {document_id} from graph")
                
        except Exception as e:
            logger.error(f"Failed to delete document from graph: {e}")
            raise
    
    def close(self):
        """Close Neo4j connection.
        
        Note: With singleton pattern, we don't close the driver here.
        The driver should remain open for the application lifecycle.
        """
        pass
        
    @classmethod
    def close_driver(cls):
        """Explicitly close the singleton driver."""
        if cls._driver_instance:
            cls._driver_instance.close()
            cls._driver_instance = None
            logger.info("Closed Neo4j singleton driver")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
