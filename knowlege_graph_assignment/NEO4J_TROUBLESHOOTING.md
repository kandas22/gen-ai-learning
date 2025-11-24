# Neo4j Connection Troubleshooting Guide

## Current Issue
❌ **Error**: "Unable to retrieve routing information"

## Possible Causes & Solutions

### 1. **Neo4j Aura Instance Not Active**
Your Neo4j Aura instance might be paused or stopped.

**Solution:**
1. Go to https://console.neo4j.io/
2. Check if your instance `42ec2f49` is **Running**
3. If paused, click **Resume** to start it

### 2. **Incorrect Password**
The password in your `.env` file might be incorrect.

**Solution:**
1. Go to https://console.neo4j.io/
2. Select your instance
3. Reset the password if needed
4. Update `NEO4J_PASSWORD` in your `.env` file

### 3. **Network/Firewall Issues**
Your network might be blocking the connection.

**Solution:**
- Try from a different network
- Check if your firewall is blocking port 7687

### 4. **Temporary Workaround: Disable Neo4j**
If you want to test the system without Neo4j:

**Option A: Make Neo4j Optional in the App**
Edit `ui/app.py` to handle Neo4j connection failures gracefully.

**Option B: Use Local Neo4j**
Install Neo4j Desktop and use:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_local_password
```

## Quick Test Commands

### Test Neon DB Only:
```bash
python -c "from database.neon_vector_store import NeonVectorStore; vs = NeonVectorStore(); print('✓ Connected'); vs.close()"
```

### Test Neo4j:
```bash
python -c "from database.neo4j_graph_store import Neo4jGraphStore; gs = Neo4jGraphStore(); print('✓ Connected'); gs.close()"
```

## Current Configuration
- **Neo4j URI**: `neo4j+s://42ec2f49.databases.neo4j.io`
- **Instance ID**: `42ec2f49`
- **Type**: Neo4j Aura (Cloud)

## Next Steps
1. ✅ Neon DB is working - you can upload documents and use vector search
2. ⚠️ Fix Neo4j connection to enable knowledge graph features
3. The app will still work without Neo4j, but knowledge graph features will be disabled
