# Verify all imports in one place
try:
    import langchain
    import faiss
    import openai
    import sentence_transformers
    import transformers
    import tqdm
    # RetrievalQA is available through langchain.chains in langchain-classic
    from langchain_classic.chains.retrieval_qa.base import RetrievalQA
    from langchain_community.vectorstores import FAISS
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import CharacterTextSplitter
    from langchain_openai import ChatOpenAI
    from langchain_openai import OpenAIEmbeddings
    print("✅ All imports are available!")
except Exception as e:
    print("❌ Missing package or import error:", e)