# Kanda RAG Chatbot - PDF Question & Answer System 🤖

A powerful Retrieval-Augmented Generation (RAG) chatbot built with Streamlit that allows you to upload PDF documents and ask intelligent questions about their content.

## 📹 Demo

See the chatbot in action! Check out the example video in the `asserts/` folder:
- **Simple_RAG_ChatBot.mov** - Full demonstration of PDF upload and Q&A functionality

## Features

### 🎯 Core Functionality
- **PDF Upload & Processing**: Upload any text-based PDF document
- **Intelligent Q&A**: Ask questions and get accurate answers from your PDF
- **Source Citations**: See exactly where the information comes from with page numbers
- **Conversation Memory**: Maintains chat history for contextual conversations
- **Semantic Search**: Uses vector embeddings for accurate information retrieval

### 💡 Smart Features
- **Automatic Text Chunking**: Splits documents into optimal chunks (1000 chars with 200 overlap)
- **Multiple Source Display**: Shows top 3 relevant sources for each answer
- **Chat History**: Keep track of all your questions and answers
- **Clean UI**: Modern, responsive interface with gradient styling
- **Real-time Statistics**: View document stats (chunks, filename, status)

### 🎨 User Interface
- Beautiful gradient color scheme
- Distinct user/bot message styling
- Source document highlighting
- Processing status indicators
- Expandable sidebar with controls

## Architecture

```
User → Upload PDF → Process & Chunk → Create Embeddings → Store in FAISS
                                                              ↓
User Question → Embed Query → Semantic Search → Retrieve Relevant Chunks
                                                              ↓
                                        GPT-3.5-Turbo + Context → Answer + Sources
```

## Technology Stack

- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-3.5-Turbo
- **Embeddings**: HuggingFace sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Framework**: LangChain
- **PDF Processing**: PyPDF

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Virtual environment (recommended)

## Installation

### 1. Clone or navigate to the RAG directory

```bash
cd RAG
```

### 2. Create and activate virtual environment

```bash
# Create virtual environment
python -m venv .venv

# Activate on macOS/Linux
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up OpenAI API Key

Create a `.env` file in the RAG directory:

```bash
touch .env
```

Add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-api-key-here
```

**Important**: Never commit your `.env` file to version control!

## Usage

### Running the Chatbot

```bash
streamlit run chatbot.py
```

The app will open in your browser at `http://localhost:8501`.

### Step-by-Step Guide

1. **Upload PDF**
   - Click on the sidebar
   - Click "Browse files" or drag & drop your PDF
   - Supported: Any text-based PDF document

2. **Process Document**
   - Click "🚀 Process PDF" button
   - Wait for processing (usually 10-30 seconds)
   - You'll see confirmation when ready

3. **Ask Questions**
   - Type your question in the input box
   - Click "Send 📤" or press Enter
   - View the answer with source citations

4. **Manage Session**
   - Clear chat history: Click "🔄 Clear Chat History"
   - Remove PDF: Click "❌ Remove PDF"
   - Upload new PDF: Remove current, upload new

## Example Questions

Here are some questions you can ask about your uploaded PDF:

- "What is the main topic of this document?"
- "Can you summarize the key points?"
- "What are the conclusions or recommendations?"
- "Explain the methodology described in the document"
- "What data or statistics are mentioned?"
- "Who are the authors and what are their affiliations?"
- "What are the limitations mentioned?"
- "What future work is suggested?"

## How RAG Works

### 1. Document Processing
```python
PDF → Load → Split into Chunks (1000 chars) → Create Embeddings → Store in FAISS
```

### 2. Query Processing
```python
User Question → Embed Query → Search FAISS → Retrieve Top 3 Chunks
```

### 3. Answer Generation
```python
Relevant Chunks + Question + Chat History → GPT-3.5-Turbo → Answer + Sources
```

### Key Components

**Text Splitter**:
- Chunk size: 1000 characters
- Overlap: 200 characters (maintains context)
- Separators: Paragraphs, lines, spaces

**Embeddings**:
- Model: sentence-transformers/all-MiniLM-L6-v2
- Dimension: 384
- Fast and accurate for semantic search

**Vector Store**:
- FAISS for efficient similarity search
- Retrieves top 3 most relevant chunks per query

**LLM**:
- GPT-3.5-Turbo with temperature 0.7
- Conversational memory for context
- Returns source documents for transparency

## Project Structure

```
RAG/
├── chatbot.py           # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env                 # OpenAI API key (create this)
├── .venv/              # Virtual environment (created by you)
└── README.md           # This file
```

## Features Explained

### Conversation Memory
The chatbot maintains conversation history, allowing for follow-up questions:
- "What was mentioned about X?" 
- "Tell me more about that"
- "Can you elaborate?"

### Source Citations
Every answer includes:
- Page numbers from the PDF
- Relevant text snippets (150 chars preview)
- Multiple sources (up to 3)
- Transparency in information retrieval

### Session State Management
- Vectorstore persistence during session
- Chat history maintained
- PDF metadata stored
- Statistics tracking

## Configuration

### Adjusting Chunk Size

In `chatbot.py`, modify the text splitter:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Increase for longer context
    chunk_overlap=200,     # Increase to maintain more context
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)
```

### Changing Number of Retrieved Sources

Modify the retriever configuration:

```python
retriever=st.session_state.vectorstore.as_retriever(
    search_kwargs={"k": 3}  # Change 3 to your preferred number
)
```

### Adjusting LLM Temperature

In the `setup_conversation_chain()` function:

```python
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,  # Lower (0.0) = more focused, Higher (1.0) = more creative
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```

### Using Different Models

Replace GPT-3.5-Turbo with other models:

```python
# For GPT-4
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# For GPT-4-Turbo
llm = ChatOpenAI(
    model_name="gpt-4-turbo-preview",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`:

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### OpenAI API Errors

If you see "Invalid API key" or authentication errors:

1. Check `.env` file exists in RAG directory
2. Verify API key format: `OPENAI_API_KEY=sk-...`
3. Ensure no extra spaces or quotes
4. Check API key is valid at https://platform.openai.com/api-keys

### PDF Processing Fails

If PDF upload/processing fails:

- Ensure PDF is text-based (not scanned images)
- Try a smaller PDF (< 50 pages for faster processing)
- Check PDF is not password-protected
- Verify sufficient disk space for temporary files

### Slow Performance

To improve speed:

- Use smaller PDFs
- Reduce chunk size
- Reduce number of retrieved sources (k=1 or k=2)
- Use GPT-3.5-Turbo instead of GPT-4

### Memory Issues

If running out of memory:

- Process smaller PDFs
- Reduce chunk size and overlap
- Clear chat history frequently
- Restart the application

## Best Practices

### For Better Answers

1. **Be Specific**: Ask precise questions about the document
2. **Use Context**: Reference specific sections or topics
3. **Follow Up**: Use conversation memory for deeper exploration
4. **Check Sources**: Verify information with source citations

### For Optimal Performance

1. **PDF Quality**: Use text-based PDFs with clear formatting
2. **Document Size**: 10-50 pages work best
3. **API Usage**: Monitor OpenAI API costs
4. **Session Management**: Clear history for new topics

### For Development

1. **Version Control**: Never commit `.env` file
2. **API Keys**: Use environment variables
3. **Error Handling**: Check logs for debugging
4. **Testing**: Test with various PDF types

## Cost Considerations

### OpenAI API Costs

- **GPT-3.5-Turbo**: ~$0.002 per 1K tokens (very affordable)
- **GPT-4**: ~$0.03 per 1K tokens (more expensive but better quality)

### Estimation

For a typical 20-page PDF with 10 questions:
- Embeddings: Free (HuggingFace local)
- Vector store: Free (FAISS local)
- LLM calls: ~$0.05-0.20 (GPT-3.5-Turbo)

## Security Notes

### Data Privacy

- PDFs are processed locally (not sent to external servers except OpenAI)
- Temporary files are deleted after processing
- Chat history is session-based (not persistent)
- Vector store is in-memory (cleared on app restart)

### API Key Security

- Store in `.env` file (never hardcode)
- Add `.env` to `.gitignore`
- Never share or commit API keys
- Rotate keys periodically

## Advanced Features

### Add Custom Prompts

Modify the conversation chain to include custom system prompts:

```python
from langchain.prompts import PromptTemplate

template = """You are a helpful assistant analyzing documents.
Use the following context to answer the question.
If you don't know, say so clearly.

Context: {context}
Question: {question}

Answer:"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])
```

### Add Document Metadata

Include more metadata in source citations:

```python
# In display_chat_message function
metadata = source.metadata
page = metadata.get('page', 'Unknown')
source_file = metadata.get('source', 'Unknown')
# Add more metadata as needed
```

### Export Chat History

Add export functionality:

```python
import json

def export_chat():
    history_json = json.dumps(st.session_state.chat_history, indent=2)
    st.download_button(
        label="Download Chat History",
        data=history_json,
        file_name="chat_history.json",
        mime="application/json"
    )
```

## Future Enhancements

Potential features to add:

- [ ] Support for multiple PDF files simultaneously
- [ ] Document comparison between multiple PDFs
- [ ] Chat history export (JSON, TXT, PDF)
- [ ] Persistent storage (database integration)
- [ ] User authentication and sessions
- [ ] Support for other document formats (DOCX, TXT, etc.)
- [ ] Advanced search filters
- [ ] Custom embedding models
- [ ] Multi-language support
- [ ] Voice input/output

## Dependencies

All dependencies are listed in `requirements.txt`:

```
streamlit>=1.51.0           # Web framework
python-dotenv>=1.0.0        # Environment variables
langchain>=0.1.0            # LLM framework
langchain-community>=0.0.20 # Community loaders
langchain-openai>=1.0.0     # OpenAI integration
langchain-huggingface>=0.0.1 # HuggingFace embeddings
langchain-text-splitters>=1.0.0 # Text splitting
faiss-cpu>=1.7.4            # Vector store
pypdf>=3.17.0               # PDF processing
sentence-transformers>=2.2.0 # Embeddings model
transformers>=4.30.0        # Transformer models
openai>=1.0.0               # OpenAI API
```

## Support

For issues or questions:

1. Check this README thoroughly
2. Review error messages in terminal
3. Verify all prerequisites are met
4. Check OpenAI API status
5. Ensure all dependencies are installed

## License

Free to use for learning and development purposes.

---

**Built with ❤️ using Streamlit, LangChain, and OpenAI**

🔒 Your documents are processed securely and locally

---

## Quick Start Commands

```bash
# Setup
cd RAG
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Create .env and add your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Run
streamlit run chatbot.py
```

Happy chatting! 🤖📚
