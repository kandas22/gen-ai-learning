from langchain_community.document_loaders import TextLoader,PyPDFLoader, WebBaseLoader, ArxivLoader,WikipediaLoader
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
text_data = TextLoader("langchain_learning/assets/notes.txt").load()
wikipedia_loader = WikipediaLoader(query="Natural Language Processing", load_max_docs=1).load

for doc in text_data:
    print("---- DOCUMENT ----")
    print("Content:")
    print(doc.page_content)
    print("Metadata:")
    print(doc.metadata)


pdf_data = PyPDFLoader("langchain_learning/assets/LLM.pdf").load()
web_data = WebBaseLoader("https://www.w3schools.com/ai/").load()
arxiv_data = ArxivLoader(query="1706.03762").load()
# print(text_data)  # Display the loaded data
# print(pdf_data)  # Display the loaded PDF data
# print(web_data)  # Display the loaded web data
# print(arxiv_data)  # Display the loaded arXiv data