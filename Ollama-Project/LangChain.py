# 1. Imports
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool
from langchain.tools import DuckDuckGoSearchRun
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# 2. Local LLM Configuration (Hugging Face)
model_name = "facebook/opt-350m"  # Small, fast model for demo purposes
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create a text generation pipeline
hf_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=100,  # Limit output length
    temperature=0.7
)

# Wrap it in LangChain's HuggingFacePipeline
local_llm = HuggingFacePipeline(pipeline=hf_pipeline)

# 3. Prompt Template
qa_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template="Given the following context:\n{context}\n\nAnswer this question: {question}"
)

# 4. Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 5. Tools
search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="Web Search",
        func=search.run,
        description="Use this to search the web for up-to-date information."
    )
]

# 6. Document Loaders and Vector Stores
# Load a sample text file
loader = TextLoader("sample.txt")
documents = loader.load()

# Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Use Hugging Face embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_documents(docs, embeddings)

# Create a retrieval chain with local LLM
retrieval_chain = RetrievalQA.from_chain_type(
    llm=local_llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    return_source_documents=True
)

# Add retrieval as a tool
tools.append(
    Tool(
        name="Document Retrieval",
        func=retrieval_chain.run,
        description="Retrieve and summarize info from a stored document."
    )
)

# 7. Agent (combines LLM, tools, and memory)
agent = initialize_agent(
    tools=tools,
    llm=local_llm,
    agent="conversational-react-description",
    memory=memory,
    verbose=True
)

# 8. Execution
queries = [
    "What is LangChain?",
    "Can you search the web for recent updates about it?",
    "What does my document say about AI?"
]

for query in queries:
    response = agent.run(query)
    print(f"Query: {query}")
    print(f"Response: {response}\n")