#!/bin/bash

echo "========================================"
echo "Knowledge Graph RAG - Startup Script"
echo "========================================"
echo

# 1. Start Database
echo "[1/3] Starting Neo4j Database..."
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found. Please install Docker Desktop."
    exit 1
fi

# Start container
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start Neo4j container."
    exit 1
fi

# Wait for readiness
echo "Waiting for Neo4j to initialize (please wait)..."
sleep 5

# 2. Validate Connection
echo "[2/3] Validating Database Connection..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run validation script
python3 test_local_connection.py
if [ $? -ne 0 ]; then
    echo "❌ Database connection failed!"
    echo "Attempting to wait 10 more seconds..."
    sleep 10
    python3 test_local_connection.py
    if [ $? -ne 0 ]; then
        echo "❌ Connection still failed. Please check Docker logs: docker logs neo4j-kg-demo"
        exit 1
    fi
fi
echo "✓ Database connection verified"
echo

# 3. Start App
echo "[3/3] Starting Streamlit App..."
streamlit run ui/app.py
