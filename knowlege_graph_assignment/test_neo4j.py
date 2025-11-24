#!/usr/bin/env python3
"""
Neo4j Connection Diagnostic Tool
Tests Neo4j connection with detailed error information
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("Neo4j Connection Diagnostic")
print("=" * 70)

# Get credentials from environment
neo4j_uri = os.getenv('NEO4J_URI')
neo4j_username = os.getenv('NEO4J_USERNAME')
neo4j_password = os.getenv('NEO4J_PASSWORD')

print(f"\n📋 Configuration:")
print(f"   URI: {neo4j_uri}")
print(f"   Username: {neo4j_username}")
print(f"   Password: {'*' * len(neo4j_password) if neo4j_password else 'NOT SET'}")

# Test 1: Check if credentials are set
print(f"\n1️⃣ Checking credentials...")
if not neo4j_uri:
    print("   ❌ NEO4J_URI is not set")
    exit(1)
if not neo4j_username:
    print("   ❌ NEO4J_USERNAME is not set")
    exit(1)
if not neo4j_password:
    print("   ❌ NEO4J_PASSWORD is not set")
    exit(1)
print("   ✅ All credentials are set")

# Test 2: Try to connect
print(f"\n2️⃣ Attempting connection...")
try:
    from neo4j import GraphDatabase
    
    driver = GraphDatabase.driver(
        neo4j_uri,
        auth=(neo4j_username, neo4j_password)
    )
    
    # Verify connection
    print("   🔄 Verifying connection...")
    driver.verify_connectivity()
    
    print("   ✅ Connection successful!")
    
    # Test 3: Run a simple query
    print(f"\n3️⃣ Testing query execution...")
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        record = result.single()
        if record["test"] == 1:
            print("   ✅ Query execution successful!")
    
    # Test 4: Get database info
    print(f"\n4️⃣ Database information...")
    with driver.session() as session:
        # Get node count
        result = session.run("MATCH (n) RETURN count(n) as count")
        node_count = result.single()["count"]
        print(f"   📊 Total nodes: {node_count}")
        
        # Get relationship count
        result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
        rel_count = result.single()["count"]
        print(f"   📊 Total relationships: {rel_count}")
    
    driver.close()
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Neo4j is working correctly")
    print("=" * 70)
    print("\n💡 Your Neo4j connection is fine. The app should work now.")
    
except Exception as e:
    error_msg = str(e)
    print(f"   ❌ Connection failed!")
    print(f"\n📝 Error Details:")
    print(f"   {error_msg}")
    
    print("\n" + "=" * 70)
    print("🔧 Troubleshooting Steps:")
    print("=" * 70)
    
    if "Unable to retrieve routing information" in error_msg:
        print("""
1. Your Neo4j Aura instance might be PAUSED or STOPPED
   → Go to: https://console.neo4j.io/
   → Find instance: 42ec2f49
   → Click 'Resume' if it's paused
   
2. Check if the instance is still active
   → Free tier instances may expire after inactivity
   
3. Verify your password
   → You can reset it in the Neo4j console
   → Update NEO4J_PASSWORD in .env file
        """)
    elif "authentication" in error_msg.lower():
        print("""
1. Password is incorrect
   → Go to: https://console.neo4j.io/
   → Reset your password
   → Update NEO4J_PASSWORD in .env file
        """)
    elif "network" in error_msg.lower() or "timeout" in error_msg.lower():
        print("""
1. Network/Firewall issue
   → Check your internet connection
   → Try from a different network
   → Check if port 7687 is blocked
        """)
    else:
        print("""
1. Check Neo4j Aura console: https://console.neo4j.io/
2. Verify instance is running
3. Reset password if needed
4. Check .env file has correct credentials
        """)
    
    print("\n💡 Alternative: Use local Neo4j")
    print("   Install Neo4j Desktop and use:")
    print("   NEO4J_URI=bolt://localhost:7687")
    print("   NEO4J_USERNAME=neo4j")
    print("   NEO4J_PASSWORD=your_local_password")
