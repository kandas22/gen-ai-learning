#!/usr/bin/env python3
"""
Test Neo4j connection exactly as you described
"""

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

print(f"Testing connection to: {uri}")
print(f"Username: {username}")
print()

try:
    # Create driver - exactly as you might be doing
    driver = GraphDatabase.driver(uri, auth=(username, password))
    
    print(f"✅ Connected to {uri}")
    
    # Try to run a simple query
    with driver.session() as session:
        result = session.run("RETURN 1 as num")
        value = result.single()["num"]
        print(f"✅ Query successful! Returned: {value}")
    
    driver.close()
    print("\n🎉 Connection is working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
