from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
text_store = ["Python programming is best language for AI.",
"The LangChain library simplifies working with language models.",
"Embeddings convert text into numerical vectors for machine learning."]

FAISS.from_texts(texts=text_store, embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")).save_local("langchain_learning/assets/faiss_index")

