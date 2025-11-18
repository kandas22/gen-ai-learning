from statistics import fmean
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = PyPDFLoader("LLM.pdf").load()

full_text = ""
for doc in text_splitter:
    full_text += doc.page_content


text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
texts = text_splitter.split_text(full_text)
print(texts)