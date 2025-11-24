# Q&A RAG System with Knowledge Graph

A high-accuracy Question & Answer system combining vector search (Neon DB) and knowledge graph (Neo4j) for extracting and querying information from PDFs, including text and images via OCR.

## 🎯 Features

- **Hybrid Retrieval**: Combines vector similarity search with knowledge graph traversal
- **PDF Processing**: Extract text and images from PDFs using PyMuPDF
- **OCR Support**: Extract text from images using Tesseract
- **Knowledge Graph**: Build entity-relationship graphs in Neo4j
- **Vector Search**: Fast semantic search using Neon DB with pgvector
- **Streamlit UI**: Interactive chatbot interface with graph visualization
- **Anti-Hallucination**: Strict prompts and confidence scoring to minimize errors

## 📋 Prerequisites

### System Requirements
- Python 3.9+
- Tesseract OCR installed
- PostgreSQL with pgvector (via Neon DB)
- Neo4j database (local or Aura)

### Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## 🚀 Setup Instructions

### 1. Clone and Navigate
```bash
cd /Users/kanda/Learning/GenAI/gen-ai-learning/knowlege_graph_assignment
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```bash
# Required: Choose your LLM provider
LLM_PROVIDER=google  # or openai, anthropic

# Required: Add your API key
GOOGLE_API_KEY=your_actual_api_key_here

# Required: Neon DB credentials
NEON_DB_URI=postgresql://user:password@host/dbname
NEON_DB_USER=your_username
NEON_DB_PASSWORD=your_password

# Required: Neo4j credentials
NEO4J_URI=bolt://localhost:7687
NEO4J_PASSWORD=your_neo4j_password
```

### 5. Set Up Databases

**Neon DB (PostgreSQL with pgvector):**
1. Sign up at https://neon.tech
2. Create a new project
3. Enable pgvector extension in SQL Editor:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
4. Copy connection details to `.env`

**Neo4j:**

Option A - Local Installation:
```bash
# Download from https://neo4j.com/download/
# Or use Docker:
docker run -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest
```

Option B - Neo4j Aura (Cloud):
1. Sign up at https://neo4j.com/cloud/aura/
2. Create a free instance
3. Update `.env` with Aura credentials

### 6. Initialize Databases
```bash
python database/init_db.py
```

### 7. Run the Application
```bash
streamlit run ui/app.py
```

## 📁 Project Structure

```
knowlege_graph_assignment/
├── config/
│   ├── settings.py          # Environment configuration
│   └── prompts.py           # System prompts for RAG
├── database/
│   ├── neon_vector_store.py # Vector operations
│   ├── neo4j_graph_store.py # Graph operations
│   └── init_db.py           # Database setup
├── processing/
│   ├── pdf_processor.py     # PDF text extraction
│   ├── ocr_processor.py     # Tesseract OCR
│   ├── chunking.py          # Document chunking
│   └── embeddings.py        # Embedding generation
├── knowledge_graph/
│   ├── entity_extractor.py  # Extract entities
│   ├── relationship_extractor.py # Extract relationships
│   └── graph_builder.py     # Build Neo4j graph
├── rag/
│   ├── retriever.py         # Hybrid retrieval
│   ├── context_builder.py   # Context aggregation
│   └── generator.py         # Answer generation
├── ui/
│   ├── app.py               # Streamlit app
│   └── components/          # UI components
├── .env.example             # Environment template
└── requirements.txt         # Python dependencies
```

## 🔧 Configuration

All configuration is managed through environment variables in `.env`:

### LLM Settings
- `LLM_PROVIDER`: Choose between `google`, `openai`, or `anthropic`
- `GOOGLE_API_KEY`: Your API key
- `LLM_TEMPERATURE`: Controls randomness (0.0-1.0, default: 0.1)

### Vector Settings
- `EMBEDDING_DIMENSION`: Vector size (768 for Google, 1536/3072 for OpenAI)
- `VECTOR_INDEX_TYPE`: `hnsw` (recommended) or `ivfflat`
- `TOP_K_RETRIEVAL`: Number of chunks to retrieve (default: 5)

### Document Processing
- `CHUNK_SIZE`: Text chunk size in characters (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)

### RAG Pipeline
- `ENABLE_GRAPH_RETRIEVAL`: Enable/disable graph retrieval (default: true)
- `VECTOR_RETRIEVAL_WEIGHT`: Weight for vector search (default: 0.6)
- `GRAPH_RETRIEVAL_WEIGHT`: Weight for graph search (default: 0.4)

## 📖 Usage

1. **Upload PDF**: Use the sidebar to upload PDF documents
2. **Wait for Processing**: The system will extract text, run OCR, create embeddings, and build the knowledge graph
3. **Ask Questions**: Type your questions in the chat interface
4. **View Results**: See answers with confidence scores and source citations
5. **Explore Graph**: Visualize the knowledge graph for your documents

## 🎯 Accuracy Tips

To maximize accuracy and minimize hallucinations:

1. **Upload Quality PDFs**: Clear, well-formatted documents work best
2. **Ask Specific Questions**: More specific questions get better answers
3. **Check Confidence Scores**: Low confidence may indicate uncertain answers
4. **Review Sources**: Always check the cited sources
5. **Adjust Retrieval**: Tune `TOP_K_RETRIEVAL` and weights in `.env`

## 🐛 Troubleshooting

### Tesseract Not Found
```bash
# Check Tesseract installation
tesseract --version

# Update TESSERACT_CMD in .env with correct path
which tesseract  # macOS/Linux
where tesseract  # Windows
```

### Database Connection Errors
- Verify credentials in `.env`
- Check database is running
- Test connection manually

### Low Accuracy
- Increase `TOP_K_RETRIEVAL`
- Adjust retrieval weights
- Use more specific questions
- Improve document quality

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.
