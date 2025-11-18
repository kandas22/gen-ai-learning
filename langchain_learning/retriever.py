from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load the FAISS index with embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("langchain_learning/assets/faiss_index", embeddings, allow_dangerous_deserialization=True)

# Create retriever from the loaded vectorstore
retriever = vectorstore.as_retriever()

# Get relevant documents
answer = retriever.invoke("python?")
print(answer)
