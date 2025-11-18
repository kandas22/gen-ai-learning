# LangChain Learning - Complete Guide

A comprehensive hands-on guide to LangChain covering document loaders, text splitting, embeddings, vector stores, and retrievers.

## 📚 Table of Contents

1. [Setup & Installation](#setup--installation)
2. [Project Structure](#project-structure)
3. [Exercises Overview](#exercises-overview)
4. [Step-by-Step Execution Guide](#step-by-step-execution-guide)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.11 or higher
- Virtual environment (recommended)
- OpenAI API key (for OpenAI embeddings)

### Installation Steps

#### 1. Navigate to Project Directory

```bash
cd /Users/kanda/Learning/GenAI/gen-ai-learning/langchain_learning
```

#### 2. Activate Virtual Environment

```bash
# Activate the existing virtual environment
source ../.venv/bin/activate

# Or create a new one if needed
python -m venv .venv
source .venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**
```txt
langchain>=0.1.0
langchain-community>=0.0.20
langchain-openai>=1.0.0
langchain-huggingface>=0.0.1
langchain-text-splitters>=1.0.0
langchain-core>=1.0.0
langchain-classic>=1.0.0
chromadb>=0.4.0
faiss-cpu>=1.7.4
pymupdf>=1.23.0
sentence-transformers>=2.2.0
transformers>=4.30.0
openai>=1.0.0
python-dotenv>=1.0.0
tqdm>=4.65.0
```

#### 4. Configure Environment Variables

Create a `.env` file in the `langchain_learning` directory:

```bash
# .env
OPENAI_API_KEY=your-openai-api-key-here
```

**Security Note:** The `.env` file is already in `.gitignore` to prevent accidentally committing secrets.

---

## 📁 Project Structure

```
langchain_learning/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── assets/                    # Data and vector stores
│   ├── notes.txt             # Sample text file
│   ├── LLM.pdf               # Sample PDF document
│   ├── faiss_index/          # FAISS vector store
│   └── chroma_db/            # ChromaDB vector store
├── test.py                    # Import verification script
├── data_injustion.py         # Exercise 1: Document loaders
├── text_splitter.py          # Exercise 2: Text splitting
├── embedding.py              # Exercise 3: Embeddings
├── vector_store.py           # Exercise 4: Vector stores (FAISS)
├── retriever.py              # Exercise 5: Retrievers (FAISS)
└── chroma_retriver.py        # Exercise 6: ChromaDB with agent mode
```

---

## 📖 Exercises Overview

| # | Exercise | File | Concepts Covered | Duration |
|---|----------|------|------------------|----------|
| 0 | Verify Setup | `test.py` | Import validation | 2 min |
| 1 | Document Loaders | `data_injustion.py` | TextLoader, data ingestion | 5 min |
| 2 | Text Splitting | `text_splitter.py` | PyPDFLoader, CharacterTextSplitter | 10 min |
| 3 | Embeddings | `embedding.py` | OpenAI & HuggingFace embeddings | 10 min |
| 4 | Vector Stores | `vector_store.py` | FAISS creation and persistence | 15 min |
| 5 | Retrievers | `retriever.py` | FAISS retriever, similarity search | 10 min |
| 6 | ChromaDB Agent | `chroma_retriver.py` | ChromaDB, interactive queries | 20 min |

**Total Learning Time:** ~70 minutes

---

## 🎯 Step-by-Step Execution Guide

### Exercise 0: Verify Setup ✅

**Purpose:** Validate all dependencies are installed correctly.

**File:** `test.py`

**Command:**
```bash
python test.py
```

**Expected Output:**
```
✅ All imports are available!
```

**If you see errors:**
- Missing packages: Run `pip install -r requirements.txt`
- Import errors: Check the troubleshooting section below

---

### Exercise 1: Document Loaders 📄

**Purpose:** Learn how to load documents into memory using LangChain loaders.

**File:** `data_injustion.py`

**Concepts:**
- `TextLoader` - Load text files
- Document structure (page_content, metadata)
- Data buffering in memory

**Command:**
```bash
python data_injustion.py
```

**What it does:**
1. Loads `assets/notes.txt` using TextLoader
2. Stores content in memory as Document objects
3. No output (silent execution)

**Code snippet:**
```python
from langchain_community.document_loaders import TextLoader
data = TextLoader("langchain_learning/assets/notes.txt").load()
```

**Key Learnings:**
- Documents are loaded into RAM, not persisted by default
- Each Document has `page_content` (text) and `metadata` (file info)

---

### Exercise 2: Text Splitting 📝

**Purpose:** Split large documents into smaller chunks for processing.

**File:** `text_splitter.py`

**Concepts:**
- `PyPDFLoader` - Load and parse PDF files
- `CharacterTextSplitter` - Split text by character count
- Chunk size and overlap configuration

**Command:**
```bash
python text_splitter.py
```

**What it does:**
1. Loads `assets/LLM.pdf` using PyPDFLoader
2. Concatenates all pages into single text
3. Splits into 200-character chunks (no overlap)
4. Prints all chunks

**Expected Output:**
```
['Large Language Models (LLMs) are...', 'trained on massive datasets...', ...]
```

**Key Parameters:**
- `chunk_size=200` - Maximum characters per chunk
- `chunk_overlap=0` - No overlap between chunks

**Best Practices:**
- Use overlap (20-50 chars) to maintain context
- Adjust chunk size based on embedding model limits
- Use `RecursiveCharacterTextSplitter` for better semantic splitting

---

### Exercise 3: Embeddings 🔢

**Purpose:** Convert text into numerical vectors for semantic search.

**File:** `embedding.py`

**Concepts:**
- OpenAI Embeddings (1536 dimensions)
- HuggingFace Embeddings (384 dimensions)
- Vector representations of text

**Prerequisites:**
- Set `OPENAI_API_KEY` in `.env` file

**Command:**
```bash
python embedding.py
```

**What it does:**
1. Loads environment variables
2. Creates OpenAI embeddings for sample text
3. Creates HuggingFace embeddings for comparison
4. Prints first 5 values of each embedding vector

**Expected Output:**
```
Embedding vector: [-0.0123, 0.0456, -0.0789, 0.0234, -0.0567]
HuggingFace Embedding vector: [0.0234, -0.0456, 0.0789, ...]
```

**Key Learnings:**
- Embeddings capture semantic meaning as numbers
- Similar texts have similar embeddings (cosine similarity)
- Cannot reverse embeddings back to original text
- OpenAI requires API key, HuggingFace is free/local

---

### Exercise 4: Vector Stores (FAISS) 🗄️

**Purpose:** Store embeddings in a vector database for efficient retrieval.

**File:** `vector_store.py`

**Concepts:**
- FAISS (Facebook AI Similarity Search)
- Vector store creation from texts
- Persistence (save/load from disk)
- Similarity search

**Command:**
```bash
python vector_store.py
```

**What it does:**
1. Creates sample texts about Python and AI
2. Generates embeddings using HuggingFace
3. Creates FAISS index from texts
4. Saves index to `assets/faiss_index/`
5. Performs similarity search

**Expected Output:**
```
[Document(page_content='Python programming is best language for AI.', metadata={}), ...]
```

**Key Learnings:**
- FAISS provides fast similarity search
- Index can be saved to disk for reuse
- `similarity_search()` finds most relevant documents
- Requires matching embedding model for load/save

---

### Exercise 5: Retrievers (FAISS) 🔍

**Purpose:** Use retriever interface for semantic search.

**File:** `retriever.py`

**Concepts:**
- Loading existing FAISS index
- Retriever interface
- `invoke()` method for queries
- Similarity scoring

**Command:**
```bash
python retriever.py
```

**What it does:**
1. Loads existing FAISS index from disk
2. Creates retriever interface
3. Searches for "python?" query
4. Prints relevant documents

**Expected Output:**
```
[Document(page_content='Python programming is best language for AI.', metadata={'source': '...'})]
```

**Key Methods:**
- `vectorstore.as_retriever()` - Create retriever
- `retriever.invoke(query)` - Modern API for search
- `vectorstore.similarity_search(query, k=3)` - Direct search

---

### Exercise 6: ChromaDB Interactive Agent 🤖

**Purpose:** Build an interactive question-answering system with ChromaDB.

**File:** `chroma_retriver.py`

**Concepts:**
- ChromaDB vector database
- Persistent storage
- Interactive agent mode
- User input validation
- Multi-step workflow

**Command:**
```bash
python chroma_retriver.py
```

**What it does:**

#### Step-by-Step Workflow:

**STEP 1:** Prepare 8 sample texts about AI/programming

**STEP 2:** Load HuggingFace embeddings model

**STEP 3:** Create ChromaDB vector store
- Stores in `assets/chroma_db/`
- Automatically persists to disk

**STEP 4:** Test similarity search
- Query: "What is Python used for?"
- Returns top 2 results

**STEP 5:** Similarity search with scores
- Query: "Tell me about embeddings"
- Shows relevance scores (lower = more similar)

**STEP 6:** Use retriever interface
- Query: "What is Chroma?"
- Returns top 3 documents

**STEP 7:** Load existing database from disk
- Demonstrates persistence
- Reloads saved ChromaDB

**STEP 8:** Advanced retrieval (MMR)
- Maximal Marginal Relevance
- Returns diverse results

**STEP 9:** Add new documents dynamically
- Adds 2 new texts about deep learning
- Total: 10 documents

**STEP 10:** Collection statistics
- Shows collection name and document count

**STEP 11:** Interactive Agent Mode 🎯

This is where you can interact with the system!

**Usage:**
```
🤖 Enter your query (or 'quit' to exit): what is python

🔎 Searching for: 'what is python'
------------------------------------------------------------
✅ Found 3 relevant results:

📄 Result 1 (Relevance Score: 0.7234):
   Python is a high-level programming language widely used for AI and machine learning.

📄 Result 2 (Relevance Score: 0.8456):
   LangChain is a framework for developing applications powered by language models.

📄 Result 3 (Relevance Score: 0.9123):
   Machine learning models learn patterns from training data.
```

**Interactive Features:**
- ✅ Continuous query loop
- ✅ Empty string validation
- ✅ Multiple exit commands: 'quit', 'exit', 'q'
- ✅ Relevance scoring
- ✅ Error handling
- ✅ User-friendly prompts with emojis

**Try These Queries:**
```
- "explain embeddings"
- "what is machine learning"
- "tell me about LangChain"
- "python programming"
- "vector databases"
```

**Exit:** Type `quit`, `exit`, or `q`

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. ModuleNotFoundError: No module named 'langchain_community'

**Solution:**
```bash
pip install langchain-community
```

#### 2. ImportError: cannot import name 'OpenAIEmbeddings' from 'langchain.embeddings'

**Solution:**
Update import to use modular structure:
```python
from langchain_openai import OpenAIEmbeddings  # Correct
```

#### 3. TypeError: FAISS.load_local() missing 1 required positional argument: 'embeddings'

**Solution:**
Pass embeddings when loading:
```python
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("path/to/index", embeddings, allow_dangerous_deserialization=True)
```

#### 4. ImportError: cannot import name 'HuggingFaceEmbeddings' from 'langchain_openai'

**Solution:**
```bash
pip install langchain-huggingface
```

Then update import:
```python
from langchain_huggingface import HuggingFaceEmbeddings
```

#### 5. No module named 'chromadb'

**Solution:**
```bash
pip install chromadb
```

#### 6. ImportError: PyMuPDF package not found

**Solution:**
```bash
pip install pymupdf
```

#### 7. OpenAI API Key Error

**Solution:**
Create `.env` file:
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

Make sure `python-dotenv` is installed:
```bash
pip install python-dotenv
```

#### 8. Virtual Environment Not Working

**Solution:**
```bash
# Deactivate current environment
deactivate

# Activate the project's virtual environment
source /Users/kanda/Learning/GenAI/gen-ai-learning/.venv/bin/activate

# Verify Python path
which python
# Should show: /Users/kanda/Learning/GenAI/gen-ai-learning/.venv/bin/python
```

---

## 📊 Comparison: FAISS vs ChromaDB

| Feature | FAISS | ChromaDB |
|---------|-------|----------|
| **Persistence** | Manual (save/load) | Automatic |
| **Metadata** | Basic | Rich support |
| **Updates** | Immutable | Add/delete easily |
| **Production** | Library only | API server available |
| **Performance** | Extremely fast | Fast |
| **Memory** | Efficient | More overhead |
| **Best For** | Static, read-heavy | Dynamic, growing data |

---

## 🎓 Learning Path

**Beginner:**
1. Start with Exercise 0 (verify setup)
2. Complete Exercises 1-3 (basics)
3. Understand embeddings and vector concepts

**Intermediate:**
4. Complete Exercises 4-5 (FAISS)
5. Learn about vector stores and retrievers
6. Practice similarity search

**Advanced:**
7. Complete Exercise 6 (ChromaDB agent)
8. Build custom RAG applications
9. Experiment with different embedding models
10. Scale to production workloads

---

## 🚀 Next Steps

After completing all exercises:

1. **Build RAG Applications**
   - Integrate with ChatGPT/GPT-4
   - Create question-answering systems
   - Build document chat interfaces

2. **Explore Advanced Topics**
   - Multi-query retrievers
   - Contextual compression
   - Parent document retrievers
   - Ensemble retrievers

3. **Production Deployment**
   - Set up ChromaDB server
   - Implement caching strategies
   - Add monitoring and logging
   - Scale vector stores

4. **Experiment with Models**
   - Try different embedding models
   - Compare retrieval performance
   - Fine-tune for your domain

---

## 📚 Additional Resources

### Documentation
- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [Sentence Transformers](https://www.sbert.net/)

### Tutorials
- LangChain Retrieval QA
- Building RAG Systems
- Vector Database Optimization
- Embedding Model Selection

### Community
- LangChain Discord
- GitHub Discussions
- Stack Overflow

---

## ✅ Completion Checklist

- [ ] Environment setup complete
- [ ] All dependencies installed
- [ ] `.env` file configured
- [ ] Exercise 0: Imports verified
- [ ] Exercise 1: Document loaders
- [ ] Exercise 2: Text splitting
- [ ] Exercise 3: Embeddings
- [ ] Exercise 4: FAISS vector store
- [ ] Exercise 5: FAISS retriever
- [ ] Exercise 6: ChromaDB agent
- [ ] Tried interactive agent mode
- [ ] Understood all concepts
- [ ] Ready for RAG applications

---

## 🤝 Contributing

Found an issue or want to improve the exercises? Feel free to:
- Report bugs
- Suggest improvements
- Add new exercises
- Share your learning experience

---

## 📝 License

Educational purposes - Free to use and modify for learning.

---

**Happy Learning! 🎉**

For questions or issues, refer to the troubleshooting section or check the official LangChain documentation.
