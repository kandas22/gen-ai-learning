#!/usr/bin/env python3
"""
Quick database setup script to initialize Neon DB and test Neo4j connection.
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 60)
print("Database Setup & Verification")
print("=" * 60)

# 1. Test Neon DB Connection
print("\n1. Testing Neon DB Connection...")
try:
    from database.neon_vector_store import NeonVectorStore
    
    with NeonVectorStore() as vs:
        print("   ✓ Neon DB connected successfully")
        
        # Initialize schema
        print("\n2. Initializing Neon DB schema...")
        vs.initialize()
        print("   ✓ Schema initialized (documents and document_chunks tables created)")
        
except Exception as e:
    print(f"   ✗ Neon DB Error: {e}")
    print("\n   Please check your NEON_DB_URI in .env file")
    print("   Format: postgresql://user:password@host/dbname?sslmode=require")

# 2. Test Neo4j Connection
print("\n3. Testing Neo4j Connection...")
try:
    from database.neo4j_graph_store import Neo4jGraphStore
    
    with Neo4jGraphStore() as gs:
        print("   ✓ Neo4j connected successfully")
        
        # Initialize schema
        print("\n4. Initializing Neo4j schema...")
        gs.initialize()
        print("   ✓ Schema initialized (constraints and indexes created)")
        
except Exception as e:
    print(f"   ✗ Neo4j Error: {e}")
    print("\n   Troubleshooting Neo4j Connection:")
    print("   1. Check your NEO4J_URI in .env file")
    print("   2. For Neo4j Aura, use: neo4j+s://xxxxx.databases.neo4j.io")
    print("   3. Verify your NEO4J_USERNAME and NEO4J_PASSWORD")
    print("   4. Make sure your Neo4j instance is running")
    print(f"\n   Current URI: {os.getenv('NEO4J_URI', 'NOT SET')}")

print("\n" + "=" * 60)
print("Setup Complete!")
print("=" * 60)
