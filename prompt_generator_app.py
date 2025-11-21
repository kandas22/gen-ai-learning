import streamlit as st
from typing import Optional, Dict, List

# Page configuration
st.set_page_config(
    page_title="AI Prompt Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .prompt-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .generated-prompt {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        margin-top: 1rem;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    h1 {
        color: #667eea;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    </style>
""", unsafe_allow_html=True)

# RAG type configurations
RAG_TYPES = {
    "Vector Database": {
        "options": ["Pinecone", "Weaviate", "Chroma", "FAISS", "Milvus"],
        "description": "Store and retrieve embeddings from vector databases"
    },
    "Document Retrieval": {
        "options": ["PDF", "Word", "Text Files", "Web Pages", "Markdown"],
        "description": "Extract and retrieve information from documents"
    },
    "Knowledge Graph": {
        "options": ["Neo4j", "Amazon Neptune", "GraphDB", "Custom Graph"],
        "description": "Query structured knowledge graphs"
    },
    "Hybrid Search": {
        "options": ["Vector + Keyword", "Semantic + BM25", "Multi-modal"],
        "description": "Combine multiple retrieval strategies"
    }
}

def generate_prompt(
    task_description: str,
    context: str,
    output_format: str,
    tone: str,
    use_rag: bool,
    rag_type: Optional[str] = None,
    rag_options: Optional[List[str]] = None,
    additional_instructions: str = ""
) -> str:
    """Generate a comprehensive prompt based on user inputs."""
    
    prompt_parts = []
    
    # Add role and task
    prompt_parts.append(f"You are an AI assistant specialized in {task_description}.")
    
    # Add context
    if context:
        prompt_parts.append(f"\nContext: {context}")
    
    # Add RAG instructions if enabled
    if use_rag and rag_type:
        rag_instruction = f"\nRetrieval Method: Use {rag_type}"
        if rag_options:
            rag_instruction += f" with the following sources: {', '.join(rag_options)}"
        rag_instruction += "\nRetrieve relevant information before generating your response."
        prompt_parts.append(rag_instruction)
    
    # Add tone
    prompt_parts.append(f"\nTone: {tone}")
    
    # Add output format
    prompt_parts.append(f"\nOutput Format: {output_format}")
    
    # Add additional instructions
    if additional_instructions:
        prompt_parts.append(f"\nAdditional Instructions:\n{additional_instructions}")
    
    # Add final instruction
    prompt_parts.append("\nPlease provide a comprehensive and well-structured response.")
    
    return "\n".join(prompt_parts)


def main():
    # Header
    st.title("🤖 AI Prompt Generator")
    st.markdown("### Create powerful prompts for your AI applications")
    
    # Sidebar for API Key and Settings
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="Enter your API key",
            help="Your API key will be kept secure and not displayed"
        )
        
        if api_key:
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your API key")
        
        st.markdown("---")
        
        # About section
        st.header("ℹ️ About")
        st.markdown("""
        This tool helps you generate structured prompts for AI models.
        
        **Features:**
        - Custom task descriptions
        - RAG integration options
        - Multiple output formats
        - Tone customization
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Prompt Configuration")
        
        # Task description
        task_description = st.text_input(
            "Task Description",
            placeholder="e.g., answering questions about medical research",
            help="Describe what you want the AI to do"
        )
        
        # Context
        context = st.text_area(
            "Context",
            placeholder="Provide any background information or context...",
            height=100,
            help="Additional context to help the AI understand the task"
        )
        
        # Tone selection
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual", "Technical", "Creative", "Academic", "Friendly"],
            help="Select the desired tone for the output"
        )
        
        # Output format
        output_format = st.selectbox(
            "Output Format",
            ["Paragraph", "Bullet Points", "Numbered List", "JSON", "Markdown", "Code"],
            help="Choose how you want the output structured"
        )
    
    with col2:
        st.markdown("### 🔍 RAG Configuration (Optional)")
        
        # RAG selection
        use_rag = st.checkbox(
            "Enable RAG (Retrieval-Augmented Generation)",
            help="Enable to add retrieval capabilities to your prompt"
        )
        
        rag_type = None
        selected_rag_options = None
        
        if use_rag:
            # RAG type selection
            rag_type = st.selectbox(
                "RAG Type",
                list(RAG_TYPES.keys()),
                help="Select the type of retrieval method"
            )
            
            if rag_type:
                # Show description
                st.info(RAG_TYPES[rag_type]["description"])
                
                # RAG options
                selected_rag_options = st.multiselect(
                    f"{rag_type} Options",
                    RAG_TYPES[rag_type]["options"],
                    help=f"Select one or more {rag_type.lower()} options"
                )
        
        # Additional instructions
        st.markdown("### ➕ Additional Instructions")
        additional_instructions = st.text_area(
            "Custom Instructions",
            placeholder="Add any specific requirements or constraints...",
            height=100,
            help="Any additional instructions for the AI"
        )
    
    # Generate button
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        generate_button = st.button("✨ Generate Prompt", use_container_width=True)
    
    # Generate and display prompt
    if generate_button:
        if not task_description:
            st.error("❌ Please provide a task description")
        elif not api_key:
            st.error("❌ Please enter your API key in the sidebar")
        else:
            with st.spinner("Generating your prompt..."):
                generated_prompt = generate_prompt(
                    task_description=task_description,
                    context=context,
                    output_format=output_format,
                    tone=tone,
                    use_rag=use_rag,
                    rag_type=rag_type,
                    rag_options=selected_rag_options,
                    additional_instructions=additional_instructions
                )
                
                st.markdown("### 🎯 Generated Prompt")
                st.markdown(f'<div class="generated-prompt">{generated_prompt}</div>', unsafe_allow_html=True)
                
                # Copy to clipboard button
                st.code(generated_prompt, language="text")
                
                # Download button
                st.download_button(
                    label="📥 Download Prompt",
                    data=generated_prompt,
                    file_name="generated_prompt.txt",
                    mime="text/plain"
                )
                
                # Show configuration summary
                with st.expander("📊 Configuration Summary"):
                    st.json({
                        "task_description": task_description,
                        "tone": tone,
                        "output_format": output_format,
                        "rag_enabled": use_rag,
                        "rag_type": rag_type if use_rag else "N/A",
                        "rag_options": selected_rag_options if use_rag else "N/A",
                        "api_key_configured": bool(api_key)
                    })


if __name__ == "__main__":
    main()
