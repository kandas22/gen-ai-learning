"""
Chroma Vector Store Example - Complete Workflow
Step-by-step implementation of text insertion, embedding, vector storage, and retrieval
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os

# ============================================
# STEP 1: Prepare Sample Data
# ============================================
print("=" * 60)
print("STEP 1: Preparing Sample Data")
print("=" * 60)

# Sample texts about AI and programming
sample_texts = [
    "Python is a high-level programming language widely used for AI and machine learning.",
    "LangChain is a framework for developing applications powered by language models.",
    "Vector databases store embeddings for efficient similarity search.",
    "Chroma is an open-source embedding database designed for AI applications.",
    "Machine learning models learn patterns from training data.",
    "Natural Language Processing enables computers to understand human language.",
    "Embeddings convert text into numerical vectors that capture semantic meaning.",
    "Retrieval Augmented Generation combines search with language model generation."
]

print(f"✓ Prepared {len(sample_texts)} sample texts\n")

# ============================================
# STEP 2: Create Embeddings Model
# ============================================
print("=" * 60)
print("STEP 2: Creating Embeddings Model")
print("=" * 60)

# Initialize HuggingFace embeddings (free, no API key needed)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("✓ Embeddings model loaded: sentence-transformers/all-MiniLM-L6-v2")
print("✓ This model creates 384-dimensional vectors\n")

# ============================================
# STEP 3: Create Chroma Vector Store
# ============================================
print("=" * 60)
print("STEP 3: Creating Chroma Vector Store")
print("=" * 60)

# Define persist directory
persist_directory = "langchain_learning/assets/chroma_db"

# Create Chroma vector store from texts
vectorstore = Chroma.from_texts(
    texts=sample_texts,
    embedding=embeddings,
    persist_directory=persist_directory
)

print(f"✓ Chroma vector store created")
print(f"✓ Stored {len(sample_texts)} documents")
print(f"✓ Persist directory: {persist_directory}\n")

# ============================================
# STEP 4: Test Similarity Search
# ============================================
print("=" * 60)
print("STEP 4: Testing Similarity Search")
print("=" * 60)

query1 = "What is Python used for?"
print(f"\nQuery: '{query1}'")
print("-" * 60)

results1 = vectorstore.similarity_search(query1, k=2)
for i, doc in enumerate(results1, 1):
    print(f"\nResult {i}:")
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}")

# ============================================
# STEP 5: Similarity Search with Scores
# ============================================
print("\n" + "=" * 60)
print("STEP 5: Similarity Search with Relevance Scores")
print("=" * 60)

query2 = "Tell me about embeddings"
print(f"\nQuery: '{query2}'")
print("-" * 60)

results_with_scores = vectorstore.similarity_search_with_score(query2, k=3)
for i, (doc, score) in enumerate(results_with_scores, 1):
    print(f"\nResult {i} (Score: {score:.4f}):")
    print(f"Content: {doc.page_content}")

# ============================================
# STEP 6: Create and Use Retriever
# ============================================
print("\n" + "=" * 60)
print("STEP 6: Using Retriever Interface")
print("=" * 60)

# Create retriever with custom search parameters
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

query3 = "What is Chroma?"
print(f"\nQuery: '{query3}'")
print("-" * 60)

retrieved_docs = retriever.invoke(query3)
for i, doc in enumerate(retrieved_docs, 1):
    print(f"\nRetrieved Document {i}:")
    print(f"{doc.page_content}")

# ============================================
# STEP 7: Load Existing Chroma DB
# ============================================
print("\n" + "=" * 60)
print("STEP 7: Loading Existing Chroma Database")
print("=" * 60)

# Simulate loading from disk (useful for persistence)
loaded_vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings
)

print("✓ Successfully loaded existing Chroma database")

# Test loaded vectorstore
query4 = "machine learning"
print(f"\nTesting loaded vectorstore with query: '{query4}'")
print("-" * 60)

loaded_results = loaded_vectorstore.similarity_search(query4, k=2)
for i, doc in enumerate(loaded_results, 1):
    print(f"\nResult {i}: {doc.page_content}")

# ============================================
# STEP 8: Advanced Retrieval Options
# ============================================
print("\n" + "=" * 60)
print("STEP 8: Advanced Retrieval Options")
print("=" * 60)

# MMR (Maximal Marginal Relevance) - diverse results
print("\n--- Using MMR (Maximal Marginal Relevance) ---")
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 5}
)

query5 = "programming and AI"
print(f"Query: '{query5}'")
mmr_results = mmr_retriever.invoke(query5)
for i, doc in enumerate(mmr_results, 1):
    print(f"\n{i}. {doc.page_content}")

# ============================================
# STEP 9: Add More Documents
# ============================================
print("\n" + "=" * 60)
print("STEP 9: Adding More Documents")
print("=" * 60)

new_texts = [
    "Deep learning is a subset of machine learning using neural networks.",
    "Transformers revolutionized natural language processing tasks."
]

# Add new documents to existing vectorstore
vectorstore.add_texts(new_texts)
print(f"✓ Added {len(new_texts)} new documents")
print(f"✓ Total documents in store: {len(sample_texts) + len(new_texts)}")

# ============================================
# STEP 10: Delete Documents (Optional)
# ============================================
print("\n" + "=" * 60)
print("STEP 10: Document Management")
print("=" * 60)

# Get collection info
collection = vectorstore._collection
print(f"✓ Collection name: {collection.name}")
print(f"✓ Total documents: {collection.count()}")

# ============================================
# STEP 11: Interactive Agent Mode
# ============================================
print("\n" + "=" * 60)
print("STEP 11: Interactive Agent Mode")
print("=" * 60)

def get_user_query():
    """
    Get query input from user with validation
    Returns: query string or None if user wants to exit
    """
    while True:
        print("\n" + "-" * 60)
        user_input = input("🤖 Enter your query (or 'quit' to exit): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Exiting interactive agent mode...")
            return None
        
        if not user_input:
            print("❌ Error: Query cannot be empty! Please enter a valid query.")
            continue
        
        return user_input

# Interactive agent loop
print("\n🤖 Welcome to Interactive Agent Mode!")
print("💬 Ask questions about AI, Python, LangChain, and more!")
print("📝 Type 'quit', 'exit', or 'q' to stop.")

while True:
    user_query = get_user_query()
    
    if user_query is None:
        break
    
    print(f"\n🔎 Searching for: '{user_query}'")
    print("-" * 60)
    
    try:
        # Perform similarity search with scores
        search_results = vectorstore.similarity_search_with_score(user_query, k=3)
        
        if not search_results:
            print("❌ No results found. Try a different query.")
        else:
            print(f"✅ Found {len(search_results)} relevant results:\n")
            
            for i, (doc, score) in enumerate(search_results, 1):
                print(f"📄 Result {i} (Relevance Score: {score:.4f}):")
                print(f"   {doc.page_content}")
                print()
    
    except Exception as e:
        print(f"❌ Error during search: {str(e)}")
        print("Please try again with a different query.")

# ============================================
# Summary
# ============================================
print("\n" + "=" * 60)
print("SUMMARY: Chroma Vector Store Workflow Complete!")
print("=" * 60)
print("""
✓ Step 1: Prepared sample data
✓ Step 2: Created embeddings model (HuggingFace)
✓ Step 3: Created Chroma vector store with persistence
✓ Step 4: Performed similarity search
✓ Step 5: Retrieved documents with relevance scores
✓ Step 6: Used retriever interface
✓ Step 7: Loaded existing database from disk
✓ Step 8: Explored advanced retrieval (MMR)
✓ Step 9: Added new documents dynamically
✓ Step 10: Checked collection statistics
✓ Step 11: Interactive agent mode with user queries

Next Steps:
- Integrate with LLMs for RAG (Retrieval Augmented Generation)
- Experiment with different embedding models
- Try different retrieval strategies
- Scale to larger datasets
""")

print("\n" + "=" * 60)
print("Chroma DB Location:", persist_directory)
print("=" * 60)