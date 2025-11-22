# 🛠️ Setup Guide - Enhanced RAG Chatbot

Step-by-step guide to set up the Enhanced RAG Chatbot system.

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] Python 3.8 or higher
- [ ] pip package manager
- [ ] Git (optional, for cloning)
- [ ] Internet connection for API access

## 🔧 Step 1: Install Tesseract OCR

Tesseract is required for extracting text from images.

### macOS

```bash
# Using Homebrew
brew install tesseract tesseract-lang

# Verify installation
tesseract --version

# Check Tamil language support
tesseract --list-langs | grep tam
```

### Ubuntu/Debian Linux

```bash
# Install Tesseract and Tamil language pack
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-tam

# Verify installation
tesseract --version
tesseract --list-langs | grep tam
```

### Windows

1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. During installation, select "Additional language data" and check Tamil
4. Add Tesseract to PATH or note the installation path
5. Set `TESSERACT_CMD` in `.env` to the full path (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`)

## 🔑 Step 2: Get API Keys

### Gemini API Key (Required)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key (starts with `AIza...`)
5. Save it for the `.env` file

**Note**: Gemini API has a free tier with generous limits.

### Neon Database (Required for Knowledge Graph)

1. Go to [Neon](https://neon.tech)
2. Sign up for a free account
3. Create a new project
4. Create a database (default is fine)
5. **Enable pgvector extension**:
   - Go to SQL Editor in Neon console
   - Run: `CREATE EXTENSION IF NOT EXISTS vector;`
6. Copy the connection string from "Connection Details"
   - Format: `postgresql://user:password@host/database?sslmode=require`

**Note**: Neon free tier includes 0.5 GB storage, which is sufficient for testing.

### Optional: OpenAI API Key

Only needed if you want to use OpenAI as a fallback:
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an API key
3. Add to `.env` file

## 📦 Step 3: Install Python Dependencies

```bash
# Navigate to the RAG directory
cd /Users/kanda/Learning/GenAI/gen-ai-learning/RAG

# Create a virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: Installation may take 5-10 minutes due to large packages like transformers.

## ⚙️ Step 4: Configure Environment Variables

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file**:
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Add your API keys**:
   ```env
   # Required
   GEMINI_API_KEY=AIza...your-actual-key...
   NEON_DATABASE_URL=postgresql://user:password@host/database?sslmode=require
   
   # Optional
   TESSERACT_CMD=/usr/local/bin/tesseract  # or /opt/homebrew/bin/tesseract
   MIN_CONFIDENCE_THRESHOLD=0.6
   ENABLE_SOURCE_ATTRIBUTION=true
   ```

4. **Save and close** the file

## ✅ Step 5: Verify Installation

### Test Tesseract

```bash
# Create a test image with text (or use any image)
echo "Testing Tesseract OCR" | convert -pointsize 24 label:@- test.png

# Run OCR
tesseract test.png stdout

# Test Tamil (if you have a Tamil image)
tesseract tamil_image.png stdout -l tam
```

### Test Gemini Connection

```bash
# Run Python test
python -c "
from gemini_embeddings import test_gemini_connection
test_gemini_connection()
"
```

Expected output: `✓ Gemini connection successful`

### Test Neon Connection

```bash
# Run Python test
python -c "
from knowledge_graph import NeonKnowledgeGraph
import os
from dotenv import load_dotenv
load_dotenv()
kg = NeonKnowledgeGraph()
print('✓ Neon connection successful')
stats = kg.get_statistics()
print(f'Entities: {stats[\"entities\"]}, Relationships: {stats[\"relationships\"]}')
kg.close()
"
```

## 🚀 Step 6: Run the Application

```bash
# Make sure you're in the RAG directory
cd /Users/kanda/Learning/GenAI/gen-ai-learning/RAG

# Activate virtual environment if not already active
source .venv/bin/activate  # macOS/Linux

# Run Streamlit app
streamlit run enhanced_rag_chatbot.py
```

The application should open automatically in your browser at `http://localhost:8501`

## 🎯 Step 7: First Use

1. **Initialize System**
   - Click "🔄 Initialize System" in the sidebar
   - Wait for success messages

2. **Upload Test Document**
   - Download a sample PDF or use any document
   - Click "Choose files" in sidebar
   - Select your document
   - Click "📤 Process Files"
   - Wait for processing to complete

3. **Ask a Question**
   - Type a question in the chat input
   - Press Enter
   - View the response with sources and confidence score

## 🐛 Troubleshooting

### Issue: "Tesseract not found"

**Solution**:
```bash
# Find Tesseract location
which tesseract  # macOS/Linux
where tesseract  # Windows

# Add to .env
TESSERACT_CMD=/path/to/tesseract
```

### Issue: "Gemini API error"

**Solutions**:
- Verify API key is correct in `.env`
- Check API key has not expired
- Ensure you have internet connection
- Check Gemini API quota at [Google AI Studio](https://makersuite.google.com)

### Issue: "Neon connection failed"

**Solutions**:
- Verify connection string format
- Ensure database is running (Neon console)
- Check pgvector extension is enabled:
  ```sql
  SELECT * FROM pg_extension WHERE extname = 'vector';
  ```
- Verify SSL mode is included in connection string

### Issue: "Tamil OCR not working"

**Solutions**:
```bash
# Verify Tamil language pack
tesseract --list-langs | grep tam

# If not found, install:
# macOS
brew install tesseract-lang

# Ubuntu
sudo apt-get install tesseract-ocr-tam
```

### Issue: "Module not found" errors

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Or install specific missing module
pip install <module-name>
```

### Issue: "ChromaDB errors"

**Solution**:
```bash
# Clear ChromaDB cache
rm -rf ./chroma_db

# Reinstall ChromaDB
pip uninstall chromadb
pip install chromadb>=0.4.22
```

## 📊 Performance Tips

1. **First Run**: Initial model downloads may take time
2. **OCR Speed**: Large images take longer to process
3. **Batch Upload**: Upload multiple files at once for efficiency
4. **Knowledge Graph**: Disable if not needed for faster responses

## 🔒 Security Best Practices

1. **Never commit `.env`** to version control
2. **Rotate API keys** periodically
3. **Use environment-specific** `.env` files for dev/prod
4. **Limit database access** to specific IPs if possible
5. **Monitor API usage** to avoid unexpected charges

## 📚 Additional Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Neon Documentation](https://neon.tech/docs)
- [Tesseract Documentation](https://tesseract-ocr.github.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)

## 🎓 Next Steps

After successful setup:
1. Upload your own documents
2. Experiment with different question types
3. Try Tamil language documents
4. Explore knowledge graph features
5. Adjust confidence thresholds
6. Customize the UI

## 💡 Tips for Best Results

1. **Document Quality**: Higher quality PDFs and images give better results
2. **Tamil OCR**: Clear, high-resolution images work best
3. **Question Clarity**: Specific questions get better answers
4. **Source Verification**: Always check the sources cited
5. **Confidence Scores**: Pay attention to confidence levels

---

**Need Help?** Check the main [README_ENHANCED_RAG.md](README_ENHANCED_RAG.md) for more details.

**Ready to Start?** Run: `streamlit run enhanced_rag_chatbot.py`
