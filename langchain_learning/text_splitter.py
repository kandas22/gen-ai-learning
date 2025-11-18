from statistics import fmean
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter,CharacterTextSplitter

text_splitter = PyPDFLoader("langchain_learning/assets/LLM.pdf").load()

full_text = ""
for doc in text_splitter:
    full_text += doc.page_content


chat_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
texts = chat_splitter.split_text(full_text)
print(texts) 

print("---- Recrusive Splitter ----")
recrusive_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
texts = recrusive_splitter.split_text(full_text)
print(texts) 