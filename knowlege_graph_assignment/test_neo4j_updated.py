#!/usr/bin/env python3
"""
Test Neo4j with the updated connection method
"""

import os
import sys
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("Testing Neo4j with Updated Connection Method")
print("=" * 60)

# Test 1: Direct connection
print("\n1️⃣ Testing direct Neo4j driver...")
try:
    from neo4j import GraphDatabase
    from config import settings
    
    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_username, settings.neo4j_password),
        max_connection_lifetime=3600,
        max_connection_pool_size=50,
        connection_acquisition_timeout=60
    )
    
    print(f"   ✅ Driver created for: {settings.neo4j_uri}")
    
    # Try to run a query
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            value = result.single()["test"]
            print(f"   ✅ Query successful! Returned: {value}")
            success = True
    except Exception as e:
        if "routing" in str(e).lower():
            print(f"   ⚠️  Routing issue (instance may be starting): {e}")
            success = False
        else:
            print(f"   ❌ Query failed: {e}")
            success = False
    
    driver.close()
    
except Exception as e:
    print(f"   ❌ Driver creation failed: {e}")
    success = False

# Test 2: Using Neo4jGraphStore
print("\n2️⃣ Testing Neo4jGraphStore class...")
try:
    from database.neo4j_graph_store import Neo4jGraphStore
    
    gs = Neo4jGraphStore()
    print(f"   ✅ Neo4jGraphStore initialized")
    
    # Try to use it
    try:
        gs.initialize()
        print(f"   ✅ Schema initialization successful!")
    except Exception as e:
        if "routing" in str(e).lower():
            print(f"   ⚠️  Routing issue: {e}")
        else:
            print(f"   ❌ Schema initialization failed: {e}")
    
    gs.close()
    
except Exception as e:
    print(f"   ❌ Neo4jGraphStore failed: {e}")

print("\n" + "=" * 60)
if success:
    print("✅ SUCCESS! Neo4j is working")
else:
    print("⚠️  Connection has issues - check Neo4j Aura console")
print("=" * 60)
