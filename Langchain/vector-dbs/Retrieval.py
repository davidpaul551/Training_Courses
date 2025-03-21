import os
from turtle import mode
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings, ChatOllama, OllamaLLM
from langchain_pinecone import PineconeVectorStore
from langchain import hub

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from ollama import embeddings


embeddings = OllamaEmbeddings(model="llama3.2")
llm = OllamaLLM(model="llama3.2")
query = "What is pinecone in ML"
chain = PromptTemplate.from_template(template=query) | llm
res = chain.invoke(input={})
print(res)

vectorstore = PineconeVectorStore(
    index_name=os.getenv("INDEX_NAME") , embedding=embeddings,pinecone_api_key=os.getenv("PINECONE_API_KEY")
)

retrieval_qa_chat_prompt= hub.pull("langchain-ai/retrieval-qa-chat")
combine_docs_chain = create_stuff_documents_chain(llm,retrieval_qa_chat_prompt)
retrival_chain = create_retrieval_chain(retriever=vectorstore.as_retriever() , combine_docs_chain=combine_docs_chain)
res = retrival_chain.invoke(input = {"input":query})
print(res)

