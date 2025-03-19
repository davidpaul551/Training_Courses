# 🛠️ Required Libraries
import os
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# 🔑 Load Environment Variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# 📂 Load Documents
loader = DirectoryLoader("path/to/documents", glob="**/*.md", loader_cls=TextLoader)
documents = loader.load()

# 📄 Split Documents into Chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# 🧬 Create Embeddings & Vector Store
embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embedding)

# 🧠 Configure Language Model (e.g., OpenAI)
llm = OpenAI(model_name="gpt-3.5-turbo")

# 🔗 Create RetrievalQA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",                # Options: 'stuff', 'map_reduce', 'refine', etc.
    retriever=vectorstore.as_retriever()
)

# 💬 Function to Handle User Queries
def chat(query: str) -> str:
    response = qa_chain.run(query)
    return response

# Example Query
print(chat("What are the key features of the product?"))
