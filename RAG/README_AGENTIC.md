# Kanda Fallback RAG with Web Search 🔍

An intelligent chatbot that searches your PDF documents first, then automatically falls back to web search if the answer isn't found in your documents. Built with Streamlit, LangChain, OpenAI, and SearchAPI.io.

## 📹 Demo

See the agentic chatbot in action! Check out the example video in the `asserts/` folder:
- **Agent_RAG_Chatbot.mov** - Full demonstration of PDF search and automatic web search fallback

## Features

### 🎯 Smart Fallback System
- **PDF-First Search**: Always searches uploaded PDF documents first
- **Automatic Web Fallback**: If no answer found in PDF, searches the web automatically
- **Intelligent Routing**: Seamlessly switches between sources
- **Source Transparency**: Color-coded responses show which source was used

### 💡 Advanced Capabilities
- **Works Without PDF**: Can answer questions using web search only
- **Conversational Memory**: Maintains chat history across questions
- **Source Citations**: Shows PDF page numbers and web search results
- **Beautiful UI**: Gradient-styled interface with visual source indicators
- **Statistics Dashboard**: Track PDF vs Web search usage

### 🎨 User Interface
- **Color-Coded Messages**:
  - Purple gradient: User messages
  - Pink gradient: PDF-sourced answers
  - Blue gradient: Web-sourced answers
- **Expandable Sources**: Click to view detailed PDF excerpts
- **Real-time Stats**: Monitor search distribution
- **Responsive Design**: Works on desktop and mobile

## Architecture

```
User Question
    ↓
PDF Available?
    ↓
    Yes → Search PDF
        ↓
        Answer Found? → Return PDF Answer (Pink)
        ↓
        No ↓
    ↓
Search Web (SerpAPI)
    ↓
Return Web Answer (Blue)
```

## Technology Stack

- **Frontend**: Streamlit with custom CSS
- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: HuggingFace sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Web Search**: SerpAPI
- **Framework**: LangChain
- **PDF Processing**: PyPDF

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- SerpAPI key
- Virtual environment (recommended)

## Installation

### 1. Navigate to RAG directory

```bash
cd RAG
```

### 2. Ensure virtual environment is active

```bash
# If not already activated
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install google-search-results
```

All other dependencies should already be installed from the main chatbot setup.

### 4. Set up API Keys

Add your SerpAPI key to the `.env` file:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-key-here

# SerpAPI Configuration (for web search)
SERPAPI_API_KEY=your-serpapi-key-here
```

**Get your SerpAPI key**: https://serpapi.com/manage-api-key
- Free tier: 100 searches/month
- Paid plans available for higher usage

## Usage

### Running the Chatbot

```bash
streamlit run chatbot_agentic.py
```

The app will open in your browser at `http://localhost:8501`.

### Usage Scenarios

#### Scenario 1: PDF + Web Fallback (Recommended)
1. Upload a PDF document
2. Click "🚀 Process PDF"
3. Ask questions about the document
4. If answer not in PDF, web search activates automatically

#### Scenario 2: Web Search Only
1. Don't upload any PDF
2. Ask any general knowledge question
3. Answers come directly from web search

#### Scenario 3: PDF Priority
1. Upload and process PDF
2. Ask questions related to your document
3. Get answers from PDF with source citations
4. See page numbers and excerpts

## Features Explained

### Smart Fallback Logic

```python
1. User asks question
2. If PDF uploaded:
   - Search PDF using RAG
   - Check if answer is meaningful
   - If yes → Return PDF answer
   - If no → Continue to step 3
3. Search web using SerpAPI
4. Return web answer with citation
```

### Source Detection

The system determines answer quality using:
- **Relevance Check**: Minimum answer length (20 chars)
- **Content Analysis**: Looks for "NOT_FOUND" indicators
- **Document Similarity**: FAISS relevance scores

### Visual Indicators

| Color | Source | Description |
|-------|--------|-------------|
| 🟣 Purple | User | User's questions |
| 🩷 Pink | PDF | Answers from uploaded document |
| 💙 Blue | Web | Answers from web search |

### Statistics Dashboard

Monitor your usage:
- **📄 PDF Searches**: Count of answers from PDF
- **🌐 Web Searches**: Count of answers from web
- **📊 PDF Stats**: Document info when PDF loaded

## How It Works

### PDF Search Process

1. **Document Processing**:
   ```
   PDF → Load Pages → Split into Chunks → Create Embeddings → Store in FAISS
   ```

2. **Question Answering**:
   ```
   Question → Retrieve Similar Chunks → Send to LLM → Generate Answer
   ```

3. **Quality Check**:
   ```
   Answer → Check Length → Check Content → Determine if Sufficient
   ```

### Web Search Process

1. **Query Execution**:
   ```
   Question → SerpAPI Search → Get Results → Format Context
   ```

2. **Answer Generation**:
   ```
   Web Results → Send to LLM → Generate Answer → Return with Citation
   ```

## Configuration

### Adjusting Search Parameters

#### PDF Search Settings

In `search_pdf()` function:

```python
retriever = st.session_state.vectorstore.as_retriever(
    search_kwargs={"k": 3}  # Number of chunks to retrieve
)
```

#### Answer Quality Threshold

In `search_pdf()` function:

```python
if "NOT_FOUND" in answer or len(answer.strip()) < 20:  # Minimum answer length
    return None, []
```

### Changing Models

#### LLM Model

```python
llm = ChatOpenAI(
    model_name="gpt-4o-mini",  # Change to gpt-4, gpt-3.5-turbo, etc.
    temperature=0.7,            # 0.0 = focused, 1.0 = creative
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```

#### Embedding Model

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",  # Change model
    model_kwargs={'device': 'cpu'}  # Use 'cuda' for GPU
)
```

## Example Questions

### PDF Questions (if uploaded)
- "What is the main topic of this document?"
- "Summarize the key findings"
- "What methodology was described?"
- "Who are the authors?"
- "What are the conclusions?"

### General Web Questions
- "What is artificial intelligence?"
- "Latest news about climate change"
- "How does blockchain technology work?"
- "What is the capital of France?"
- "Explain quantum computing"

### Hybrid Questions
- "Compare this document's findings with current industry standards" (uses both!)

## Troubleshooting

### SerpAPI Errors

**Error: "SERPAPI_API_KEY not found"**
- Check `.env` file exists in RAG directory
- Verify key is correctly formatted: `SERPAPI_API_KEY=your-key-here`
- No quotes needed around the key

**Error: "Rate limit exceeded"**
- Free tier limited to 100 searches/month
- Upgrade plan at https://serpapi.com/pricing
- Wait until monthly limit resets

### PDF Search Issues

**PDF search always falls back to web**
- Check if PDF was processed successfully
- Verify embeddings model loaded correctly
- Try questions more specific to document content

**No sources shown for PDF answers**
- This is normal if answer came from web search
- PDF sources only shown when answer from PDF

### General Issues

**Import errors**
- Ensure `google-search-results` installed: `pip install google-search-results`
- Activate virtual environment: `source .venv/bin/activate`
- Reinstall requirements: `pip install -r requirements.txt`

**Slow responses**
- PDF search is fast (< 2 seconds)
- Web search can take 3-5 seconds
- Both LLM calls add processing time

## Cost Considerations

### OpenAI API Costs

- **GPT-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- Average question: ~500 tokens total
- Estimated: $0.0004 per question

### SerpAPI Costs

- **Free tier**: 100 searches/month (sufficient for testing)
- **Paid tiers**: From $50/month for 5,000 searches
- Only charged when web search is used

### Optimization Tips

1. **Upload relevant PDFs** to maximize PDF hits
2. **Be specific** with questions to get better PDF matches
3. **Monitor statistics** to track search distribution
4. **Use PDF search** when possible (free after setup)

## Security Notes

### API Keys

- **Never commit** `.env` file to version control
- **Rotate keys** periodically
- **Limit permissions** in API dashboards
- **Monitor usage** for unusual activity

### Data Privacy

- PDFs processed locally (not sent to external servers except OpenAI for LLM)
- Web searches go through SerpAPI
- No data persistence between sessions
- Chat history cleared on app restart

## Advanced Features

### Custom Prompts

Modify the prompts in the code to change behavior:

**PDF Search Prompt:**
```python
prompt = f"""Based on the following context from the PDF document, answer the question.
If the context doesn't contain relevant information to answer the question, respond with "NOT_FOUND".
...
```

**Web Search Prompt:**
```python
prompt = f"""Based on the following web search results, provide a comprehensive answer to the question.
Be informative and cite that the information comes from web search.
...
```

### Adding More Fallback Sources

You can extend the fallback chain:
1. PDF Search
2. Web Search
3. Wikipedia Search
4. Custom Database
5. Default response

## Comparison: Basic vs Agentic Chatbot

| Feature | Basic (chatbot.py) | Agentic (chatbot_agentic.py) |
|---------|-------------------|------------------------------|
| PDF Search | ✅ Yes | ✅ Yes |
| Web Search | ❌ No | ✅ Yes |
| Fallback System | ❌ No | ✅ Automatic |
| Works Without PDF | ❌ No | ✅ Yes |
| Source Detection | Basic | Color-coded |
| Search Stats | ❌ No | ✅ Yes |
| Flexibility | Limited | High |

## Future Enhancements

Potential features to add:

- [ ] Multiple PDF support
- [ ] Custom search engines (Bing, Google, etc.)
- [ ] Wikipedia integration
- [ ] Database search fallback
- [ ] Export chat history
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Confidence scores
- [ ] Citation management
- [ ] Fact-checking layer

## Dependencies

```
streamlit>=1.51.0
python-dotenv>=1.0.0
langchain==0.3.7
langchain-community==0.3.7
langchain-openai==0.2.8
langchain-huggingface==0.1.2
langchain-text-splitters==0.3.2
faiss-cpu>=1.7.4
pypdf>=3.17.0
sentence-transformers>=2.2.0
transformers>=4.30.0
openai>=1.0.0
google-search-results>=2.4.2
```

## Support

For issues or questions:

1. Check this README thoroughly
2. Review error messages in terminal
3. Verify all API keys are set correctly
4. Check SerpAPI dashboard for quota
5. Ensure all dependencies installed

## License

Free to use for learning and development purposes.

---

## Quick Start Commands

```bash
# Setup (if not already done)
cd RAG
source .venv/bin/activate
pip install google-search-results

# Add SerpAPI key to .env file
echo "SERPAPI_API_KEY=your-key-here" >> .env

# Run the chatbot
streamlit run chatbot_agentic.py
```

---

**Built with ❤️ using Streamlit, LangChain, OpenAI & SerpAPI**

🔍 Smart fallback system: PDF → Web Search

Enjoy intelligent question answering! 🚀
