# GenAI Learning Repository 🚀

A comprehensive collection of Generative AI, Machine Learning, Automation, and Full-Stack Development projects. This repository serves as a hands-on learning journey covering RAG systems, Knowledge Graphs, LangChain, Automation workflows, Web Development, and more.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Categories](#project-categories)
- [AI & Machine Learning Projects](#ai--machine-learning-projects)
- [Automation Projects](#automation-projects)
- [Web Development Projects](#web-development-projects)
- [Python Fundamentals](#python-fundamentals)
- [Setup & Installation](#setup--installation)
- [Contact](#contact)

---

## 🎯 Overview

This repository is organized into multiple subdirectories, each focusing on specific technologies and use cases. Every project includes comprehensive documentation, setup instructions, and practical examples.

### Key Technologies Covered
- 🤖 **RAG Systems** (Retrieval-Augmented Generation)
- 🕸️ **Knowledge Graphs** (Neo4j, Graphiti)
- 🔗 **LangChain** (Document Processing, Embeddings, Vector Stores)
- ⚡ **N8N Automation** (Email, Slack, AI Integration)
- 🌐 **Web Frameworks** (Flask, Streamlit)
- 🎭 **Browser Automation** (Playwright, PyAutoGUI)
- 🧠 **LLM Integration** (OpenAI, Google Gemini, Hugging Face)

---

## 📂 Project Categories

### AI & Machine Learning Projects

| Project | Description | Key Technologies |
|---------|-------------|------------------|
| [`RAG/`](#rag-chatbot) | PDF Question & Answer System with RAG | Streamlit, OpenAI, FAISS, LangChain |
| [`knowledge_graph_rag/`](#knowledge-graph-rag) | KG vs Traditional RAG Comparison | Neo4j, Graphiti, OpenAI, FAISS |
| [`knowlege_graph_assignment/`](#knowledge-graph-assignment) | Hybrid RAG with Vector + Graph Search | Neo4j, Neon DB, OCR, pgvector |
| [`langchain_learning/`](#langchain-learning) | Complete LangChain Tutorial | Document Loaders, Embeddings, Retrievers |
| [`hugging_face/`](#hugging-face-text-generation) | GPT-2 Text Generation | Transformers, PyTorch |
| [`prompt_battle/`](#prompt-battle) | AI Video Generation Project | Google Veo 2.1, JSON Prompts |
| [`prompt_corrective_rag/`](#prompt-corrective-rag) | Corrective RAG Prompting | RAG Optimization |

### Automation Projects

| Project | Description | Key Technologies |
|---------|-------------|------------------|
| [`n8n_automation/`](#n8n-automation-workflows) | Email, Slack, AI Image Automation | N8N, Gmail, Slack, OpenAI, Gemini |
| [`playwright_basics/`](#playwright-basics) | Browser Automation Framework | Playwright (async), pytest |
| [`playwright_assignment/`](#playwright-assignment) | Cricket Scorecard Scraper | Playwright, Bing Search, Screenshots |
| [`pyautogui_assignment/`](#pyautogui-assignment) | WhatsApp Auto-Send Script | PyAutoGUI, pynput |

### Web Development Projects

| Project | Description | Key Technologies |
|---------|-------------|------------------|
| [`streamlit_webapp/`](#streamlit-webapp) | Interactive Web Apps | Streamlit, Calculator, Forms |
| [`streamlit_assignment/`](#streamlit-assignment) | Patient Profile Management | Streamlit, SQLite, CRUD |
| [`flask_app/`](#flask-application) | Flask Web Application | Flask, REST API, JSON |
| [`python_15_days_challenge/`](#python-15-days-challenge) | 15 Streamlit Mini-Projects | Various Streamlit Apps |

### Python Fundamentals

| Project | Description | Focus Areas |
|---------|-------------|-------------|
| [`python_basics/`](#python-basics) | Core Python Examples | Language Features, Testing |

---

## 🤖 AI & Machine Learning Projects

### RAG Chatbot

**Location**: `RAG/`

A powerful PDF Question & Answer system using Retrieval-Augmented Generation.

**Features**:
- PDF upload and processing
- Intelligent Q&A with source citations
- Conversation memory
- Semantic search with FAISS
- Beautiful Streamlit UI

**Tech Stack**: Streamlit, OpenAI GPT-3.5-Turbo, HuggingFace Embeddings, FAISS, LangChain

**Quick Start**:
```bash
cd RAG
pip install -r requirements.txt
streamlit run chatbot.py
```

[📖 Full Documentation](RAG/README.md)

---

### Knowledge Graph RAG

**Location**: `knowledge_graph_rag/`

Comprehensive comparison between Traditional RAG and Knowledge Graph-based RAG systems.

**Features**:
- Side-by-side RAG comparison
- Interactive graph visualization
- Relationship discovery
- Performance metrics analysis
- Neo4j + Graphiti integration

**Tech Stack**: Neo4j, Graphiti, LangChain, OpenAI, FAISS, Docker

**Quick Start**:
```bash
cd knowledge_graph_rag
docker-compose up -d
pip install -r requirements.txt
streamlit run demo.py
```

[📖 Full Documentation](knowledge_graph_rag/README.md)

---

### Knowledge Graph Assignment

**Location**: `knowlege_graph_assignment/`

Advanced Q&A RAG system combining vector search (Neon DB) and knowledge graph (Neo4j).

**Features**:
- Hybrid retrieval (vector + graph)
- PDF processing with OCR support
- Entity-relationship extraction
- Anti-hallucination measures
- Streamlit chatbot UI

**Tech Stack**: Neo4j, Neon DB (pgvector), Tesseract OCR, PyMuPDF, OpenAI

**Quick Start**:
```bash
cd knowlege_graph_assignment
brew install tesseract  # macOS
pip install -r requirements.txt
docker-compose up -d
python setup_databases.py
```

[📖 Full Documentation](knowlege_graph_assignment/README.md)

---

### LangChain Learning

**Location**: `langchain_learning/`

Complete hands-on guide to LangChain covering all core concepts.

**Topics Covered**:
- Document loaders
- Text splitting strategies
- Embeddings (OpenAI, HuggingFace)
- Vector stores (FAISS, Chroma)
- Retrievers and search

**Tech Stack**: LangChain, OpenAI, HuggingFace, FAISS, Chroma

**Quick Start**:
```bash
cd langchain_learning
pip install -r requirements.txt
python data_injustion.py
python retriever.py
```

[📖 Full Documentation](langchain_learning/README.md)

---

### Hugging Face Text Generation

**Location**: `hugging_face/`

Text generation using GPT-2 model from Hugging Face Transformers.

**Features**:
- GPT-2 text generation pipeline
- Customizable prompts
- Adjustable generation parameters

**Tech Stack**: Transformers, PyTorch, GPT-2

**Quick Start**:
```bash
cd hugging_face
pip install transformers torch
python ai_gp2.py
```

[📖 Full Documentation](hugging_face/README.md)

---

### Prompt Battle

**Location**: `prompt_battle/`

Collaborative AI video generation project using Google Veo 2.1.

**Features**:
- 1-minute GenAI learning journey trailer
- JSON-based prompting
- Team collaboration (4 members)
- Segment-by-segment video generation

**Tech Stack**: Google Veo 2.1, JSON Prompts

[📖 Full Documentation](prompt_battle/README.md)

---

### Prompt Corrective RAG

**Location**: `prompt_corrective_rag/`

Experiments with corrective RAG prompting techniques for improved accuracy.

---

## ⚡ Automation Projects

### N8N Automation Workflows

**Location**: `n8n_automation/`

Three production-ready N8N workflows for communication and content automation.

**Workflows**:
1. **Email Automation** - Personalized thank you emails with AI-generated content
2. **Email to Slack** - Customer support ticketing system
3. **Slack Image Generator** - AI-powered promotional poster creation

**Features**:
- Gmail + Google Sheets integration
- Slack notifications and file uploads
- OpenAI GPT-4 content generation
- Google Gemini image generation
- Ticket tracking system

**Tech Stack**: N8N, Gmail API, Slack API, Google Sheets, OpenAI, Google Gemini

**Quick Start**:
```bash
cd n8n_automation
# Import JSON files to N8N instance
# Configure credentials (Gmail, Slack, OpenAI, Gemini)
# Set up Google Sheets as documented
```

**Required Sheets**:
- `trigger_email` - Columns: `Customer Name`, `Email ID`
- `n8n_automation_user_tickets` - Columns: `TicketID`, `CreatedAt`, `From`, `FromEmail`, `Subject`, `Snippet`, `Body`, `Status`

[📖 Full Documentation](n8n_automation/README.md)

---

### Playwright Basics

**Location**: `playwright_basics/`

Browser automation framework using Playwright's async API.

**Features**:
- Async Playwright examples
- Browser interaction utilities
- Form automation
- pytest integration

**Tech Stack**: Playwright, pytest, pytest-asyncio

**Quick Start**:
```bash
cd playwright_basics
pip install playwright pytest pytest-asyncio
playwright install
python examples/browser_example.py
```

[📖 Full Documentation](playwright_basics/README.md)

---

### Playwright Assignment

**Location**: `playwright_assignment/`

Cricket scorecard scraper using Playwright and Bing search.

**Features**:
- Bing search automation
- Smart cricket website detection (Cricbuzz, ESPNcricinfo)
- Cookie consent handling
- Full-page screenshots
- HTML snapshot capture

**Tech Stack**: Playwright, Bing Search

**Quick Start**:
```bash
cd playwright_assignment
pip install -r requirements.txt
playwright install
python src/scorecard.py
```

[📖 Full Documentation](playwright_assignment/README.md)

---

### PyAutoGUI Assignment

**Location**: `pyautogui_assignment/`

WhatsApp auto-send message automation with single-click execution.

**Features**:
- Mouse click detection
- Automated message typing
- WhatsApp Web/Desktop integration
- macOS accessibility integration

**Tech Stack**: PyAutoGUI, pynput, macOS Accessibility

**Quick Start**:
```bash
cd pyautogui_assignment
pip install -r requirements.txt
# Grant accessibility permissions
python src/main.py
```

[📖 Full Documentation](pyautogui_assignment/README.md)

---

## 🌐 Web Development Projects

### Streamlit WebApp

**Location**: `streamlit_webapp/`

Interactive web applications demonstrating Streamlit fundamentals.

**Applications**:
1. **Hello World App** - Basic greeting with user input
2. **Calculator App** - Full-featured calculator with error handling

**Tech Stack**: Streamlit

**Quick Start**:
```bash
cd streamlit_webapp
pip install -r requirements.txt
streamlit run src/myapp.py
streamlit run src/calculator.py
```

[📖 Full Documentation](streamlit_webapp/README.md)

---

### Streamlit Assignment

**Location**: `streamlit_assignment/`

KaviHealthCare - Professional patient profile management system.

**Features**:
- Complete CRUD operations
- Advanced search and filtering
- CSV import/export
- Email and phone validation
- SQLite persistence
- Modular database architecture

**Tech Stack**: Streamlit, SQLite, pytest

**Quick Start**:
```bash
cd streamlit_assignment
pip install -r requirements.txt
streamlit run src/kavihealthcare.py
pytest tests/  # Run 30+ tests
```

[📖 Full Documentation](streamlit_assignment/README.md)

---

### Flask Application

**Location**: `flask_app/`

Lightweight Flask web application demonstrating REST API fundamentals.

**Features**:
- Route definitions
- JSON responses
- URL and query parameters
- Development server

**Tech Stack**: Flask

**Quick Start**:
```bash
cd flask_app
pip install -r requirements.txt
python app.py
```

[📖 Full Documentation](flask_app/README.md)

---

### Python 15 Days Challenge

**Location**: `python_15_days_challenge/`

Collection of 15 bite-sized Streamlit projects for daily practice.

**Completed Projects** (7/15):
1. ✅ Greeting Form
2. ✅ Expense Splitter
3. ✅ Modern Calculator
4. ✅ BMI Calculator
5. ✅ Unit Converter
6. ✅ Water Intake Tracker
7. ✅ Gym Workout Logger

**Tech Stack**: Streamlit, Plotly, JSON persistence

**Quick Start**:
```bash
cd python_15_days_challenge
pip install -r requirements.txt
streamlit run Day7/gym_workout_logger/app.py
```

[📖 Full Documentation](python_15_days_challenge/README.md)

---

## 🐍 Python Fundamentals

### Python Basics

**Location**: `python_basics/`

Core Python examples, exercises, and tests for learning language fundamentals.

**Features**:
- Language feature demonstrations
- Small utility examples
- Comprehensive test coverage
- Clean code practices

**Quick Start**:
```bash
cd python_basics
PYTHONPATH=./src pytest -q
PYTHONPATH=./src python examples/hello.py
```

[📖 Full Documentation](python_basics/README.md)

---

## 🚀 Setup & Installation

### General Setup

Most projects follow this pattern:

```bash
# Navigate to project directory
cd <project_name>

# Create virtual environment
python -m venv .venv

# Activate virtual environment (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Common Requirements

- **Python**: 3.9+ (3.11+ recommended)
- **Virtual Environment**: Recommended for all projects
- **API Keys**: OpenAI, Google Gemini (for AI projects)
- **Docker**: For Neo4j-based projects
- **Playwright**: `playwright install` for browser automation

### Environment Variables

Create `.env` files in project directories as needed:

```bash
# OpenAI
OPENAI_API_KEY=your_key_here

# Google Gemini
GOOGLE_API_KEY=your_key_here

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password

# Neon DB
DATABASE_URL=postgresql://...
```

---

## 📖 Documentation Standards

Each project directory contains:
- `README.md` - Comprehensive documentation
- `requirements.txt` - Python dependencies
- `src/` - Source code (where applicable)
- `tests/` - Test suites (where applicable)

---

## 🔧 Common Commands Reference

### Python & Virtual Environments
```bash
python -m venv .venv                    # Create virtual environment
source .venv/bin/activate               # Activate (macOS/Linux)
pip install -r requirements.txt         # Install dependencies
pip freeze > requirements.txt           # Save dependencies
```

### Streamlit
```bash
streamlit run app.py                    # Run Streamlit app
streamlit run app.py --server.port 8502 # Custom port
```

### Playwright
```bash
playwright install                      # Install browsers
playwright codegen                      # Record interactions
```

### Docker (Neo4j Projects)
```bash
docker-compose up -d                    # Start services
docker-compose down                     # Stop services
docker-compose logs -f                  # View logs
```

### Testing
```bash
pytest                                  # Run all tests
pytest -v                               # Verbose output
pytest tests/test_file.py               # Specific test file
PYTHONPATH=./src pytest                 # With custom Python path
```

---

## 🎯 Learning Path Recommendations

### Beginner Path
1. Start with `python_basics/` - Core Python fundamentals
2. Explore `streamlit_webapp/` - Simple web apps
3. Try `flask_app/` - REST API basics
4. Complete `python_15_days_challenge/` - Daily practice

### AI/ML Path
1. Begin with `hugging_face/` - Text generation basics
2. Progress to `RAG/` - RAG fundamentals
3. Study `langchain_learning/` - LangChain framework
4. Advance to `knowledge_graph_rag/` - Graph-based RAG
5. Master `knowlege_graph_assignment/` - Hybrid systems

### Automation Path
1. Learn `playwright_basics/` - Browser automation
2. Build `playwright_assignment/` - Real-world scraping
3. Try `pyautogui_assignment/` - Desktop automation
4. Implement `n8n_automation/` - Workflow automation

### Full-Stack Path
1. Master `flask_app/` - Backend basics
2. Build `streamlit_assignment/` - Full CRUD app
3. Integrate with `RAG/` - AI-powered apps
4. Deploy with `n8n_automation/` - Production workflows

---

## 🤝 Contributing

This is a personal learning repository, but suggestions and improvements are welcome!

**To suggest improvements**:
1. Review the project structure
2. Check existing documentation
3. Open an issue with detailed suggestions
4. Submit pull requests with clear descriptions

---

## 📝 Notes

- **PYTHONPATH**: Many examples assume `PYTHONPATH=./src` when run from project root
- **Virtual Environments**: Always use virtual environments for dependency isolation
- **API Keys**: Never commit API keys - use `.env` files (add to `.gitignore`)
- **Browser Binaries**: Playwright requires `playwright install` for browser automation
- **Database Setup**: Neo4j and PostgreSQL projects require Docker or external services

---

## 🔍 Project Status

| Category | Total Projects | Status |
|----------|----------------|--------|
| AI & ML | 7 | ✅ Active |
| Automation | 4 | ✅ Active |
| Web Development | 4 | ✅ Active |
| Python Fundamentals | 1 | ✅ Active |
| **Total** | **16** | **✅ Active** |

---

## ⚠️ Troubleshooting

### Import Errors
```bash
# Set PYTHONPATH
export PYTHONPATH=./src

# Or install in editable mode
pip install -e .
```

### Playwright Issues
- **Browser crashes**: Run in headed mode (remove `headless=True`)
- **Timeouts**: Increase timeout values in scripts
- **Version conflicts**: Try upgrading/downgrading Playwright

### Async/Event Loop Errors
- Ensure `pytest-asyncio` is installed
- Use async APIs consistently
- Check `playwright_basics/README.md` for pytest configuration

### Database Connection Issues
- **Neo4j**: Verify Docker container is running (`docker ps`)
- **PostgreSQL/Neon**: Check connection string and credentials
- **SQLite**: Verify file permissions

### API Key Errors
- Check `.env` file exists and has correct keys
- Verify API key validity and quota limits
- Ensure `.env` is not in `.gitignore` conflicts

### Streamlit Issues
```bash
# Clear cache
streamlit cache clear

# Check port availability
lsof -i :8501

# Use different port
streamlit run app.py --server.port 8502
```

---

## 🏆 Project Highlights

### Most Complex Projects
1. **Knowledge Graph RAG** - Full graph database integration
2. **Knowledge Graph Assignment** - Hybrid retrieval system
3. **N8N Automation** - Multi-service orchestration

### Best for Learning
1. **LangChain Learning** - Comprehensive tutorials
2. **Python 15 Days Challenge** - Incremental skill building
3. **RAG Chatbot** - Clear RAG implementation

### Production Ready
1. **Streamlit Assignment** - Full CRUD app with tests
2. **N8N Automation** - Enterprise workflow automation
3. **Playwright Assignment** - Robust web scraping

---

## 📚 Additional Resources

### Official Documentation
- [OpenAI API](https://platform.openai.com/docs)
- [LangChain](https://python.langchain.com/)
- [Streamlit](https://docs.streamlit.io/)
- [Playwright](https://playwright.dev/python/)
- [Neo4j](https://neo4j.com/docs/)
- [N8N](https://docs.n8n.io/)

### Community & Support
- [LangChain Discord](https://discord.gg/langchain)
- [Streamlit Forum](https://discuss.streamlit.io/)
- [Playwright Discord](https://discord.gg/playwright)

---

## 📊 Repository Statistics

- **Lines of Code**: 10,000+
- **Documentation Pages**: 16 comprehensive READMEs
- **Test Coverage**: 30+ tests in key projects
- **Technologies**: 20+ frameworks and tools
- **Last Updated**: December 7, 2025

---

## 🎓 Skills Demonstrated

### AI & Machine Learning
- RAG system implementation
- Knowledge graph construction
- Vector embeddings and similarity search
- LLM integration (OpenAI, Gemini)
- Prompt engineering

### Backend Development
- Flask REST APIs
- SQLite database management
- PostgreSQL with pgvector
- Neo4j graph databases
- Data validation and error handling

### Frontend Development
- Streamlit interactive UIs
- Responsive design
- Real-time data visualization
- Form handling and validation
- Chart integration (Plotly)

### Automation & DevOps
- Browser automation (Playwright)
- Desktop automation (PyAutoGUI)
- Workflow orchestration (N8N)
- Docker containerization
- CI/CD concepts

### Software Engineering
- Modular architecture
- Test-driven development (pytest)
- Documentation best practices
- Version control (Git)
- Environment management

---

## 🔮 Future Enhancements

### Planned Projects
- [ ] LangGraph implementation
- [ ] Multi-agent systems
- [ ] FastAPI microservices
- [ ] React + Streamlit integration
- [ ] Advanced prompt engineering
- [ ] Fine-tuning experiments
- [ ] Vector database comparisons
- [ ] Complete Python 15 Days Challenge (8 more projects)

### Improvements
- [ ] Add CI/CD pipelines
- [ ] Containerize all applications
- [ ] Add performance benchmarks
- [ ] Create video tutorials
- [ ] Add API documentation (Swagger)
- [ ] Implement monitoring/logging
- [ ] Add security best practices guide

---

## 📧 Contact & Support

**Repository Maintainer**: kandas22@gmail.com

### Get Help
- 📖 Check project-specific README files
- 🐛 Open an issue for bugs
- 💡 Submit feature requests
- 🤝 Contribute improvements via pull requests

### Connect
- **GitHub**: [@kandas22](https://github.com/kandas22)
- **Email**: kandas22@gmail.com

---

## 📄 License

This repository is for educational purposes. Individual projects may have specific licenses. Please check project directories for details.

---

## ⭐ Acknowledgments

Special thanks to:
- OpenAI for GPT models and APIs
- LangChain community for excellent frameworks
- Streamlit team for amazing web framework
- Neo4j for graph database technology
- Hugging Face for transformer models
- N8N for workflow automation tools

---

## 🚀 Quick Start Summary

```bash
# Clone repository
git clone https://github.com/kandas22/gen-ai-learning.git
cd gen-ai-learning

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install common dependencies
pip install -r requirements.txt

# Navigate to any project
cd RAG/  # or any other project directory

# Follow project-specific README
cat README.md
```

---

**Happy Learning! 🎉**

For detailed instructions, always refer to individual project README files. Each project is self-contained with comprehensive documentation, examples, and setup guides.
