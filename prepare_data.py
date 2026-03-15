from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os

print("Loading your Hansards and Constitution...")

loader = PyPDFDirectoryLoader("data")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.from_documents(texts, embeddings)
vectorstore.save_local("faiss_index")

print(f"✅ Done! Processed {len(texts)} chunks. Vectorstore saved.")