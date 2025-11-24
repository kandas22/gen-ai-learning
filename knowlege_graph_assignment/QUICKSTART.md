# Quick Start Guide

## Prerequisites

Before running the system, ensure you have:

1. **Python 3.9+** installed
2. **Tesseract OCR** installed (see README.md for installation instructions)
3. **Neon DB account** with pgvector enabled
4. **Neo4j database** (local or Aura cloud)
5. **LLM API key** (Google Gemini, OpenAI, or Anthropic)

## Setup Steps

### 1. Install Dependencies

```bash
cd /Users/kanda/Learning/GenAI/gen-ai-learning/knowlege_graph_assignment
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
nano .env  # or use any text editor
```

**Required fields:**
- `GOOGLE_API_KEY` (or your chosen LLM provider key)
- `NEON_DB_URI`, `NEON_DB_USER`, `NEON_DB_PASSWORD`
- `NEO4J_PASSWORD`

### 3. Initialize Databases

```bash
python database/init_db.py
```

This will:
- Create tables in Neon DB
- Set up pgvector extension
- Create Neo4j constraints and indexes
- Verify connections

### 4. Run the Application

```bash
streamlit run ui/app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Upload PDF**: Click "Upload PDF Document" in the sidebar
2. **Process**: Click "Process Document" to extract text, run OCR, and build knowledge graph
3. **Ask Questions**: Type your questions in the chat input
4. **View Answers**: See answers with confidence scores and source citations

## Troubleshooting

### Tesseract Not Found
```bash
# Check installation
tesseract --version

# Update path in .env
TESSERACT_CMD=/path/to/tesseract
```

### Database Connection Errors
- Verify credentials in `.env`
- Check that databases are running
- Run `python database/init_db.py` to verify connections

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Project Structure

```
knowlege_graph_assignment/
├── config/          # Configuration and prompts
├── database/        # Neon DB and Neo4j handlers
├── processing/      # PDF, OCR, chunking, embeddings
├── knowledge_graph/ # Entity/relationship extraction
├── rag/            # Retrieval and generation
├── ui/             # Streamlit application
└── utils/          # Logging and validation
```

## Next Steps

- Test with various PDF documents
- Tune retrieval parameters in `.env`
- Customize system prompts in `config/prompts.py`
- Add more entity types as needed
