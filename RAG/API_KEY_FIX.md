# 🔑 Gemini API Key Configuration Guide

## Issue: API Key Not Valid

You're seeing: `400 API key not valid. Please pass a valid API key.`

This means your Gemini API key is either:
1. Not set correctly in `.env`
2. Invalid or expired
3. Not activated

## ✅ Solution: Get a Valid API Key

### Step 1: Get Your Gemini API Key

1. **Go to Google AI Studio**: https://makersuite.google.com/app/apikey

2. **Sign in** with your Google account

3. **Click "Create API Key"**

4. **Copy the API key** (starts with `AIza...`)

### Step 2: Add to `.env` File

1. **Open your `.env` file**:
   ```bash
   nano /Users/kanda/Learning/GenAI/gen-ai-learning/RAG/.env
   ```

2. **Add or update these lines**:
   ```env
   # Gemini API Configuration
   GEMINI_API_KEY=AIza...your-actual-key-here
   GEMINI_MODEL_NAME=gemini-2.0-flash-exp
   ```

3. **Save the file** (Ctrl+O, Enter, Ctrl+X in nano)

### Step 3: Verify API Key

Test your API key:

```bash
cd /Users/kanda/Learning/GenAI/gen-ai-learning/RAG
python -c "
from gemini_embeddings import test_gemini_connection
test_gemini_connection()
"
```

Should output: `✓ Gemini connection successful`

## 📝 Model Configuration

The system now reads the model name from `.env`:

```env
# Available models:
GEMINI_MODEL_NAME=gemini-2.0-flash-exp    # Latest experimental (recommended)
# GEMINI_MODEL_NAME=gemini-1.5-flash      # Stable, fast
# GEMINI_MODEL_NAME=gemini-1.5-pro        # High quality
# GEMINI_MODEL_NAME=gemini-pro            # Fallback
```

## 🔍 Check Your Current `.env`

View your current configuration:

```bash
cat /Users/kanda/Learning/GenAI/gen-ai-learning/RAG/.env | grep GEMINI
```

Should show:
```
GEMINI_API_KEY=AIza...
GEMINI_MODEL_NAME=gemini-2.0-flash-exp
```

## ⚠️ Important Notes

### API Key Format
- **Correct**: `GEMINI_API_KEY=AIzaSyABC123...` (no quotes, no spaces)
- **Wrong**: `GEMINI_API_KEY="AIzaSyABC123..."` (has quotes)
- **Wrong**: `GEMINI_API_KEY = AIzaSyABC123...` (has spaces)

### Security
- **Never share** your API key
- **Never commit** `.env` to git
- **Rotate keys** if exposed

### Free Tier Limits
- **Embeddings**: 1,500 requests/day
- **Text Generation**: 60 requests/minute
- **Upgrade**: Enable billing for higher limits

## 🚀 Quick Fix Steps

1. **Get new API key**: https://makersuite.google.com/app/apikey

2. **Update `.env`**:
   ```bash
   echo "GEMINI_API_KEY=your-new-key-here" > /Users/kanda/Learning/GenAI/gen-ai-learning/RAG/.env
   echo "GEMINI_MODEL_NAME=gemini-2.0-flash-exp" >> /Users/kanda/Learning/GenAI/gen-ai-learning/RAG/.env
   ```

3. **Restart Streamlit**:
   ```bash
   streamlit run enhanced_rag_chatbot.py
   ```

## 📊 Available Models

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| `gemini-2.0-flash-exp` | ⚡⚡⚡ | ⭐⭐⭐ | 💰 | Latest experimental |
| `gemini-1.5-flash` | ⚡⚡⚡ | ⭐⭐ | 💰 | Production stable |
| `gemini-1.5-pro` | ⚡⚡ | ⭐⭐⭐⭐ | 💰💰 | High quality |
| `gemini-pro` | ⚡⚡ | ⭐⭐⭐ | 💰 | Fallback |

## ✅ Verification Checklist

- [ ] API key obtained from Google AI Studio
- [ ] API key added to `.env` file (no quotes, no spaces)
- [ ] Model name set in `.env` file
- [ ] `.env` file saved
- [ ] Test connection successful
- [ ] Streamlit restarted

---

**After fixing, restart Streamlit and try uploading a document again!**
