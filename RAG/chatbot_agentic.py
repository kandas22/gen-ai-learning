import streamlit as st
import os
# Fix for HuggingFace tokenizers warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from dotenv import load_dotenv
import tempfile
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import requests
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Kanda Hybrid RAG Framework Featuring Web Search Failover",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        display: flex;
        flex-direction: column;
        width: 100%;
        box-sizing: border-box;
    }
    
    .user-message {
        border-left: 5px solid #667eea;
        background-color: rgba(102, 126, 234, 0.05);
        color: inherit;
        margin-left: auto;
        margin-right: 0;
        max-width: 80%;
        padding-left: 1rem;
    }
    
    .bot-message {
        border-left: 5px solid #11998e;
        background-color: rgba(17, 153, 142, 0.05);
        color: inherit;
        margin-left: 0;
        margin-right: auto;
        max-width: 80%;
        padding-left: 1rem;
    }
    
    .web-search-message {
        border-left: 5px solid #4facfe;
        background-color: rgba(79, 172, 254, 0.05);
        color: inherit;
        margin-left: 0;
        margin-right: auto;
        max-width: 80%;
        padding-left: 1rem;
    }
    
    .message-header {
        opacity: 0.6;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-align: left;
    }
    
    .stats-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .stExpander {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    /* File uploader button styling */
    .stFileUploader>div>button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        font-weight: bold !important;
    }
    
    .stFileUploader>div>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4) !important;
    }
    
    /* Spinner color customization */
    .stSpinner > div {
        border-top-color: #4facfe !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False
if 'pdf_name' not in st.session_state:
    st.session_state.pdf_name = None
if 'chunk_count' not in st.session_state:
    st.session_state.chunk_count = 0
if 'search_count' not in st.session_state:
    st.session_state.search_count = {'pdf': 0, 'web': 0}

def process_pdf(uploaded_file):
    """Process uploaded PDF and create vector store"""
    try:
        with st.spinner("📄 Processing PDF..."):
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Load PDF
            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()
            
            st.info(f"✅ Loaded {len(documents)} pages from PDF")
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            chunks = text_splitter.split_documents(documents)
            
            st.info(f"✅ Split into {len(chunks)} text chunks")
            
            # Create embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            # Create vector store
            vectorstore = FAISS.from_documents(chunks, embeddings)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            st.session_state.vectorstore = vectorstore
            st.session_state.chunk_count = len(chunks)
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.pdf_processed = True
            
            st.success("🎉 PDF processed successfully! You can now ask questions.")
            
    except Exception as e:
        st.error(f"❌ Error processing PDF: {str(e)}")
        return None

def search_pdf(question):
    """Search PDF using RAG"""
    try:
        if st.session_state.vectorstore is None:
            return None, []
        
        # Initialize LLM
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Get relevant documents
        retriever = st.session_state.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )
        
        docs = retriever.invoke(question)
        
        if not docs:
            return None, []
        
        # Convert chat history
        chat_history = []
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                chat_history.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                chat_history.append(AIMessage(content=msg['content']))
        
        # Create context from documents
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Create prompt
        prompt = f"""Based on the following context from the PDF document, answer the question.
If the context doesn't contain relevant information to answer the question, respond with "NOT_FOUND".

Context:
{context}

Question: {question}

Answer:"""
        
        response = llm.invoke([HumanMessage(content=prompt)])
        answer = response.content
        
        # Check if answer is meaningful
        if "NOT_FOUND" in answer or len(answer.strip()) < 20:
            return None, []
        
        st.session_state.search_count['pdf'] += 1
        return answer, docs
        
    except Exception as e:
        st.warning(f"⚠️ PDF search failed: {str(e)}")
        return None, []

def search_web(question):
    """Search web using SearchAPI.io"""
    try:
        searchapi_key = os.getenv("SERPAPI_API_KEY")
        if not searchapi_key or searchapi_key == "your-serpapi-key-here":
            st.error("❌ SearchAPI key not configured in .env file")
            st.info("🔑 Get your API key from: https://www.searchapi.io/")
            return None
        
        with st.spinner("🌐 Searching the web..."):
            # Use SearchAPI.io
            params = {
                "engine": "google",
                "q": question,
                "api_key": searchapi_key
            }
            
            response = requests.get("https://www.searchapi.io/api/v1/search", params=params)
            
            if response.status_code != 200:
                st.error(f"❌ SearchAPI request failed with status {response.status_code}")
                return None
            
            data = response.json()
            
            # Extract organic results
            search_results = ""
            if "organic_results" in data and len(data["organic_results"]) > 0:
                for i, result in enumerate(data["organic_results"][:5], 1):
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    search_results += f"{i}. {title}\n{snippet}\n\n"
            elif "answer_box" in data:
                search_results = data["answer_box"].get("answer", "")
            
            # Check if we got meaningful results
            if not search_results or len(search_results.strip()) < 20:
                st.warning("⚠️ No relevant web results found for your question.")
                return "I couldn't find relevant information on the web for your question. Please try rephrasing or asking something else."
            
            # Initialize LLM
            llm = ChatOpenAI(
                model_name="gpt-4o-mini",
                temperature=0.7,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Create prompt with web search results
            prompt = f"""Based on the following web search results, provide a comprehensive answer to the question.
If the search results don't contain relevant information to answer the question, respond with "NOT_FOUND_WEB".
Be informative and cite that the information comes from web search.

Web Search Results:
{search_results}

Question: {question}

Answer:"""
            
            response = llm.invoke([HumanMessage(content=prompt)])
            answer = response.content
            
            # Check if answer is meaningful
            if "NOT_FOUND_WEB" in answer or len(answer.strip()) < 30:
                st.warning("⚠️ Could not generate a relevant answer from web search results.")
                return "I found some web results but couldn't generate a relevant answer. Please try rephrasing your question."
            
            st.session_state.search_count['web'] += 1
            return answer
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ SearchAPI request failed: {str(e)}")
        st.info("🔑 Get your API key from: https://www.searchapi.io/")
        return None
    except Exception as e:
        st.error(f"❌ Web search failed: {str(e)}")
        return None

def get_response(question):
    """Get response with fallback to web search"""
    try:
        # First try PDF search
        if st.session_state.pdf_processed:
            pdf_answer, sources = search_pdf(question)
            
            if pdf_answer:
                return {
                    "answer": pdf_answer,
                    "source": "pdf",
                    "sources": sources
                }
        
        # Fallback to web search
        web_answer = search_web(question)
        
        if web_answer:
            return {
                "answer": web_answer,
                "source": "web",
                "sources": []
            }
        
        return {
            "answer": "I couldn't find relevant information in the PDF or on the web. Please try rephrasing your question.",
            "source": "none",
            "sources": []
        }
        
    except Exception as e:
        st.error(f"❌ Error getting response: {str(e)}")
        return None

def display_chat_message(role, content, source=None, sources=None):
    """Display a chat message with styling"""
    if role == "user":
        # Escape HTML in content and convert newlines to <br>
        safe_content = content.replace('\n', '<br>')
        st.markdown(f'''
        <div class="chat-message user-message">
            <div class="message-header">👤 <strong>You:</strong></div>
            <div style="margin-top: 0.5rem;">{safe_content}</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        # Determine message class based on source
        message_class = "web-search-message" if source == "web" else "bot-message"
        source_icon = "🌐" if source == "web" else "📄"
        source_text = "Web Search" if source == "web" else "PDF Document"
        label_name = "Assistant" if source != "web" else "Web Search"
        
        # Check if content contains code blocks
        if "```" in content:
            # Process code blocks
            content_html = ""
            parts = content.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    # Regular text - convert markdown to HTML
                    if part.strip():
                        # Simple markdown conversion
                        part = part.replace('\n', '<br>')
                        # Bold
                        import re
                        part = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', part)
                        # Bullets
                        part = re.sub(r'<br>[-*]\s+', '<br>• ', part)
                        content_html += f'<div style="margin-bottom: 0.5rem;">{part}</div>'
                else:
                    # Code block
                    lines = part.split('\n', 1)
                    if len(lines) > 1:
                        lang = lines[0].strip()
                        code = lines[1]
                        # Escape HTML in code
                        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        content_html += f'<pre style="background-color: #f5f5f5; padding: 1rem; border-radius: 0.5rem; overflow-x: auto;"><code>{code}</code></pre>'
                    else:
                        code = part.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        content_html += f'<pre style="background-color: #f5f5f5; padding: 1rem; border-radius: 0.5rem; overflow-x: auto;"><code>{code}</code></pre>'
        else:
            # Convert markdown formatting to HTML
            import re
            content_html = content.replace('\n\n', '</p><p>').replace('\n', '<br>')
            # Bold
            content_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content_html)
            # Bullets
            content_html = re.sub(r'<br>[-*]\s+', '<br>• ', content_html)
            # Wrap in paragraph
            if not content_html.startswith('<p>'):
                content_html = f'<p>{content_html}</p>'
        
        # Display complete message in one div
        st.markdown(f'''
        <div class="chat-message {message_class}">
            <div class="message-header">{source_icon} <strong>{label_name}:</strong></div>
            <div style="margin-top: 0.5rem;">{content_html}</div>
            <div style="opacity: 0.7; font-size: 0.85rem; margin-top: 0.75rem;">{source_icon} Source: {source_text}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Display PDF sources if available
        if sources and len(sources) > 0:
            st.markdown("**📚 PDF Sources:**")
            for i, source_doc in enumerate(sources, 1):
                page = source_doc.metadata.get('page', 'Unknown')
                snippet = source_doc.page_content[:250] + "..." if len(source_doc.page_content) > 250 else source_doc.page_content
                
                with st.expander(f"📄 Source {i} (Page {page + 1})"):
                    st.write(snippet)
                    st.caption(f"Page {page + 1} of {st.session_state.pdf_name}")

# Main UI
st.markdown('<h1 class="main-header">🔍 Kanda Hybrid RAG Framework Featuring Web Search Failover</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ask questions from your PDF or search the web automatically!</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📁 Upload PDF (Optional)")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF document to search first, then fall back to web"
    )
    
    if uploaded_file is not None:
        if st.button("🚀 Process PDF"):
            process_pdf(uploaded_file)
    
    st.markdown("---")
    
    # Display statistics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📄 PDF Searches", st.session_state.search_count['pdf'])
    with col2:
        st.metric("🌐 Web Searches", st.session_state.search_count['web'])
    
    if st.session_state.pdf_processed:
        st.markdown(f"""
        <div class="stats-box">
            <h3>📊 PDF Stats</h3>
            <p><strong>File:</strong> {st.session_state.pdf_name}</p>
            <p><strong>Chunks:</strong> {st.session_state.chunk_count}</p>
            <p><strong>Status:</strong> ✅ Ready</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("❌ Remove PDF"):
            st.session_state.vectorstore = None
            st.session_state.pdf_processed = False
            st.session_state.pdf_name = None
            st.session_state.chunk_count = 0
            st.rerun()
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.search_count = {'pdf': 0, 'web': 0}
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div class="info-box">
        <h3>🎯 How It Works</h3>
        <ol>
            <li><strong>PDF First:</strong> Searches your uploaded PDF document</li>
            <li><strong>Web Fallback:</strong> If no answer found, searches the web</li>
            <li><strong>Smart Routing:</strong> Automatically picks the best source</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Tips
    - Upload PDF for document-specific questions
    - Web search works without PDF
    - Color-coded responses show source
    - Chat history maintained
    
    ### ⚙️ Configuration
    - Model: GPT-4o-mini
    - Embeddings: HuggingFace
    - Vector Store: FAISS
    - Web Search: SearchAPI.io
    """)

# Main chat interface
st.subheader("💬 Ask Anything!")

# Display chat history
for message in st.session_state.chat_history:
    display_chat_message(
        message['role'],
        message['content'],
        message.get('source'),
        message.get('sources')
    )

# Chat input
with st.form(key='chat_form', clear_on_submit=True):
    user_question = st.text_input(
        "Your question:",
        placeholder="e.g., What is machine learning? or Ask about your PDF...",
        key='user_input'
    )
    submit_button = st.form_submit_button("Send 🚀")

if submit_button and user_question.strip():
    # Add user message to history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_question
    })
    
    # Get response
    response = get_response(user_question)
    
    if response:
        # Add bot response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response['answer'],
            'source': response['source'],
            'sources': response.get('sources', [])
        })
    
    st.rerun()

# Welcome screen (when no messages)
if len(st.session_state.chat_history) == 0:
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📄 Step 1: Upload (Optional)
        Upload a PDF document for document-specific questions.
        Can also work without PDF!
        """)
    
    with col2:
        st.markdown("""
        ### 💬 Step 2: Ask
        Type your question in the input box.
        Works with or without PDF!
        """)
    
    with col3:
        st.markdown("""
        ### 🎯 Step 3: Get Answer
        Automatically searches PDF first, then web.
        Color-coded by source!
        """)
    
    st.markdown("---")
    
    # Example questions
    st.subheader("💡 Example Questions:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📄 PDF Questions:**")
        st.markdown("""
        - What is the main topic of this document?
        - Summarize the key findings
        - What methodology was used?
        """)
    
    with col2:
        st.markdown("**🌐 Web Questions:**")
        st.markdown("""
        - What is artificial intelligence?
        - Latest news about technology
        - How does blockchain work?
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Built with ❤️ using Streamlit, LangChain, OpenAI & SearchAPI.io</p>
    <p>🔒 Smart fallback system: PDF → Web Search</p>
</div>
""", unsafe_allow_html=True)
