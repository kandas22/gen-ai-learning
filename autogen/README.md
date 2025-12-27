# SEO Content Generator - Restructured

## 🎯 Features

- ✅ Multi-agent workflow orchestration
- ✅ Circular progress indicators
- ✅ Round-robin agent visualization
- ✅ SEO-optimized content generation (1500+ words)
- ✅ Automated research and verification
- ✅ Email delivery support

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

## 🚀 Usage

```bash
streamlit run app.py
```

Access at: http://localhost:8501

## 📁 Structure

```
├── app.py                  # Main application
├── config.py               # Configuration
├── core/                   # Core logic
│   ├── workflow.py        # Orchestration
│   ├── agents.py          # Agent management
│   └── seo_scoring.py     # SEO analysis
├── tools/                  # Utilities
│   ├── search.py          # Web search
│   ├── email_sender.py    # Email delivery
│   └── formatters.py      # Output formatting
├── ui/                     # User interface
│   ├── components.py      # UI components
│   └── styles.py          # CSS styling
└── utils/                  # Helpers
    ├── helpers.py         # General utilities
    └── keywords.py        # Keyword extraction
```

## 🔑 Configuration

Required environment variables:
- `OPENAI_API_KEY` - OpenAI API key
- `SERPAPI_API_KEY` - SerpAPI key for web search
- `SMTP_USERNAME` - Email address (optional)
- `SMTP_PASSWORD` - Email password (optional)

## 📊 Field Selection

- **Any (General Content)** - Broader research, diverse keywords
- **Technology** - Tech-focused content
- **Healthcare** - Medical/health content
- **Finance** - Financial content
- And more...

## 🎨 UI Features

- Circular progress indicator (left)
- Round-robin orchestrator display (right)
- Settings menu (top)
- Real-time status updates
- Result tabs with download options

## 📝 License

MIT License
