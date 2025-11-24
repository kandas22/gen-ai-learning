"""
Main Streamlit application for Q&A RAG system.
"""

import os
import sys
from pathlib import Path

# Load environment variables FIRST before any other imports
from dotenv import load_dotenv

# Get the project root directory
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'

# Load .env file
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✓ Loaded environment from: {env_path}")
else:
    print(f"⚠ Warning: .env file not found at {env_path}")
    print("Please create a .env file with your configuration.")

# Add parent directory to path
sys.path.append(str(project_root))

# Now import other modules (they will use the loaded environment variables)
from utils.logger import get_logger

# Validate critical environment variables
required_vars = ['LLM_PROVIDER']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"⚠ Warning: Missing environment variables: {', '.join(missing_vars)}")
    print("Please check your .env file")

# Import settings after environment is loaded
from config import settings

# Import streamlit after environment is loaded
import streamlit as st

logger = get_logger(__name__)

# Display environment status in console
print("=" * 60)
print("RAG System Starting...")
print("=" * 60)
print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
print(f"LLM Provider: {os.getenv('LLM_PROVIDER', 'NOT SET')}")
print(f"Embedding Dimension: {os.getenv('EMBEDDING_DIMENSION', 'NOT SET')}")
print(f"Neo4j URI: {os.getenv('NEO4J_URI', 'NOT SET')}")
print("=" * 60)

# Page configuration
st.set_page_config(
    page_title="Q&A RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .confidence-high {
        color: #4caf50;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ff9800;
        font-weight: bold;
    }
    .confidence-low {
        color: #f44336;
        font-weight: bold;
    }
    .source-box {
        background-color: #fafafa;
        padding: 0.5rem;
        border-radius: 0.3rem;
        border: 1px solid #ddd;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    /* Custom CSS for modern UI */
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* React-style Progress Bar */
    .react-progress-container {
        width: 100%;
        background: #f0f2f6;
        border-radius: 12px;
        padding: 4px;
        margin: 20px 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .react-progress-bar {
        height: 28px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%);
        background-size: 200% 100%;
        border-radius: 10px;
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        animation: shimmer 2s infinite;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .react-progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255,255,255,0.3) 50%, 
            transparent 100%);
        animation: slide 1.5s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes slide {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .react-progress-text {
        text-align: center;
        font-weight: 600;
        color: #333;
        margin-top: 8px;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
    }
    
    .react-progress-percentage {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'documents' not in st.session_state:
    st.session_state.documents = []

if 'processing' not in st.session_state:
    st.session_state.processing = False

# Header
st.markdown('<div class="main-header">📚 School Books Q&A System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Knowledge Graph + Vector Search powered Q&A</div>',
    unsafe_allow_html=True
)

# Team Information
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem; padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem;">
    <p style="margin: 0; font-size: 1rem; color: #1f77b4;"><strong>Team: GenAI4 Titans</strong></p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #666;">
        <strong>Contributors:</strong> McEnroe • Vijay • Hemanth • Kanda
    </p>
</div>
""", unsafe_allow_html=True)

# Visualization Section
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 View NLP Analysis", use_container_width=True):
        st.session_state.show_nlp = True

with col2:
    if st.button("🎯 View Vector Space", use_container_width=True):
        st.session_state.show_vectors = True

with col3:
    if st.button("🕸️ View Knowledge Graph", use_container_width=True):
        st.session_state.show_graph = True

# NLP Analysis Modal
if st.session_state.get('show_nlp', False):
    with st.expander("📊 NLP Analysis & Statistics", expanded=True):
        st.markdown("### Document NLP Analysis")
        
        if st.session_state.documents:
            try:
                from database.neon_vector_store import NeonVectorStore
                import pandas as pd
                
                with NeonVectorStore() as vs:
                    all_chunks = []
                    for doc in st.session_state.documents:
                        chunks = vs.get_document_chunks(doc['id'])
                        all_chunks.extend([c['content'] for c in chunks])
                    
                    if all_chunks:
                        # Word frequency analysis
                        from collections import Counter
                        import re
                        
                        words = []
                        for chunk in all_chunks:
                            words.extend(re.findall(r'\b\w+\b', chunk.lower()))
                        
                        word_freq = Counter(words).most_common(20)
                        
                        # Create bar chart
                        import plotly.graph_objects as go
                        
                        fig = go.Figure(data=[
                            go.Bar(
                                x=[w[0] for w in word_freq],
                                y=[w[1] for w in word_freq],
                                marker_color='lightblue'
                            )
                        ])
                        fig.update_layout(
                            title="Top 20 Most Frequent Words",
                            xaxis_title="Words",
                            yaxis_title="Frequency",
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Chunks", len(all_chunks))
                        with col2:
                            st.metric("Total Words", len(words))
                        with col3:
                            st.metric("Unique Words", len(set(words)))
                    else:
                        st.info("No chunks available for analysis")
            except Exception as e:
                st.error(f"Error loading NLP analysis: {str(e)}")
        else:
            st.info("Upload documents first to see NLP analysis")
        
        if st.button("Close", key="close_nlp"):
            st.session_state.show_nlp = False
            st.rerun()

# Vector Space Visualization Modal
if st.session_state.get('show_vectors', False):
    with st.expander("🎯 Vector Embedding Space", expanded=True):
        st.markdown("### Vector Space Visualization (t-SNE)")
        
        if st.session_state.documents:
            try:
                from database.neon_vector_store import NeonVectorStore
                import numpy as np
                import plotly.graph_objects as go
                
                with NeonVectorStore() as vs:
                    all_chunks = []
                    all_embeddings = []
                    
                    for doc in st.session_state.documents:
                        # Get chunks with embeddings
                        vs.cursor.execute(
                            """
                            SELECT content, embedding 
                            FROM document_chunks 
                            WHERE document_id = %s 
                            LIMIT 100
                            """,
                            (doc['id'],)
                        )
                        results = vs.cursor.fetchall()
                        
                        for content, embedding in results:
                            all_chunks.append(content[:50] + "...")
                            # Convert pgvector string to list of floats
                            if isinstance(embedding, str):
                                try:
                                    # Try parsing as JSON first
                                    import json
                                    embedding_list = json.loads(embedding)
                                except json.JSONDecodeError:
                                    # Fallback to string parsing for pgvector format '[1,2,3]'
                                    embedding_list = [float(x) for x in embedding.strip('[]').split(',')]
                                all_embeddings.append(embedding_list)
                            else:
                                # Already a list/array
                                all_embeddings.append(embedding)
                    
                    if all_embeddings and len(all_embeddings) > 2:
                        # Convert to numpy array
                        embeddings_array = np.array(all_embeddings)
                        
                        # Use t-SNE for dimensionality reduction
                        from sklearn.manifold import TSNE
                        
                        tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(all_embeddings)-1))
                        embeddings_2d = tsne.fit_transform(embeddings_array)
                        
                        # Create scatter plot
                        fig = go.Figure(data=[
                            go.Scatter(
                                x=embeddings_2d[:, 0],
                                y=embeddings_2d[:, 1],
                                mode='markers',
                                marker=dict(
                                    size=10,
                                    color=np.arange(len(embeddings_2d)),
                                    colorscale='Viridis',
                                    showscale=True
                                ),
                                text=all_chunks,
                                hovertemplate='<b>%{text}</b><extra></extra>'
                            )
                        ])
                        
                        fig.update_layout(
                            title="Document Chunks in 2D Vector Space",
                            xaxis_title="t-SNE Dimension 1",
                            yaxis_title="t-SNE Dimension 2",
                            height=500,
                            hovermode='closest'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        st.info(f"Visualizing {len(all_embeddings)} chunk embeddings reduced from {embeddings_array.shape[1]}D to 2D")
                    else:
                        st.info("Need at least 3 chunks to visualize vector space")
                        
            except Exception as e:
                st.error(f"Error loading vector visualization: {str(e)}")
        else:
            st.info("Upload documents first to see vector space")
        
        if st.button("Close", key="close_vectors"):
            st.session_state.show_vectors = False
            st.rerun()

# Knowledge Graph Visualization Modal
if st.session_state.get('show_graph', False):
    with st.expander("🕸️ Knowledge Graph Visualization", expanded=True):
        st.markdown("### Interactive Knowledge Graph")
        
        if st.session_state.documents:
            try:
                from database.neo4j_graph_store import Neo4jGraphStore
                import networkx as nx
                import plotly.graph_objects as go
                
                with Neo4jGraphStore() as gs:
                    # Get entities and relationships
                    result = gs.driver.execute_query(
                        """
                        MATCH (e:Entity)
                        OPTIONAL MATCH (e)-[r:RELATES_TO]->(e2:Entity)
                        RETURN e.name as source, e.type as source_type, 
                               e2.name as target, r.type as rel_type
                        LIMIT 100
                        """
                    )
                    
                    # Build NetworkX graph
                    G = nx.Graph()
                    
                    for record in result.records:
                        source = record.get("source")
                        target = record.get("target")
                        source_type = record.get("source_type", "Entity")
                        
                        if source:
                            G.add_node(source, type=source_type)
                        
                        if source and target:
                            rel_type = record.get("rel_type", "relates_to")
                            G.add_edge(source, target, type=rel_type)
                    
                    if len(G.nodes()) > 0:
                        # Create layout
                        pos = nx.spring_layout(G, k=0.5, iterations=50)
                        
                        # Create edges
                        edge_trace = []
                        for edge in G.edges():
                            x0, y0 = pos[edge[0]]
                            x1, y1 = pos[edge[1]]
                            edge_trace.append(
                                go.Scatter(
                                    x=[x0, x1, None],
                                    y=[y0, y1, None],
                                    mode='lines',
                                    line=dict(width=1, color='#888'),
                                    hoverinfo='none',
                                    showlegend=False
                                )
                            )
                        
                        # Create nodes
                        node_x = []
                        node_y = []
                        node_text = []
                        node_color = []
                        
                        color_map = {
                            'PERSON': '#FF6B6B',
                            'ORGANIZATION': '#4ECDC4',
                            'LOCATION': '#45B7D1',
                            'DATE': '#FFA07A',
                            'CONCEPT': '#98D8C8'
                        }
                        
                        for node in G.nodes():
                            x, y = pos[node]
                            node_x.append(x)
                            node_y.append(y)
                            node_text.append(node)
                            node_type = G.nodes[node].get('type', 'Entity')
                            node_color.append(color_map.get(node_type, '#999'))
                        
                        node_trace = go.Scatter(
                            x=node_x,
                            y=node_y,
                            mode='markers+text',
                            text=node_text,
                            textposition="top center",
                            marker=dict(
                                size=20,
                                color=node_color,
                                line=dict(width=2, color='white')
                            ),
                            hovertemplate='<b>%{text}</b><extra></extra>'
                        )
                        
                        # Create figure
                        fig = go.Figure(data=edge_trace + [node_trace])
                        
                        fig.update_layout(
                            title=f"Knowledge Graph ({len(G.nodes())} entities, {len(G.edges())} relationships)",
                            showlegend=False,
                            hovermode='closest',
                            height=600,
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Legend
                        st.markdown("**Entity Types:**")
                        cols = st.columns(5)
                        for idx, (etype, color) in enumerate(color_map.items()):
                            with cols[idx % 5]:
                                st.markdown(f'<span style="color: {color};">●</span> {etype}', unsafe_allow_html=True)
                    else:
                        st.info("No entities found in knowledge graph")
                        
            except Exception as e:
                st.error(f"Error loading graph visualization: {str(e)}")
        else:
            st.info("Upload documents first to see knowledge graph")
        
        if st.button("Close", key="close_graph"):
            st.session_state.show_graph = False
            st.rerun()

# Sidebar
with st.sidebar:
    st.header("📚 Document Management")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload PDF Document",
        type=['pdf'],
        help="Upload a PDF document to add to the knowledge base"
    )
    
    if uploaded_file and not st.session_state.processing:
        if st.button("Process Document", type="primary"):
            st.session_state.processing = True
            temp_path = None  # Initialize before try block
            
            # Create custom React-style progress bar
            progress_container = st.empty()
            status_text = st.empty()
            
            def update_progress(percentage, message):
                """Update the React-style progress bar"""
                progress_container.markdown(f"""
                <div class="react-progress-container">
                    <div class="react-progress-bar" style="width: {percentage}%;"></div>
                </div>
                <div class="react-progress-text">
                    {message} <span class="react-progress-percentage">{percentage}%</span>
                </div>
                """, unsafe_allow_html=True)
            
            try:
                # Import processing modules
                from processing.pdf_processor import PDFProcessor
                from processing.ocr_processor import OCRProcessor
                from processing.chunking import TextChunker
                from processing.embeddings import EmbeddingGenerator
                from database.neon_vector_store import NeonVectorStore
                from knowledge_graph.graph_builder import GraphBuilder
                
                # Save uploaded file temporarily
                temp_path = f"/tmp/{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                update_progress(5, "📁 Saving file...")
                
                # Process PDF
                update_progress(10, "📄 Extracting text and images...")
                with PDFProcessor(temp_path) as pdf_proc:
                    doc_data = pdf_proc.process_document()
                update_progress(20, "📄 Text extraction complete")
                
                # OCR for images with multithreading
                if doc_data['images']:
                    update_progress(20, f"🖼️ Running OCR on {len(doc_data['images'])} images...")
                    ocr_proc = OCRProcessor()
                    
                    # Process images in parallel with 8 workers for maximum speed
                    from concurrent.futures import ThreadPoolExecutor, as_completed
                    ocr_results = {}
                    
                    with ThreadPoolExecutor(max_workers=8) as executor:
                        future_to_img = {
                            executor.submit(ocr_proc.process_image, img_data['image']): img_data['page_number']
                            for img_data in doc_data['images']
                        }
                        
                        completed = 0
                        for future in as_completed(future_to_img):
                            page_num = future_to_img[future]
                            ocr_result = future.result()
                            if ocr_result['text']:
                                ocr_results[page_num] = ocr_result['text']
                            
                            completed += 1
                            ocr_progress = 20 + int((completed / len(doc_data['images'])) * 15)
                            update_progress(ocr_progress, f"🖼️ OCR Progress: {completed}/{len(doc_data['images'])} images")
                    
                    # Add OCR text to pages
                    for page_num, ocr_text in ocr_results.items():
                        for page in doc_data['pages']:
                            if page['page_number'] == page_num:
                                page['text'] += "\n\n[OCR Text]\n" + ocr_text
                    
                    update_progress(35, "🖼️ OCR complete")
                else:
                    update_progress(35, "📄 No images to process")
                
                # Chunk text
                update_progress(40, "✂️ Chunking document...")
                chunker = TextChunker()
                chunks = chunker.chunk_document_pages(doc_data['pages'])
                update_progress(45, "✂️ Chunking complete")
                
                # Generate embeddings
                update_progress(50, f"🧮 Generating embeddings for {len(chunks)} chunks...")
                embedding_gen = EmbeddingGenerator()
                texts = [chunk['content'] for chunk in chunks]
                embeddings = embedding_gen.generate_embeddings_batch(texts, show_progress=False)
                
                # Add embeddings to chunks
                for chunk, embedding in zip(chunks, embeddings):
                    chunk['embedding'] = embedding
                update_progress(65, "🧮 Embeddings generated")
                
                # Store in vector database
                update_progress(70, "💾 Storing in vector database...")
                with NeonVectorStore() as vector_store:
                    doc_id = vector_store.add_document(
                        filename=uploaded_file.name,
                        total_pages=doc_data['total_pages'],
                        file_size=doc_data['metadata']['file_size'],
                        metadata=doc_data['metadata']
                    )
                    vector_store.add_chunks(doc_id, chunks)
                update_progress(80, "💾 Vector storage complete")
                
                # Build knowledge graph
                update_progress(85, "🕸️ Building knowledge graph...")
                with GraphBuilder() as graph_builder:
                    graph_result = graph_builder.build_graph_for_document(
                        document_id=doc_id,
                        filename=uploaded_file.name,
                        chunks=chunks,
                        metadata=doc_data['metadata']
                    )
                update_progress(95, "🕸️ Knowledge graph complete")
                
                # Add to session state
                st.session_state.documents.append({
                    'id': doc_id,
                    'filename': uploaded_file.name,
                    'pages': doc_data['total_pages'],
                    'chunks': len(chunks),
                    'entities': len(graph_result['entities']),
                    'relationships': len(graph_result['relationships'])
                })
                
                # Complete
                update_progress(100, "✅ Processing complete!")
                
                # Display detailed statistics in a nice card
                st.success("✅ Document processed successfully!")
                
                # Create columns for statistics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        label="📄 Pages",
                        value=doc_data['total_pages'],
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        label="📦 Chunks",
                        value=len(chunks),
                        delta=f"{len(chunks)/doc_data['total_pages']:.1f} per page"
                    )
                
                with col3:
                    st.metric(
                        label="🏷️ Entities",
                        value=len(graph_result['entities']),
                        delta=f"{len(graph_result['entities'])/len(chunks):.1f} per chunk"
                    )
                
                with col4:
                    st.metric(
                        label="🔗 Relationships",
                        value=len(graph_result['relationships']),
                        delta=None
                    )
                
                # Additional details in expander
                with st.expander("📊 Detailed Processing Information"):
                    st.markdown("### Document Information")
                    st.write(f"**Filename:** {uploaded_file.name}")
                    st.write(f"**File Size:** {doc_data['metadata']['file_size'] / (1024*1024):.2f} MB")
                    st.write(f"**Total Pages:** {doc_data['total_pages']}")
                    
                    st.markdown("### Processing Statistics")
                    st.write(f"**Total Chunks:** {len(chunks)}")
                    st.write(f"**Average Chunk Size:** {sum(len(c['content']) for c in chunks) / len(chunks):.0f} characters")
                    st.write(f"**Embeddings Generated:** {len(embeddings)}")
                    st.write(f"**Embedding Dimension:** {len(embeddings[0]) if embeddings else 0}")
                    
                    st.markdown("### Knowledge Graph")
                    st.write(f"**Entities Extracted:** {len(graph_result['entities'])}")
                    st.write(f"**Relationships Found:** {len(graph_result['relationships'])}")
                    
                    # Entity type breakdown
                    if graph_result['entities']:
                        entity_types = {}
                        for entity in graph_result['entities']:
                            etype = entity.get('type', 'Unknown')
                            entity_types[etype] = entity_types.get(etype, 0) + 1
                        
                        st.markdown("**Entity Types:**")
                        for etype, count in sorted(entity_types.items(), key=lambda x: x[1], reverse=True):
                            st.write(f"  - {etype}: {count}")
                    
                    st.markdown("### Storage")
                    st.write(f"**Document ID:** {doc_id}")
                    st.write(f"**Vector Database:** Neon DB (pgvector)")
                    st.write(f"**Knowledge Graph:** Neo4j")
                
            except Exception as e:
                progress_container.empty()
                st.error(f"❌ Error processing document: {str(e)}")
                logger.error(f"Document processing error: {e}", exc_info=True)
            
            finally:
                st.session_state.processing = False
                # Clean up temp file
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
    
    # Display uploaded documents
    st.divider()
    st.subheader("📑 Uploaded Documents")
    
    if st.session_state.documents:
        for doc in st.session_state.documents:
            with st.expander(f"📄 {doc['filename']}"):
                st.write(f"**Pages:** {doc['pages']}")
                st.write(f"**Chunks:** {doc['chunks']}")
                st.write(f"**Entities:** {doc['entities']}")
                st.write(f"**Relationships:** {doc['relationships']}")
    else:
        st.info("No documents uploaded yet")
    
    # Settings
    st.divider()
    st.subheader("⚙️ Settings")
    
    # Environment status
    env_status = "✅" if env_path.exists() else "❌"
    st.write(f"{env_status} **Environment File:** {'.env loaded' if env_path.exists() else 'Not found'}")
    
    # Database Connections
    st.divider()
    st.subheader("🔌 Database Connections")
    
    # Test database connections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Neon DB (Vectors)**")
        if st.button("🔍 Test Connection", key="test_neon"):
            try:
                from database.neon_vector_store import NeonVectorStore
                with NeonVectorStore() as vs:
                    st.success("✅ Connected!")
            except Exception as e:
                st.error(f"❌ Failed: {str(e)[:50]}")
        
        # Extract host from URI for Neon console link
        neon_uri = os.getenv('NEON_DB_URI', '')
        if 'neon.tech' in neon_uri:
            st.markdown("🌐 [Open Neon Console](https://console.neon.tech)")
    
    with col2:
        st.markdown("**Neo4j (Graph)**")
        if st.button("🔍 Test Connection", key="test_neo4j"):
            try:
                # Use Neo4jGraphStore which includes retry logic for routing issues
                from database.neo4j_graph_store import Neo4jGraphStore
                with Neo4jGraphStore() as gs:
                    # Simple test query
                    result = gs.driver.session(database=settings.neo4j_database).run("RETURN 1 AS test")
                    result.single()
                st.success("✅ Connected!")
            except Exception as e:
                st.error(f"❌ Failed: {str(e)[:200]}")
            except Exception as e:
                st.error(f"❌ Failed: {str(e)[:50]}")
        
        # Extract host from URI for Neo4j browser link
        neo4j_uri = settings.neo4j_uri
        if 'neo4j.io' in neo4j_uri:
            # Extract instance ID from URI
            instance_id = neo4j_uri.split('//')[1].split('.')[0] if '//' in neo4j_uri else ''
            st.markdown(f"🌐 [Open Neo4j Browser](https://browser.neo4j.io/?connectURL={neo4j_uri})")
        else:
            # Local Neo4j
            st.markdown("🌐 [Open Neo4j Browser](http://localhost:7474)")
    
    # Database Statistics
    with st.expander("📊 Database Statistics"):
        try:
            from database.neon_vector_store import NeonVectorStore
            from database.neo4j_graph_store import Neo4jGraphStore
            
            # Neon DB stats
            try:
                with NeonVectorStore() as vs:
                    docs = vs.get_all_documents()
                    st.write(f"**Vector Store:** {len(docs)} documents")
            except Exception as e:
                st.write(f"**Vector Store:** Error - {str(e)[:50]}")
            
            # Neo4j stats
            try:
                with Neo4jGraphStore() as gs:
                    # Get node and relationship counts
                    result = gs.driver.execute_query(
                        "MATCH (n) RETURN count(n) as node_count"
                    )
                    node_count = result.records[0]["node_count"] if result.records else 0
                    
                    result = gs.driver.execute_query(
                        "MATCH ()-[r]->() RETURN count(r) as rel_count"
                    )
                    rel_count = result.records[0]["rel_count"] if result.records else 0
                    
                    st.write(f"**Knowledge Graph:** {node_count} nodes, {rel_count} relationships")
            except Exception as e:
                st.write(f"**Knowledge Graph:** ⚠️ Not connected")
                st.caption(f"Error: {str(e)[:50]}")
                st.info("💡 Check NEO4J_TROUBLESHOOTING.md for help")
        except Exception as e:
            st.write(f"Error loading stats: {str(e)[:50]}")
    
    # Configuration details
    with st.expander("📋 Configuration Details"):
        st.write(f"**Environment:** {settings.environment}")
        st.write(f"**LLM Provider:** {settings.llm_provider}")
        st.write(f"**Model:** {settings.get_llm_model()}")
        st.write(f"**Embedding Model:** {settings.get_embedding_model()}")
        st.write(f"**Embedding Dimension:** {settings.embedding_dimension}")
        st.write(f"**Vector Index:** {settings.vector_index_type}")
        st.write(f"**Chunk Size:** {settings.chunk_size}")
        st.write(f"**Top-K Retrieval:** {settings.top_k_retrieval}")
        st.write(f"**Graph Retrieval:** {'Enabled' if settings.enable_graph_retrieval else 'Disabled'}")

# Main chat interface
st.header("💬 Ask Questions")

# Display chat messages
for message in st.session_state.messages:
    role = message['role']
    content = message['content']
    
    if role == 'user':
        st.markdown(
            f'<div class="chat-message user-message"><strong>You:</strong><br>{content}</div>',
            unsafe_allow_html=True
        )
    else:
        answer = content.get('answer', '')
        confidence = content.get('confidence', 'Medium')
        sources = content.get('sources', [])
        
        # Determine confidence class
        conf_class = 'confidence-medium'
        if confidence == 'High':
            conf_class = 'confidence-high'
        elif confidence == 'Low':
            conf_class = 'confidence-low'
        
        st.markdown(
            f'<div class="chat-message assistant-message">'
            f'<strong>Assistant:</strong><br>{answer}<br><br>'
            f'<span class="{conf_class}">Confidence: {confidence}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Display sources
        if sources:
            with st.expander("📚 View Sources"):
                for source in sources:
                    st.markdown(
                        f"**{source['source_number']}.** {source['filename']} - "
                        f"Page {source.get('page_number', 'N/A')} "
                        f"(Score: {source.get('score', 0):.2f})"
                    )

# Chat input
if not st.session_state.documents:
    st.info("👆 Please upload a document first to start asking questions")
else:
    query = st.chat_input("Ask a question about your documents...")
    
    if query:
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': query
        })
        
        # Generate answer
        with st.spinner("🤔 Thinking..."):
            try:
                from rag.retriever import HybridRetriever
                from rag.context_builder import ContextBuilder
                from rag.generator import AnswerGenerator
                from utils.validators import validate_query
                
                # Validate query
                is_valid, error_msg = validate_query(query)
                if not is_valid:
                    st.error(f"Invalid query: {error_msg}")
                else:
                    # Retrieve relevant chunks
                    with HybridRetriever() as retriever:
                        retrieved_chunks = retriever.retrieve(query)
                    
                    # Build context
                    context_builder = ContextBuilder()
                    context_data = context_builder.build_context(retrieved_chunks)
                    
                    # Generate answer
                    generator = AnswerGenerator()
                    result = generator.generate_answer(
                        query=query,
                        context=context_data['context'],
                        sources=context_data['sources']
                    )
                    
                    # Add assistant message
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': result
                    })
                    
                    # Rerun to display new messages
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error generating answer: {str(e)}")
                logger.error(f"Answer generation error: {e}", exc_info=True)

# Footer
st.divider()
st.caption(
    "Powered by Neon DB (Vector Store) + Neo4j (Knowledge Graph) | "
    f"Environment: {settings.environment}"
)
