# 🤖 AI Prompt Generator

A beautiful Streamlit application for generating structured AI prompts with optional RAG (Retrieval-Augmented Generation) integration.

## Features

- **Custom Prompt Generation**: Create tailored prompts based on task descriptions
- **RAG Integration**: Optional RAG configuration with multiple types:
  - Vector Database (Pinecone, Weaviate, Chroma, FAISS, Milvus)
  - Document Retrieval (PDF, Word, Text Files, Web Pages, Markdown)
  - Knowledge Graph (Neo4j, Amazon Neptune, GraphDB)
  - Hybrid Search (Vector + Keyword, Semantic + BM25, Multi-modal)
- **Customization Options**:
  - Multiple tone selections (Professional, Casual, Technical, Creative, Academic, Friendly)
  - Various output formats (Paragraph, Bullet Points, JSON, Markdown, Code)
  - Additional custom instructions
- **Secure API Key Input**: Password-protected API key field
- **Beautiful UI**: Modern gradient design with smooth animations
- **Export Options**: Download generated prompts as text files

## Installation

1. **Install Streamlit**:
```bash
pip install streamlit
```

## Usage

1. **Run the application**:
```bash
streamlit run prompt_generator_app.py
```

2. **Configure your settings**:
   - Enter your API key in the sidebar (required)
   - Fill in the task description
   - Add context if needed
   - Select tone and output format

3. **Optional RAG Configuration**:
   - Check "Enable RAG" if you want retrieval capabilities
   - Select RAG type
   - Choose specific options for your RAG type

4. **Generate Prompt**:
   - Click "Generate Prompt" button
   - View your generated prompt
   - Copy or download the prompt

## Example Use Cases

- **Research Assistant**: Generate prompts for answering questions with document retrieval
- **Code Generation**: Create prompts for technical code generation tasks
- **Content Creation**: Build prompts for creative writing with specific tones
- **Data Analysis**: Generate prompts for analyzing data with structured outputs

## Screenshots

The application features a modern, gradient-based UI with:
- Purple gradient background
- Clean white cards for content
- Smooth hover effects on buttons
- Responsive two-column layout

## Requirements

- Python 3.7+
- Streamlit

## License

MIT License
