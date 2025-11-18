from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

# Using OpenAIEmbeddings Embeddings
openai_embed = OpenAIEmbeddings()
openai_text = "LangChain is an amazing framework for building applications with LLMs."
embedding = openai_embed.embed_query(openai_text)
print("Embedding vector:", embedding[:5])

#Using HuggingFaceEmbeddings Embeddings
hf_embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
hf_text = "LangChain is an amazing framework for building applications with LLMs."
hf_embedding = hf_embed.embed_query(hf_text)
print("HuggingFace Embedding vector:", hf_embedding[:5])

