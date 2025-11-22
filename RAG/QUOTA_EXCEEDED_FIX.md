# 🚨 Gemini API Quota Exceeded - Solutions

## Problem

You're seeing this error:
```
429 You exceeded your current quota, please check your plan and billing details.
Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests
```

## What This Means

You've hit the **Gemini API free tier daily limit** for embeddings. This happens when processing large files or multiple documents.

## ✅ Immediate Solutions

### Option 1: Wait for Quota Reset (Free)
- **Free tier resets**: Every 24 hours
- **Wait time**: Check your usage at https://ai.dev/usage?tab=rate-limit
- **Cost**: $0

### Option 2: Use OpenAI Embeddings (Paid Alternative)
Switch to OpenAI embeddings which have higher limits:

1. **Get OpenAI API Key**: https://platform.openai.com/api-keys

2. **Add to `.env`**:
   ```env
   OPENAI_API_KEY=sk-your-key-here
   USE_OPENAI_EMBEDDINGS=true
   ```

3. **Install OpenAI**:
   ```bash
   pip install openai
   ```

4. **Update code** to use OpenAI embeddings when quota exceeded

### Option 3: Upgrade Gemini API (Recommended for Production)
- **Enable billing**: https://console.cloud.google.com/billing
- **Much higher limits**: 1500 requests/minute
- **Cost**: Pay-as-you-go (very affordable)
- **Pricing**: ~$0.00025 per 1000 tokens

## 🔧 Temporary Workaround

### Disable Knowledge Graph (Saves API Calls)

In `.env`:
```env
ENABLE_KNOWLEDGE_GRAPH=false
```

This will:
- Skip entity extraction (saves Gemini calls)
- Only use embeddings for RAG
- Reduce API usage by ~50%

### Process Smaller Batches

In `.env`:
```env
# Reduce chunk size to create fewer embeddings
CHUNK_SIZE=2000

# Process fewer pages
MAX_PAGES_TOTAL=50
```

## 📊 Gemini Free Tier Limits

| Resource | Free Tier Limit |
|----------|----------------|
| Embeddings | 1,500/day |
| Text Generation | 60 requests/minute |
| Total Tokens | Limited |

Your 72MB PDF with 144 pages created **45 chunks**, which requires:
- 45 embedding calls (for chunks)
- Entity extraction calls (if KG enabled)
- Query embedding calls

## 💰 Cost Comparison

### Gemini API (Paid)
- **Embeddings**: $0.00025/1K tokens
- **Generation**: $0.00025/1K tokens (flash)
- **Your 72MB PDF**: ~$0.05-0.10

### OpenAI API
- **Embeddings**: $0.0001/1K tokens (text-embedding-3-small)
- **Generation**: $0.0005/1K tokens (gpt-3.5-turbo)
- **Your 72MB PDF**: ~$0.08-0.15

## 🎯 Recommended Action Plan

### For Testing (Now)
1. **Wait 24 hours** for quota reset
2. **Disable knowledge graph** temporarily
3. **Process smaller files** (<10MB)

### For Production (Long-term)
1. **Enable Gemini billing** ($0.35/month minimum)
2. **Set budget alerts** in Google Cloud Console
3. **Monitor usage** at https://ai.dev/usage

## 🔍 Check Your Current Usage

Visit: https://ai.dev/usage?tab=rate-limit

You'll see:
- Current quota usage
- When quota resets
- Rate limit details

## ⚙️ Quick Fix Configuration

Add to your `.env` file:

```env
# Disable features to reduce API usage
ENABLE_KNOWLEDGE_GRAPH=false
ENABLE_OCR_FOR_LARGE_FILES=false

# Reduce processing
CHUNK_SIZE=3000
MAX_PAGES_TOTAL=50

# Use fallback when quota exceeded
ENABLE_FALLBACK_MODE=true
```

## 🐛 Model Name Issue (Also Fixed)

The model name error is also fixed:
- ✅ Changed from `gemini-1.5-flash-latest` to `gemini-1.5-flash`
- ✅ Added fallback to `gemini-pro`
- ✅ Better error handling

## 📝 Summary

**Immediate**: Disable knowledge graph and wait for quota reset
**Short-term**: Process smaller files or fewer pages
**Long-term**: Enable billing for production use (~$0.35/month)

---

**Next Steps**:
1. Update `.env` with `ENABLE_KNOWLEDGE_GRAPH=false`
2. Restart Streamlit
3. Try processing a smaller file (<10MB)
4. Consider enabling billing for production

**Cost**: Enabling billing costs ~$0.35/month minimum, but actual usage for your PDFs would be ~$0.05-0.10 per 70MB file.
