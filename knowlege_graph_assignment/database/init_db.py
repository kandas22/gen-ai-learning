"""
Database initialization script.
Sets up Neon DB and Neo4j schemas.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from database.neon_vector_store import NeonVectorStore
from database.neo4j_graph_store import Neo4jGraphStore
from utils.logger import get_logger
from config import settings

logger = get_logger(__name__)


def init_neon_db():
    """Initialize Neon DB schema."""
    logger.info("Initializing Neon DB...")
    try:
        with NeonVectorStore() as vector_store:
            vector_store.initialize()
        logger.info("✓ Neon DB initialized successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to initialize Neon DB: {e}")
        return False


def init_neo4j():
    """Initialize Neo4j schema."""
    logger.info("Initializing Neo4j...")
    try:
        with Neo4jGraphStore() as graph_store:
            graph_store.initialize()
        logger.info("✓ Neo4j initialized successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to initialize Neo4j: {e}")
        return False


def verify_connections():
    """Verify database connections."""
    logger.info("Verifying database connections...")
    
    # Test Neon DB
    try:
        with NeonVectorStore() as vector_store:
            logger.info("✓ Neon DB connection verified")
    except Exception as e:
        logger.error(f"✗ Neon DB connection failed: {e}")
        return False
    
    # Test Neo4j
    try:
        with Neo4jGraphStore() as graph_store:
            logger.info("✓ Neo4j connection verified")
    except Exception as e:
        logger.error(f"✗ Neo4j connection failed: {e}")
        return False
    
    return True


def main():
    """Main initialization function."""
    print("=" * 60)
    print("RAG System Database Initialization")
    print("=" * 60)
    print()
    
    print(f"Environment: {settings.environment}")
    print(f"LLM Provider: {settings.llm_provider}")
    print(f"Embedding Dimension: {settings.embedding_dimension}")
    print(f"Vector Index Type: {settings.vector_index_type}")
    print()
    
    # Verify connections first
    if not verify_connections():
        print("\n✗ Connection verification failed. Please check your .env configuration.")
        sys.exit(1)
    
    print()
    
    # Initialize Neon DB
    neon_success = init_neon_db()
    
    # Initialize Neo4j
    neo4j_success = init_neo4j()
    
    print()
    print("=" * 60)
    
    if neon_success and neo4j_success:
        print("✓ All databases initialized successfully!")
        print()
        print("Next steps:")
        print("1. Run the Streamlit app: streamlit run ui/app.py")
        print("2. Upload PDF documents")
        print("3. Start asking questions!")
    else:
        print("✗ Database initialization failed. Please check the logs.")
        sys.exit(1)
    
    print("=" * 60)


if __name__ == "__main__":
    main()
