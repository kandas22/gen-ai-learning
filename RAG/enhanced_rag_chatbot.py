"""
Enhanced RAG Chatbot with Knowledge Graph and OCR

Features:
- Document upload (PDF, images, text files)
- OCR with Tamil language support
- Gemini embeddings for multilingual support
- Knowledge graph integration with Neon PostgreSQL
- Hallucination prevention with source attribution
- Beautiful Streamlit UI
"""

import streamlit as st
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from dotenv import load_dotenv
from typing import List, Dict, Optional
import tempfile
from pathlib import Path
import base64

# Import custom modules
from document_processor import DocumentProcessor, is_supported_file, get_supported_extensions
from gemini_embeddings import GeminiEmbeddings, GeminiLLM, test_gemini_connection
from knowledge_graph import NeonKnowledgeGraph, EntityExtractor, build_knowledge_graph_from_documents

# Import LangChain components
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Enhanced RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .upload-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        padding: 2rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .confidence-high {
        color: #10b981;
        font-weight: bold;
    }
    
    .confidence-medium {
        color: #f59e0b;
        font-weight: bold;
    }
    
    .confidence-low {
        color: #ef4444;
        font-weight: bold;
    }
    
    .source-citation {
        background: rgba(102, 126, 234, 0.1);
        padding: 0.5rem;
        border-left: 3px solid #667eea;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
        font-size: 0.9rem;
    }
    
    .ocr-image {
        max-width: 100%;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .entity-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'knowledge_graph' not in st.session_state:
    st.session_state.knowledge_graph = None
if 'processed_documents' not in st.session_state:
    st.session_state.processed_documents = []
if 'embeddings' not in st.session_state:
    st.session_state.embeddings = None
if 'llm' not in st.session_state:
    st.session_state.llm = None
if 'doc_processor' not in st.session_state:
    st.session_state.doc_processor = None
if 'entity_extractor' not in st.session_state:
    st.session_state.entity_extractor = None


def initialize_components():
    """Initialize all RAG components"""
    try:
        # Initialize embeddings
        if st.session_state.embeddings is None:
            with st.spinner("Initializing Gemini embeddings..."):
                st.session_state.embeddings = GeminiEmbeddings()
                st.success("✓ Gemini embeddings initialized")
        
        # Initialize LLM
        if st.session_state.llm is None:
            with st.spinner("Initializing Gemini LLM..."):
                # Model name will be read from GEMINI_MODEL_NAME env var
                st.session_state.llm = GeminiLLM(
                    temperature=0.7
                )
                st.success("✓ Gemini LLM initialized")
        
        # Initialize document processor
        if st.session_state.doc_processor is None:
            with st.spinner("Initializing document processor..."):
                st.session_state.doc_processor = DocumentProcessor(
                    chunk_size=int(os.getenv('CHUNK_SIZE', 1000)),
                    chunk_overlap=int(os.getenv('CHUNK_OVERLAP', 200)),
                    ocr_languages=['eng', 'tam']  # English and Tamil
                )
                st.success("✓ Document processor initialized")
        
        # Initialize knowledge graph if enabled
        enable_kg = os.getenv('ENABLE_KNOWLEDGE_GRAPH', 'true').lower() == 'true'
        if enable_kg and st.session_state.knowledge_graph is None:
            neon_url = os.getenv('NEON_DATABASE_URL')
            if neon_url:
                try:
                    with st.spinner("Connecting to Neon knowledge graph..."):
                        st.session_state.knowledge_graph = NeonKnowledgeGraph(neon_url)
                        st.session_state.entity_extractor = EntityExtractor()
                        st.success("✓ Knowledge graph connected")
                except Exception as e:
                    st.warning(f"Knowledge graph not available: {e}")
            else:
                st.info("ℹ️ Knowledge graph disabled (no NEON_DATABASE_URL)")
        
        return True
        
    except Exception as e:
        st.error(f"Error initializing components: {e}")
        return False


def process_uploaded_files(uploaded_files):
    """Process uploaded files and add to vector store"""
    if not uploaded_files:
        return
    
    all_chunks = []
    all_images = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            # Process document
            processed_doc = st.session_state.doc_processor.process_document(tmp_path)
            
            # Store processed document
            st.session_state.processed_documents.append({
                'name': uploaded_file.name,
                'source': tmp_path,
                'text': processed_doc.text,
                'chunks': processed_doc.chunks,
                'images': processed_doc.images,
                'metadata': processed_doc.metadata
            })
            
            # Collect chunks for vector store
            all_chunks.extend(processed_doc.chunks)
            all_images.extend(processed_doc.images)
            
            # Build knowledge graph if enabled
            if st.session_state.knowledge_graph and st.session_state.entity_extractor:
                if processed_doc.text.strip():
                    try:
                        docs_for_kg = [{
                            'text': processed_doc.text,
                            'source': uploaded_file.name
                        }]
                        build_knowledge_graph_from_documents(
                            docs_for_kg,
                            st.session_state.knowledge_graph,
                            st.session_state.entity_extractor
                        )
                    except Exception as e:
                        st.warning(f"Could not build knowledge graph for {uploaded_file.name}: {e}")
            
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        progress_bar.progress((idx + 1) / len(uploaded_files))
    
    status_text.text("Creating vector store...")
    
    # Create vector store from chunks
    if all_chunks:
        documents = []
        for chunk in all_chunks:
            documents.append(Document(
                page_content=chunk['text'],
                metadata=chunk['metadata']
            ))
        
        # Create or update vector store
        if st.session_state.vectorstore is None:
            st.session_state.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=st.session_state.embeddings,
                collection_name="enhanced_rag"
            )
        else:
            st.session_state.vectorstore.add_documents(documents)
    
    progress_bar.empty()
    status_text.empty()
    
    st.success(f"✓ Processed {len(uploaded_files)} file(s), {len(all_chunks)} chunks, {len(all_images)} images")


def query_with_sources(query: str, use_kg: bool = False):
    """Query the RAG system with source attribution"""
    if st.session_state.vectorstore is None:
        return {
            'answer': "Please upload documents first!",
            'sources': [],
            'confidence': 0.0,
            'has_answer': False
        }
    
    # Retrieve relevant documents
    k = int(os.getenv('RETRIEVAL_K', 5))
    docs_with_scores = st.session_state.vectorstore.similarity_search_with_score(query, k=k)
    
    # Prepare contexts with scores
    contexts = []
    for doc, score in docs_with_scores:
        # Convert distance to similarity (lower distance = higher similarity)
        similarity = 1.0 / (1.0 + score)
        contexts.append({
            'text': doc.page_content,
            'source': doc.metadata.get('source', 'Unknown'),
            'score': similarity,
            'chunk_index': doc.metadata.get('chunk_index', 0)
        })
    
    # Enhance with knowledge graph if enabled
    kg_context = ""
    if use_kg and st.session_state.knowledge_graph:
        try:
            # Search for relevant entities
            entities = st.session_state.knowledge_graph.search_entities(query, limit=5)
            if entities:
                kg_context = "\n\nRelated Entities from Knowledge Graph:\n"
                for entity in entities:
                    kg_context += f"- {entity['name']} ({entity['type']}): {entity['description']}\n"
                    
                    # Get related entities
                    related = st.session_state.knowledge_graph.get_related_entities(entity['name'], max_depth=1)
                    if related:
                        kg_context += f"  Related to: {', '.join([r['entity_name'] for r in related[:3]])}\n"
        except Exception as e:
            st.warning(f"Knowledge graph query failed: {e}")
    
    # Add KG context to first context if available
    if kg_context and contexts:
        contexts[0]['text'] += kg_context
    
    # Generate response with sources
    min_confidence = float(os.getenv('MIN_CONFIDENCE_THRESHOLD', 0.6))
    result = st.session_state.llm.generate_with_sources(query, contexts, min_confidence)
    
    return result


# Main UI
st.markdown('<h1 class="main-header">🤖 Enhanced RAG Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">With Knowledge Graph, OCR & Tamil Language Support</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Initialize button
    if st.button("🔄 Initialize System", use_container_width=True):
        initialize_components()
    
    st.divider()
    
    # Document Upload Section
    st.header("📁 Upload Documents")
    
    supported_exts = get_supported_extensions()
    st.caption(f"Supported: {', '.join(supported_exts)}")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=[ext.replace('.', '') for ext in supported_exts],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files and st.button("📤 Process Files", use_container_width=True):
        if st.session_state.doc_processor is None:
            st.error("Please initialize the system first!")
        else:
            process_uploaded_files(uploaded_files)
    
    st.divider()
    
    # Settings
    st.header("🎛️ Settings")
    
    use_knowledge_graph = st.checkbox(
        "Use Knowledge Graph",
        value=True,
        disabled=st.session_state.knowledge_graph is None,
        help="Enhance responses with knowledge graph relationships"
    )
    
    show_confidence = st.checkbox(
        "Show Confidence Scores",
        value=True,
        help="Display confidence scores for responses"
    )
    
    show_sources = st.checkbox(
        "Show Sources",
        value=True,
        help="Display source citations"
    )
    
    st.divider()
    
    # Statistics
    st.header("📊 Statistics")
    
    if st.session_state.vectorstore:
        st.metric("Documents Processed", len(st.session_state.processed_documents))
        
        total_chunks = sum(len(doc['chunks']) for doc in st.session_state.processed_documents)
        st.metric("Total Chunks", total_chunks)
        
        total_images = sum(len(doc['images']) for doc in st.session_state.processed_documents)
        st.metric("Images with OCR", total_images)
    
    if st.session_state.knowledge_graph:
        try:
            kg_stats = st.session_state.knowledge_graph.get_statistics()
            st.metric("Entities", kg_stats['entities'])
            st.metric("Relationships", kg_stats['relationships'])
        except:
            pass
    
    st.divider()
    
    # Clear data
    if st.button("🗑️ Clear All Data", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.processed_documents = []
        st.session_state.vectorstore = None
        st.rerun()

# Main chat interface
st.header("💬 Chat")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.write(message['content'])
        
        # Show metadata if available
        if 'metadata' in message and message['metadata']:
            metadata = message['metadata']
            
            # Confidence score
            if show_confidence and 'confidence' in metadata:
                confidence = metadata['confidence']
                if confidence >= 0.7:
                    conf_class = "confidence-high"
                elif confidence >= 0.5:
                    conf_class = "confidence-medium"
                else:
                    conf_class = "confidence-low"
                
                st.markdown(
                    f'<p class="{conf_class}">Confidence: {confidence:.2%}</p>',
                    unsafe_allow_html=True
                )
            
            # Sources
            if show_sources and 'sources' in metadata:
                with st.expander("📚 Sources"):
                    for source in metadata['sources']:
                        st.markdown(
                            f'<div class="source-citation">'
                            f'[{source["index"]}] {source["source"]} '
                            f'(relevance: {source["score"]:.2%})'
                            f'</div>',
                            unsafe_allow_html=True
                        )

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.chat_history.append({
        'role': 'user',
        'content': prompt
    })
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = query_with_sources(prompt, use_kg=use_knowledge_graph)
            
            st.write(result['answer'])
            
            # Store assistant message with metadata
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': result['answer'],
                'metadata': {
                    'confidence': result['confidence'],
                    'sources': result['sources'],
                    'has_answer': result['has_answer']
                }
            })
            
            # Show confidence
            if show_confidence:
                confidence = result['confidence']
                if confidence >= 0.7:
                    conf_class = "confidence-high"
                elif confidence >= 0.5:
                    conf_class = "confidence-medium"
                else:
                    conf_class = "confidence-low"
                
                st.markdown(
                    f'<p class="{conf_class}">Confidence: {confidence:.2%}</p>',
                    unsafe_allow_html=True
                )
            
            # Show sources
            if show_sources and result['sources']:
                with st.expander("📚 Sources"):
                    for source in result['sources']:
                        st.markdown(
                            f'<div class="source-citation">'
                            f'[{source["index"]}] {source["source"]} '
                            f'(relevance: {source["score"]:.2%})'
                            f'</div>',
                            unsafe_allow_html=True
                        )

# Footer
st.divider()
st.caption("🚀 Enhanced RAG Chatbot with Gemini AI, Knowledge Graph & OCR | Built with ❤️")
