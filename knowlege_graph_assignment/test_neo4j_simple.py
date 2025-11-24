#!/usr/bin/env python3
"""
Simple Neo4j connection test without database parameter
"""

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

print("Testing Neo4j Connection...")
print(f"URI: {uri}")
print(f"Username: {username}")

try:
    # Create driver
    driver = GraphDatabase.driver(uri, auth=(username, password))
    
    # Test 1: Verify connectivity (this is what fails)
    print("\n1. Testing verify_connectivity()...")
    try:
        driver.verify_connectivity()
        print("   ✅ verify_connectivity() passed")
    except Exception as e:
        print(f"   ❌ verify_connectivity() failed: {e}")
    
    # Test 2: Try session without database parameter
    print("\n2. Testing session WITHOUT database parameter...")
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            value = result.single()["test"]
            print(f"   ✅ Session works! Got value: {value}")
    except Exception as e:
        print(f"   ❌ Session failed: {e}")
    
    # Test 3: Try session WITH database parameter
    print("\n3. Testing session WITH database='neo4j'...")
    try:
        with driver.session(database="neo4j") as session:
            result = session.run("RETURN 1 as test")
            value = result.single()["test"]
            print(f"   ✅ Session with database works! Got value: {value}")
    except Exception as e:
        print(f"   ❌ Session with database failed: {e}")
    
    driver.close()
    print("\n✅ At least one method worked!")
    
except Exception as e:
    print(f"\n❌ Complete failure: {e}")
