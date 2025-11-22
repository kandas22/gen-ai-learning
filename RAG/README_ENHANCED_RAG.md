# 🤖 Enhanced RAG Chatbot System

A comprehensive RAG (Retrieval-Augmented Generation) chatbot with **Knowledge Graph**, **OCR**, **Multilingual Support** (especially Tamil), and **Hallucination Prevention**.

## ✨ Key Features

### 📄 **Document Processing**
- **PDF Processing**: Extract text and images from PDFs
- **OCR Support**: Extract text from images using Tesseract
- **Tamil Language**: Full support for Tamil text recognition
- **Multiple Formats**: PDF, images (PNG, JPG, TIFF), text files

### 🧠 **Knowledge Graph**
- **Entity Extraction**: Automatically extract entities from documents
- **Relationship Mapping**: Build relationships between entities
- **Neon PostgreSQL**: Store knowledge graph in Neon database
- **Graph-Enhanced Retrieval**: Use graph relationships to improve answers

### 🌍 **Multilingual Embeddings**
- **Gemini Embeddings**: Google's multilingual embedding model
- **Tamil Support**: Optimized for Tamil and English
- **High Quality**: Better semantic understanding across languages

### 🛡️ **Hallucination Prevention**
- **Source Attribution**: Every answer cites its sources
- **Confidence Scoring**: Display confidence for each response
- **Threshold-Based**: Refuse to answer when confidence is too low
- **No Hallucination**: Never generate information not in documents

### 🎨 **Beautiful UI**
- **Modern Design**: Gradient-based aesthetic
- **Real-time Processing**: Progress indicators for uploads
- **Interactive Chat**: Clean chat interface with metadata
- **Statistics Dashboard**: Track documents, chunks, entities

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR** (for image text extraction)
   ```bash
   # macOS
   brew install tesseract tesseract-lang
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr tesseract-ocr-tam
   
   # Windows
   # Download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

3. **API Keys**
   - Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Neon database from [Neon](https://neon.tech) (free tier available)

### Installation

1. **Clone and navigate to directory**
   ```bash
   cd /Users/kanda/Learning/GenAI/gen-ai-learning/RAG
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Configure Neon Database**
   - Create a free database at [neon.tech](https://neon.tech)
   - Enable pgvector extension in your database
   - Copy connection string to `.env`

### Running the Application

```bash
streamlit run enhanced_rag_chatbot.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. **Initialize System**
- Click "🔄 Initialize System" in the sidebar
- Wait for all components to initialize
- You should see success messages for embeddings, LLM, and document processor

### 2. **Upload Documents**
- Click "Choose files" in the sidebar
- Select PDFs, images, or text files
- Click "📤 Process Files"
- Wait for processing to complete

**Supported File Types:**
- PDF (`.pdf`)
- Images (`.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`)
- Text (`.txt`, `.md`)

### 3. **Ask Questions**
- Type your question in the chat input
- The system will:
  - Search relevant documents
  - Query knowledge graph (if enabled)
  - Generate answer with sources
  - Display confidence score

### 4. **View Results**
- **Answer**: Main response to your question
- **Confidence Score**: How confident the system is (color-coded)
  - 🟢 Green (70%+): High confidence
  - 🟡 Yellow (50-70%): Medium confidence
  - 🔴 Red (<50%): Low confidence
- **Sources**: Citations with relevance scores

## ⚙️ Configuration

### Environment Variables

Edit `.env` file:

```env
# Required
GEMINI_API_KEY=your-gemini-api-key
NEON_DATABASE_URL=postgresql://user:pass@host/db

# Optional
TESSERACT_CMD=/opt/homebrew/bin/tesseract
MIN_CONFIDENCE_THRESHOLD=0.6
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=5
```

### Settings in UI

- **Use Knowledge Graph**: Enable/disable graph-enhanced retrieval
- **Show Confidence Scores**: Display confidence for responses
- **Show Sources**: Display source citations

## 🏗️ Architecture

### Components

1. **Document Processor** (`document_processor.py`)
   - PDF text extraction
   - Image OCR with Tamil support
   - Intelligent text chunking

2. **Gemini Integration** (`gemini_embeddings.py`)
   - Multilingual embeddings
   - LLM for generation
   - Source attribution

3. **Knowledge Graph** (`knowledge_graph.py`)
   - Entity extraction
   - Relationship mapping
   - Neon PostgreSQL storage

4. **Streamlit App** (`enhanced_rag_chatbot.py`)
   - User interface
   - Document upload
   - Chat interface

### Data Flow

```
Document Upload → OCR/Processing → Chunking → Embeddings → Vector Store
                                              ↓
                                    Entity Extraction
                                              ↓
                                    Knowledge Graph (Neon)

User Query → Vector Search + Graph Query → Context Retrieval → LLM Generation → Response with Sources
```

## 🔍 Features in Detail

### OCR with Tamil Support

The system uses Tesseract OCR with Tamil language pack:
- Automatically detects text in images
- Supports both English and Tamil
- Provides confidence scores for OCR results
- Displays images alongside extracted text

### Knowledge Graph

Entities and relationships are automatically extracted:
- **Entities**: People, organizations, locations, concepts
- **Relationships**: "works_for", "located_in", "related_to", etc.
- **Graph Queries**: Find related entities to enhance context
- **Visualization**: (Optional) View entity relationships

### Hallucination Prevention

Multiple strategies ensure accurate responses:
1. **Source Requirement**: Only answer from retrieved documents
2. **Confidence Threshold**: Refuse low-confidence answers
3. **Citation Requirement**: Always cite sources
4. **Explicit Uncertainty**: Say "I don't know" when appropriate

## 📊 Statistics

The sidebar shows:
- **Documents Processed**: Total uploaded documents
- **Total Chunks**: Number of text chunks in vector store
- **Images with OCR**: Number of images processed
- **Entities**: Total entities in knowledge graph
- **Relationships**: Total relationships in graph

## 🧪 Testing

### Test with Sample Documents

1. **English PDF**: Upload any technical PDF
2. **Tamil Document**: Upload Tamil text or image
3. **Mixed Content**: Upload PDF with both text and images

### Example Questions

- "What is the main topic of this document?"
- "Summarize the key points"
- "What entities are mentioned?" (with KG enabled)
- "Show me information about [specific topic]"

## 🐛 Troubleshooting

### Tesseract Not Found

```bash
# Find Tesseract location
which tesseract

# macOS - set in .env
TESSERACT_CMD=/opt/homebrew/bin/tesseract

# Or install:
brew install tesseract tesseract-lang
```

### Tamil OCR Not Working

```bash
# Verify Tamil language pack
tesseract --list-langs | grep tam

# If not found, install:
# macOS
brew install tesseract-lang

# Ubuntu
sudo apt-get install tesseract-ocr-tam
```

### Neon Connection Failed

- Check `NEON_DATABASE_URL` in `.env`
- Ensure pgvector extension is enabled
- Verify database is accessible

### Low Confidence Responses

- Upload more relevant documents
- Adjust `MIN_CONFIDENCE_THRESHOLD` in `.env`
- Enable knowledge graph for better context

## 🔐 Security

- API keys stored in `.env` (not committed to git)
- Database connections use SSL
- No sensitive data in logs
- Source attribution prevents misinformation

## 📝 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- **Google Gemini**: Multilingual embeddings and LLM
- **Neon**: Serverless PostgreSQL with pgvector
- **Tesseract**: Open-source OCR engine
- **Streamlit**: Beautiful web app framework
- **LangChain**: RAG framework

## 🚀 Next Steps

- Add more document formats (DOCX, HTML)
- Implement graph visualization
- Add conversation memory
- Support more languages
- Add batch processing

---

**Built with ❤️ for multilingual RAG applications**

🔗 **Quick Start**: `streamlit run enhanced_rag_chatbot.py`
