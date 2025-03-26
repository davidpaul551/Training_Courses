import os
import urllib3
from unittest import loader
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
load_dotenv()


loader = TextLoader("C:/Users/david.doggala/OneDrive - ascendion/Desktop/Langchain/vector-dbs/blog.txt",encoding="utf-8")
document = loader.load()
print("Splitting")
text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)
texts = text_splitter.split_documents(document)

print(f"created {len(texts)} chunks")

print("ingesting")

embeddings = OllamaEmbeddings(model="llama3.2")

PineconeVectorStore.from_documents(texts,embeddings,index_name = os.getenv("INDEX_NAME"))

print("finished")
