"""
Knowledge Graph Module using Neon PostgreSQL

This module provides:
- Entity extraction from documents using Gemini
- Relationship mapping between entities
- Neon PostgreSQL storage with pgvector
- Graph-based retrieval for enhanced RAG
"""

import os
import json
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
import psycopg2
from psycopg2.extras import execute_values
import google.generativeai as genai


@dataclass
class Entity:
    """Represents an extracted entity"""
    name: str
    entity_type: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Relationship:
    """Represents a relationship between entities"""
    source_entity: str
    target_entity: str
    relationship_type: str
    description: Optional[str] = None
    confidence: float = 1.0


class EntityExtractor:
    """Extract entities and relationships from text using Gemini"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash-latest"):
        """
        Initialize entity extractor
        
        Args:
            api_key: Gemini API key
            model_name: Gemini model to use
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key required")
        
        genai.configure(api_key=self.api_key)
        # Use model name from environment or default
        model_to_use = os.getenv('GEMINI_MODEL_NAME', 'gemini-2.0-flash-exp')
        self.model = genai.GenerativeModel(model_to_use)
        print(f"EntityExtractor using model: {model_to_use}")
        
    def extract_entities(self, text: str, max_entities: int = 20) -> List[Entity]:
        """
        Extract entities from text
        
        Args:
            text: Input text
            max_entities: Maximum number of entities to extract
            
        Returns:
            List of Entity objects
        """
        prompt = f"""Extract the key entities from the following text. 
For each entity, provide:
1. name: The entity name
2. type: The entity type (PERSON, ORGANIZATION, LOCATION, CONCEPT, TECHNOLOGY, EVENT, etc.)
3. description: A brief description

IMPORTANT: Return ONLY a valid JSON array, no other text.
Format: [{{"name": "...", "type": "...", "description": "..."}}]

Extract up to {max_entities} most important entities.

Text:
{text[:3000]}

JSON Array:"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean up the response - remove markdown code blocks
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            # Remove any leading/trailing whitespace or newlines
            result_text = result_text.strip()
            
            # Try to parse JSON
            try:
                entities_data = json.loads(result_text)
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                print(f"Response text: {result_text[:200]}...")
                # Try to find JSON array in the text
                import re
                json_match = re.search(r'\[.*\]', result_text, re.DOTALL)
                if json_match:
                    entities_data = json.loads(json_match.group())
                else:
                    print("Could not find valid JSON array in response")
                    return []
            
            # Validate it's a list
            if not isinstance(entities_data, list):
                print(f"Expected list, got {type(entities_data)}")
                return []
            
            entities = []
            for entity_dict in entities_data:
                if isinstance(entity_dict, dict) and 'name' in entity_dict:
                    entities.append(Entity(
                        name=entity_dict.get('name', ''),
                        entity_type=entity_dict.get('type', 'UNKNOWN'),
                        description=entity_dict.get('description', '')
                    ))
            
            return entities
            
        except Exception as e:
            print(f"Error extracting entities: {e}")
            return []
    
    def extract_relationships(
        self, 
        text: str, 
        entities: List[Entity],
        max_relationships: int = 15
    ) -> List[Relationship]:
        """
        Extract relationships between entities
        
        Args:
            text: Input text
            entities: List of entities to find relationships for
            max_relationships: Maximum relationships to extract
            
        Returns:
            List of Relationship objects
        """
        if not entities:
            return []
        
        entity_names = [e.name for e in entities]
        
        prompt = f"""Given the following text and list of entities, extract the relationships between them.

Entities: {', '.join(entity_names)}

For each relationship, provide:
1. source: Source entity name (must be from the entity list)
2. target: Target entity name (must be from the entity list)
3. type: Relationship type (e.g., "works_for", "located_in", "part_of", "related_to", etc.)
4. description: Brief description of the relationship

IMPORTANT: Return ONLY a valid JSON array, no other text.
Format: [{{"source": "...", "target": "...", "type": "...", "description": "..."}}]

Extract up to {max_relationships} most important relationships.

Text:
{text[:3000]}

JSON Array:"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean up the response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            # Remove any leading/trailing whitespace
            result_text = result_text.strip()
            
            # Try to parse JSON
            try:
                relationships_data = json.loads(result_text)
            except json.JSONDecodeError as e:
                print(f"JSON parse error in relationships: {e}")
                print(f"Response text: {result_text[:200]}...")
                # Try to find JSON array
                import re
                json_match = re.search(r'\[.*\]', result_text, re.DOTALL)
                if json_match:
                    relationships_data = json.loads(json_match.group())
                else:
                    print("Could not find valid JSON array in response")
                    return []
            
            # Validate it's a list
            if not isinstance(relationships_data, list):
                print(f"Expected list, got {type(relationships_data)}")
                return []
            
            relationships = []
            for rel_dict in relationships_data:
                if not isinstance(rel_dict, dict):
                    continue
                    
                source = rel_dict.get('source', '')
                target = rel_dict.get('target', '')
                
                # Only include if both entities are in our list
                if source in entity_names and target in entity_names:
                    relationships.append(Relationship(
                        source_entity=source,
                        target_entity=target,
                        relationship_type=rel_dict.get('type', 'related_to'),
                        description=rel_dict.get('description', '')
                    ))
            
            return relationships
            
        except Exception as e:
            print(f"Error extracting relationships: {e}")
            return []


class NeonKnowledgeGraph:
    """Knowledge graph using Neon PostgreSQL"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize Neon knowledge graph
        
        Args:
            connection_string: Neon database connection string
        """
        self.connection_string = connection_string or os.getenv('NEON_DATABASE_URL')
        if not self.connection_string:
            raise ValueError(
                "Neon database connection string required. "
                "Set NEON_DATABASE_URL environment variable."
            )
        
        self.conn = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(self.connection_string)
            print("✓ Connected to Neon database")
        except Exception as e:
            print(f"✗ Failed to connect to Neon: {e}")
            raise
    
    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            with self.conn.cursor() as cur:
                # Enable pgvector extension (if not already enabled)
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                
                # Entities table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS entities (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(500) UNIQUE NOT NULL,
                        entity_type VARCHAR(100),
                        description TEXT,
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # Create index on entity name
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_entity_name 
                    ON entities(name);
                """)
                
                # Relationships table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS relationships (
                        id SERIAL PRIMARY KEY,
                        source_entity VARCHAR(500) NOT NULL,
                        target_entity VARCHAR(500) NOT NULL,
                        relationship_type VARCHAR(100),
                        description TEXT,
                        confidence FLOAT DEFAULT 1.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (source_entity) REFERENCES entities(name) ON DELETE CASCADE,
                        FOREIGN KEY (target_entity) REFERENCES entities(name) ON DELETE CASCADE
                    );
                """)
                
                # Create index on relationships
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_relationships 
                    ON relationships(source_entity, target_entity);
                """)
                
                # Document-entity mapping table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS document_entities (
                        id SERIAL PRIMARY KEY,
                        document_source VARCHAR(1000) NOT NULL,
                        entity_name VARCHAR(500) NOT NULL,
                        chunk_index INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (entity_name) REFERENCES entities(name) ON DELETE CASCADE
                    );
                """)
                
                # Create index on document source
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_doc_entities 
                    ON document_entities(document_source);
                """)
                
                self.conn.commit()
                print("✓ Knowledge graph tables created/verified")
                
        except Exception as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()
            raise
    
    def add_entity(self, entity: Entity) -> bool:
        """
        Add an entity to the knowledge graph
        
        Args:
            entity: Entity to add
            
        Returns:
            True if successful
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO entities (name, entity_type, description, metadata)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (name) DO UPDATE 
                    SET entity_type = EXCLUDED.entity_type,
                        description = EXCLUDED.description,
                        metadata = EXCLUDED.metadata;
                """, (
                    entity.name,
                    entity.entity_type,
                    entity.description,
                    json.dumps(entity.metadata) if entity.metadata else None
                ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error adding entity: {e}")
            self.conn.rollback()
            return False
    
    def add_relationship(self, relationship: Relationship) -> bool:
        """
        Add a relationship to the knowledge graph
        
        Args:
            relationship: Relationship to add
            
        Returns:
            True if successful
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO relationships 
                    (source_entity, target_entity, relationship_type, description, confidence)
                    VALUES (%s, %s, %s, %s, %s);
                """, (
                    relationship.source_entity,
                    relationship.target_entity,
                    relationship.relationship_type,
                    relationship.description,
                    relationship.confidence
                ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error adding relationship: {e}")
            self.conn.rollback()
            return False
    
    def link_document_to_entities(
        self, 
        document_source: str, 
        entity_names: List[str],
        chunk_index: Optional[int] = None
    ) -> bool:
        """
        Link a document to its entities
        
        Args:
            document_source: Document source path
            entity_names: List of entity names in the document
            chunk_index: Optional chunk index
            
        Returns:
            True if successful
        """
        try:
            with self.conn.cursor() as cur:
                values = [(document_source, name, chunk_index) for name in entity_names]
                execute_values(cur, """
                    INSERT INTO document_entities (document_source, entity_name, chunk_index)
                    VALUES %s
                    ON CONFLICT DO NOTHING;
                """, values)
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error linking document to entities: {e}")
            self.conn.rollback()
            return False
    
    def get_related_entities(
        self, 
        entity_name: str, 
        max_depth: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Get entities related to a given entity
        
        Args:
            entity_name: Name of the entity
            max_depth: Maximum relationship depth to traverse
            
        Returns:
            List of related entities with relationship info
        """
        try:
            with self.conn.cursor() as cur:
                # Get direct relationships
                cur.execute("""
                    SELECT 
                        r.target_entity,
                        r.relationship_type,
                        r.description,
                        e.entity_type,
                        e.description as entity_description
                    FROM relationships r
                    JOIN entities e ON r.target_entity = e.name
                    WHERE r.source_entity = %s
                    UNION
                    SELECT 
                        r.source_entity,
                        r.relationship_type,
                        r.description,
                        e.entity_type,
                        e.description as entity_description
                    FROM relationships r
                    JOIN entities e ON r.source_entity = e.name
                    WHERE r.target_entity = %s;
                """, (entity_name, entity_name))
                
                results = cur.fetchall()
                
                related = []
                for row in results:
                    related.append({
                        'entity_name': row[0],
                        'relationship_type': row[1],
                        'relationship_description': row[2],
                        'entity_type': row[3],
                        'entity_description': row[4]
                    })
                
                return related
                
        except Exception as e:
            print(f"Error getting related entities: {e}")
            return []
    
    def get_entities_from_document(self, document_source: str) -> List[str]:
        """
        Get all entities mentioned in a document
        
        Args:
            document_source: Document source path
            
        Returns:
            List of entity names
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT DISTINCT entity_name
                    FROM document_entities
                    WHERE document_source = %s;
                """, (document_source,))
                
                return [row[0] for row in cur.fetchall()]
                
        except Exception as e:
            print(f"Error getting entities from document: {e}")
            return []
    
    def search_entities(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for entities by name or description
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of matching entities
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT name, entity_type, description
                    FROM entities
                    WHERE name ILIKE %s OR description ILIKE %s
                    LIMIT %s;
                """, (f'%{query}%', f'%{query}%', limit))
                
                results = []
                for row in cur.fetchall():
                    results.append({
                        'name': row[0],
                        'type': row[1],
                        'description': row[2]
                    })
                
                return results
                
        except Exception as e:
            print(f"Error searching entities: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get knowledge graph statistics
        
        Returns:
            Dict with entity and relationship counts
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM entities;")
                entity_count = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM relationships;")
                relationship_count = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(DISTINCT document_source) FROM document_entities;")
                document_count = cur.fetchone()[0]
                
                return {
                    'entities': entity_count,
                    'relationships': relationship_count,
                    'documents': document_count
                }
                
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {'entities': 0, 'relationships': 0, 'documents': 0}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✓ Closed Neon connection")


# Utility functions
def build_knowledge_graph_from_documents(
    documents: List[Dict[str, Any]],
    kg: NeonKnowledgeGraph,
    extractor: EntityExtractor
) -> Dict[str, int]:
    """
    Build knowledge graph from a list of documents
    
    Args:
        documents: List of document dicts with 'text' and 'source'
        kg: NeonKnowledgeGraph instance
        extractor: EntityExtractor instance
        
    Returns:
        Statistics dict
    """
    total_entities = 0
    total_relationships = 0
    
    for doc in documents:
        text = doc.get('text', '')
        source = doc.get('source', 'unknown')
        
        if not text.strip():
            continue
        
        print(f"Processing: {source}")
        
        # Extract entities
        entities = extractor.extract_entities(text)
        
        # Add entities to graph
        for entity in entities:
            kg.add_entity(entity)
        
        # Extract relationships
        relationships = extractor.extract_relationships(text, entities)
        
        # Add relationships to graph
        for rel in relationships:
            kg.add_relationship(rel)
        
        # Link document to entities
        entity_names = [e.name for e in entities]
        kg.link_document_to_entities(source, entity_names)
        
        total_entities += len(entities)
        total_relationships += len(relationships)
        
        print(f"  Extracted {len(entities)} entities, {len(relationships)} relationships")
    
    return {
        'total_entities': total_entities,
        'total_relationships': total_relationships,
        'documents_processed': len(documents)
    }
